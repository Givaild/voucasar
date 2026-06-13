from fastapi import FastAPI, Request, status
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from util.csrf import csrf_protection
import uvicorn
from conexao_db import get_pool
import logging
import os
import uuid
from dotenv import load_dotenv
from init_db import init_database
from util.rate_limit import (
    check_rate_limit,
    get_limit_from_env,
    get_excluded_paths_from_env,
)

# Importando routers de VouCasar
from backend.routers.usuario import router as usuario_router
from backend.routers.casal import router as casal_router
from backend.routers.presente import router as presente_router
from backend.routers.fonte_compra import router as fonte_compra_router
from backend.routers.transacao_presente import router as transacao_presente_router
from backend.routers.template import router as template_router

load_dotenv()

logger = logging.getLogger(__name__)

# Detectar ambiente
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inicializa o connection pool
    pool = get_pool()
    if pool:
        logger.info("Connection pool inicializado com sucesso!")
        try:
            init_database()
            logger.info("Tabelas inicializadas com sucesso!")
        except Exception as e:
            logger.error(f"Falha ao inicializar tabelas: {e}")
    else:
        logger.error("Falha ao inicializar connection pool")
    
    yield
    
    # Shutdown: limpa o connection pool
    if pool:
        logger.info("Connection pool limpo")

# Configuracao de Rate Limiting global por IP
RATE_LIMIT_PER_SECOND = get_limit_from_env("RATE_LIMIT_GLOBAL_PER_SECOND", 20)
RATE_LIMIT_PER_MINUTE = get_limit_from_env("RATE_LIMIT_GLOBAL_PER_MINUTE", 120)
RATE_LIMIT_EXCLUDED_PATHS = get_excluded_paths_from_env("RATE_LIMIT_EXCLUDED_PATHS")

app = FastAPI(
    title="VouCasar - Lista de Casamento",
    description="API para gerenciamento de lista de casamento",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Erro não tratado na aplicação")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"erro": "Erro interno do servidor. Tente novamente mais tarde."},
        )

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    # Proteção CSRF
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        # Excluir apenas endpoints realmente publicos da protecao CSRF
        excluded_paths = [
            # Publico: cadastro e login
            "/api/usuario",
            "/api/usuario/auth/login",
            # Publico: leitura
            "/api/presente/publico",
            "/api/casal/publico",
            "/api/template/publico",
            # Publico: fluxo de PIX
            "/api/transacao-presente/publico",
        ]
        is_excluded = any(request.url.path.startswith(path) for path in excluded_paths)

        if not is_excluded:
            token_recebido = csrf_protection.get_token_from_request(request)
            if not csrf_protection.validate_token(request, token_recebido):
                return JSONResponse(status_code=403, content={"detail": "Token CSRF inválido ou ausente"})

    # Garantir que o token exista na sessão ANTES do call_next —
    # o SessionMiddleware serializa a sessão durante call_next,
    # então qualquer escrita depois chega tarde demais.
    csrf_protection.get_or_create_token(request)

    response = await call_next(request)

    # Ler o token já persistido na sessão e enviar como header e cookie
    # O cookie não é acessível ao JS em contexto cross-origin (localhost:5173 → :8000),
    # então o header é o canal confiável para o frontend ler e reenviar nos POSTs.
    token = csrf_protection.get_token_from_session(request)
    if token:
        response.headers["X-CSRF-Token"] = token
        response.set_cookie(
            key="csrf_token",
            value=token,
            httponly=False,
            samesite="lax",
            secure=IS_PRODUCTION
        )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    user_id = '-'
    if hasattr(request, 'session'):
        usuario = request.session.get('usuario')
        if usuario:
            user_id = str(usuario.get('id', '-'))
    
    ip = request.client.host if request.client else '-'
    user_agent = request.headers.get('user-agent', '-')[:100]
    
    log_extra = {
        'request_id': request_id,
        'user_id': user_id,
        'ip': ip,
        'user_agent': user_agent
    }
    
    request.state.log_extra = log_extra
    response = await call_next(request)
    return response

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting global por IP, aplicado a todas as requisicoes.
    Aplica duas janelas deslizantes:
      - 1 segundo: protege contra rajadas/ataques de forca bruta
      - 1 minuto: protege contra scraping e uso abusivo sostenido
    Endpoints listados em RATE_LIMIT_EXCLUDED_PATHS sao ignorados
    (ex.: /health, /docs, /).
    """
    path = request.url.path
    if path in RATE_LIMIT_EXCLUDED_PATHS:
        return await call_next(request)

    # Janela curta: 1 segundo
    allowed, retry_after = check_rate_limit(
        request,
        key="global:per_second",
        limit=RATE_LIMIT_PER_SECOND,
        window_seconds=1,
    )
    if not allowed:
        logger.warning(
            "Rate limit por segundo excedido para o IP",
            extra={"ip": request.client.host if request.client else "-", "path": path},
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Muitas requisicoes. Tente novamente em alguns instantes."},
            headers={"Retry-After": str(retry_after)},
        )

    # Janela longa: 1 minuto
    allowed, retry_after = check_rate_limit(
        request,
        key="global:per_minute",
        limit=RATE_LIMIT_PER_MINUTE,
        window_seconds=60,
    )
    if not allowed:
        logger.warning(
            "Rate limit por minuto excedido para o IP",
            extra={"ip": request.client.host if request.client else "-", "path": path},
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Muitas requisicoes. Tente novamente em alguns instantes."},
            headers={"Retry-After": str(retry_after)},
        )

    return await call_next(request)

SECRET_KEY = os.getenv('SECRET_KEY', 'voucasar-secret-key-change-in-production')
if IS_PRODUCTION and SECRET_KEY == 'voucasar-secret-key-change-in-production':
    raise ValueError("SECRET_KEY deve ser alterada em produção")

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=2592000,
    same_site="lax",
    https_only=IS_PRODUCTION,
    session_cookie="voucasar_session"
)

allowed_origins = [FRONTEND_URL]
if not IS_PRODUCTION:
    allowed_origins.extend([
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173"   
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-CSRF-Token",
        "X-Captcha-Token",
        "X-Confirm-Token",
        "X-Requested-With",
        "Accept",
    ],
    expose_headers=["X-CSRF-Token"],
)


# Incluindo routers com prefixo /api
app.include_router(usuario_router, prefix="/api")
app.include_router(casal_router, prefix="/api")
app.include_router(presente_router, prefix="/api")
app.include_router(fonte_compra_router, prefix="/api")
app.include_router(transacao_presente_router, prefix="/api")
app.include_router(template_router, prefix="/api")

@app.get("/")
async def root():
    return {"mensagem": "VouCasar - API de Lista de Casamento", "versao": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
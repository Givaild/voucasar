from fastapi import APIRouter, Request, Body, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from util.auth_decorator import requer_autenticacao
from backend.data.model.usuario import Usuario
from backend.data.repo import usuario as usuario_repo

router = APIRouter(prefix="/usuario", tags=["usuario"])
logger = logging.getLogger(__name__)

@router.post("")
async def criar_usuario(request: Request, usuario_data: dict = Body(...)):
    """Cria um novo usuário"""
    try:
        usuario = Usuario(
            id=0,
            nome=usuario_data.get("nome"),
            email=usuario_data.get("email"),
            senha=usuario_data.get("senha")
        )
        cod_usuario = usuario_repo.inserir(usuario)
        return JSONResponse({
            "id": cod_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "mensagem": "Usuário criado com sucesso"
        })
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{usuario_id}")
@requer_autenticacao()
async def buscar_usuario_endpoint(usuario_id: int, request: Request, usuario_logado: dict = None):
    """Busca um usuário por ID"""
    try:
        usuario = usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return JSONResponse({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        })
    except Exception as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{usuario_id}")
@requer_autenticacao()
async def atualizar_usuario_endpoint(usuario_id: int, request: Request, usuario_data: dict = Body(...), usuario_logado: dict = None):
    """Atualiza um usuário"""
    try:
        usuario = usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        
        usuario.nome = usuario_data.get("nome", usuario.nome)
        usuario.email = usuario_data.get("email", usuario.email)
        usuario.senha = usuario_data.get("senha", usuario.senha)
        
        usuario_repo.atualizar(usuario)
        return JSONResponse({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "mensagem": "Usuário atualizado com sucesso"
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("")
@requer_autenticacao()
async def listar_usuarios_endpoint(request: Request, usuario_logado: dict = None):
    """Lista todos os usuários"""
    try:
        usuarios = usuario_repo.listar_todos()
        return JSONResponse([
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email
            } for u in usuarios
        ])
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/auth/login")
async def login(request: Request, credenciais: dict = Body(...)):
    """Faz login de um usuário"""
    try:
        email = credenciais.get("email")
        senha = credenciais.get("senha")
        
        # Buscar usuário por email listando todos
        usuarios = usuario_repo.listar_todos()
        usuario = next((u for u in usuarios if u.email == email), None)
        
        if not usuario or usuario.senha != senha:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
            
        request.session["usuario_id"] = usuario.id
        request.session["usuario_nome"] = usuario.nome
        
        return JSONResponse({
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email
            },
            "mensagem": "Login realizado com sucesso"
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao fazer login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/auth/logout")
async def logout(request: Request):
    """Faz logout de um usuário"""
    request.session.clear()
    return JSONResponse({"mensagem": "Logout realizado com sucesso"})

@router.get("/auth/me")
async def me(request: Request):
    """Retorna dados do usuário autenticado"""
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
        
    try:
        usuario = usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
            
        return JSONResponse({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        })
    except Exception as e:
        logger.error(f"Erro ao buscar usuário atual: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

from functools import wraps
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
import os
import datetime
import logging

logger = logging.getLogger(__name__)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
INACTIVITY_TIMEOUT_MINUTES = 30


def get_log_extra(request: Request) -> dict:
    if hasattr(request, 'state') and hasattr(request.state, 'log_extra'):
        return request.state.log_extra
    return {}


def obter_usuario_logado(request: Request) -> Optional[dict]:
    if not hasattr(request, 'session'):
        return None
    
    usuario = request.session.get('usuario')
    if not usuario:
        return None
    
    expira_em = request.session.get('_expira_em')
    if expira_em:
        try:
            expiracao = datetime.datetime.fromisoformat(expira_em)
            if datetime.datetime.now() > expiracao:
                request.session.clear()
                return None
        except:
            pass
    
    last_activity = request.session.get('_last_activity')
    if last_activity:
        try:
            ultima_atividade = datetime.datetime.fromisoformat(last_activity)
            tempo_inativo = datetime.datetime.now() - ultima_atividade
            if tempo_inativo.total_seconds() > (INACTIVITY_TIMEOUT_MINUTES * 60):
                logger.warning(
                    f"Sessão expirada por inatividade ({int(tempo_inativo.total_seconds() / 60)} minutos)",
                    extra={
                        **get_log_extra(request),
                        'user_id': usuario.get('cod_usuario', '-'),
                        'email': usuario.get('email_usuario', '-'),
                        'role': usuario.get('role_usuario', '-')
                    }
                )
                request.session.clear()
                return None
        except:
            pass
    
    return usuario


def esta_logado(request: Request) -> bool:
    usuario = obter_usuario_logado(request)
    return usuario is not None and len(usuario) > 0


def criar_sessao(request: Request, usuario: dict, max_age: int = None) -> None:
    if hasattr(request, 'session'):
        usuario_sessao = usuario.copy()
        usuario_sessao.pop('senha', None)
        usuario_sessao.pop('senha_usuario', None)
        request.session['usuario'] = usuario_sessao
        request.session['_last_activity'] = datetime.datetime.now().isoformat()
        
        if max_age is not None:
            request.session['_max_age'] = max_age


def destruir_sessao(request: Request) -> None:
    if hasattr(request, 'session'):
        request.session.clear()


def requer_autenticacao(perfis_autorizados: List[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            usuario = obter_usuario_logado(request)
            if not usuario:
                logger.warning(
                    "Acesso negado - usuário não autenticado",
                    extra={
                        **get_log_extra(request),
                        'path': request.url.path,
                        'method': request.method
                    }
                )
                accept = request.headers.get('accept', '')
                xrw = request.headers.get('x-requested-with', '')
                redirect_path = "/login?redirect=" + str(request.url.path)
                redirect_url = FRONTEND_URL.rstrip('/') + redirect_path
                if 'application/json' in accept or xrw.lower() == 'xmlhttprequest':
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                        'error': 'not_authenticated',
                        'redirect': redirect_url
                    })

                return RedirectResponse(
                    url=redirect_url,
                    status_code=status.HTTP_303_SEE_OTHER
                )
            
            request.session['_last_activity'] = datetime.datetime.now().isoformat()
            
            # # Verifica se é primeiro acesso (exceto para a própria página de configuração de senha)
            # primeiro_acesso = usuario.get('primeiro_acesso', False)
            # if primeiro_acesso and request.url.path not in ['/configurar-senha-primeiro-acesso', '/api/configurar-senha-primeiro-acesso']:
            #     accept = request.headers.get('accept', '')
            #     xrw = request.headers.get('x-requested-with', '')
            #     redirect_path = "/configurar-senha?redirect=" + str(request.url.path)
            #     redirect_url = FRONTEND_URL.rstrip('/') + redirect_path
            #     if 'application/json' in accept or xrw.lower() == 'xmlhttprequest':
            #         return JSONResponse(status_code=status.HTTP_200_OK, content={
            #             'primeiro_acesso': True,
            #             'redirect': redirect_url
            #         })

            #     return RedirectResponse(
            #         url=redirect_url,
            #         status_code=status.HTTP_303_SEE_OTHER
            #     )
            
            
            # Verifica autorização se perfis foram especificados
            if perfis_autorizados:
                perfil_usuario = usuario.get('role_usuario', 'cliente')
                perfil_usuario = perfil_usuario.lower() if isinstance(perfil_usuario, str) else perfil_usuario
                perfis_autorizados_lower = [p.lower() for p in perfis_autorizados]
                if perfil_usuario not in perfis_autorizados_lower:
                    logger.warning(
                        "Acesso negado - permissão insuficiente",
                        extra={
                            **get_log_extra(request),
                            'user_id': usuario.get('cod_usuario', '-'),
                            'email': usuario.get('email_usuario', '-'),
                            'role': perfil_usuario,
                            'required_roles': perfis_autorizados_lower,
                            'path': request.url.path,
                            'method': request.method
                        }
                    )
                    accept = request.headers.get('accept', '')
                    if 'application/json' in accept:
                        return JSONResponse(
                            status_code=status.HTTP_403_FORBIDDEN,
                            content={
                                'error': 'forbidden',
                                'message': 'Você não tem permissão para acessar este recurso',
                                'redirect': FRONTEND_URL.rstrip('/') + '/login'
                            }
                        )
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Você não tem permissão para acessar este recurso"
                    )
            
            # Adiciona o usuário aos kwargs para fácil acesso na rota, mas apenas se a função aceita
            import inspect
            sig = inspect.signature(func)
            if 'usuario_logado' in sig.parameters:
                kwargs['usuario_logado'] = usuario
            
            # Chama a função original
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Importação necessária para funções assíncronas
import asyncio
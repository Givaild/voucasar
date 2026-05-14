from fastapi import APIRouter, Request, Body, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from util.auth_decorator import requer_autenticacao
from backend.data.model.fonte_compra import FonteCompra
from backend.data.repo import fonte_compra as fonte_compra_repo

router = APIRouter(prefix="/fonte-compra", tags=["fonte-compra"])
logger = logging.getLogger(__name__)

@router.post("")
@requer_autenticacao()
async def criar_fonte_compra(request: Request, fonte_data: dict = Body(...), usuario_logado: dict = None):
    """Cria uma nova fonte de compra"""
    try:
        fonte = FonteCompra(
            id=0,
            id_presente=fonte_data.get("id_presente"),
            tipo=fonte_data.get("tipo"),
            url_externa=fonte_data.get("url_externa")
        )
        cod_fonte = fonte_compra_repo.inserir(fonte)
        return JSONResponse({
            "id": cod_fonte,
            "id_presente": fonte.id_presente,
            "tipo": fonte.tipo,
            "url_externa": fonte.url_externa,
            "mensagem": "Fonte de compra criada com sucesso"
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erro ao criar fonte de compra: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{fonte_id}")
@requer_autenticacao()
async def buscar_fonte_compra_endpoint(fonte_id: int, request: Request, usuario_logado: dict = None):
    """Busca uma fonte de compra por ID"""
    try:
        fonte = fonte_compra_repo.buscar_por_id(fonte_id)
        if not fonte:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fonte de compra não encontrada")
        return JSONResponse({
            "id": fonte.id,
            "id_presente": fonte.id_presente,
            "tipo": fonte.tipo,
            "url_externa": fonte.url_externa
        })
    except Exception as e:
        logger.error(f"Erro ao buscar fonte de compra: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{fonte_id}")
@requer_autenticacao()
async def atualizar_fonte_compra_endpoint(fonte_id: int, request: Request, fonte_data: dict = Body(...), usuario_logado: dict = None):
    """Atualiza uma fonte de compra"""
    try:
        fonte = fonte_compra_repo.buscar_por_id(fonte_id)
        if not fonte:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fonte de compra não encontrada")
        
        fonte.tipo = fonte_data.get("tipo", fonte.tipo)
        fonte.url_externa = fonte_data.get("url_externa", fonte.url_externa)
        
        fonte_compra_repo.atualizar(fonte)
        return JSONResponse({
            "id": fonte.id,
            "id_presente": fonte.id_presente,
            "tipo": fonte.tipo,
            "url_externa": fonte.url_externa,
            "mensagem": "Fonte de compra atualizada com sucesso"
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar fonte de compra: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{fonte_id}")
@requer_autenticacao()
async def deletar_fonte_compra_endpoint(fonte_id: int, request: Request, usuario_logado: dict = None):
    """Deleta uma fonte de compra"""
    try:
        fonte_compra_repo.deletar(fonte_id)
        return JSONResponse({"mensagem": "Fonte de compra deletada com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao deletar fonte de compra: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/presente/{presente_id}")
@requer_autenticacao()
async def listar_fontes_por_presente_endpoint(presente_id: int, request: Request, usuario_logado: dict = None):
    """Lista fontes de compra por presente"""
    try:
        fontes = fonte_compra_repo.listar_por_presente(presente_id)
        return JSONResponse([
            {
                "id": f.id,
                "id_presente": f.id_presente,
                "tipo": f.tipo,
                "url_externa": f.url_externa
            } for f in fontes
        ])
    except Exception as e:
        logger.error(f"Erro ao listar fontes de compra: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

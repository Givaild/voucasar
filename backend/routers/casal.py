from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from util.auth_decorator import requer_autenticacao
from backend.data.model.casal import Casal
from backend.data.repo import casal as casal_repo
from backend.data.repo import usuario as usuario_repo

router = APIRouter(prefix="/casal", tags=["casal"])
logger = logging.getLogger(__name__)

@router.post("")
@requer_autenticacao()
async def criar_casal(request: Request, usuario_logado: dict = None):
    """Cria um novo casal"""
    try:
        casal_data = await request.json()
        casal = Casal(
            id=0,
            id_usuario_1=casal_data.get("id_usuario_1"),
            id_usuario_2=casal_data.get("id_usuario_2"),
            email_usuario_2=casal_data.get("email_usuario_2"),
            chave_pix=casal_data.get("chave_pix"),
            data_casamento=casal_data.get("data_casamento")
        )
        cod_casal = casal_repo.inserir(casal)
        return JSONResponse({
            "id": cod_casal,
            "id_usuario_1": casal.id_usuario_1,
            "id_usuario_2": casal.id_usuario_2,
            "email_usuario_2": casal.email_usuario_2,
            "chave_pix": casal.chave_pix,
            "data_casamento": str(casal.data_casamento),
            "mensagem": "Casal criado com sucesso"
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erro ao criar casal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{casal_id}")
@requer_autenticacao()
async def buscar_casal_endpoint(casal_id: int, request: Request, usuario_logado: dict = None):
    """Busca um casal por ID"""
    try:
        casal = casal_repo.buscar_por_id(casal_id)
        if not casal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Casal não encontrado")
        return JSONResponse({
            "id": casal.id,
            "id_usuario_1": casal.id_usuario_1,
            "id_usuario_2": casal.id_usuario_2,
            "email_usuario_2": casal.email_usuario_2,
            "chave_pix": casal.chave_pix,
            "data_casamento": str(casal.data_casamento)
        })
    except Exception as e:
        logger.error(f"Erro ao buscar casal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{casal_id}")
@requer_autenticacao()
async def atualizar_casal_endpoint(casal_id: int, request: Request, usuario_logado: dict = None):
    """Atualiza um casal"""
    try:
        casal_data = await request.json()
        casal = casal_repo.buscar_por_id(casal_id)
        if not casal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Casal não encontrado")
        
        casal.id_usuario_1 = casal_data.get("id_usuario_1", casal.id_usuario_1)
        casal.id_usuario_2 = casal_data.get("id_usuario_2", casal.id_usuario_2)
        casal.email_usuario_2 = casal_data.get("email_usuario_2", casal.email_usuario_2)
        casal.chave_pix = casal_data.get("chave_pix", casal.chave_pix)
        casal.data_casamento = casal_data.get("data_casamento", casal.data_casamento)
        
        casal_repo.atualizar(casal)

        # Se o email_usuario_2 mudou, tentar auto-vincular imediatamente
        # caso já exista uma conta com esse email
        if casal.email_usuario_2 and (not casal.id_usuario_2 or casal.id_usuario_2 == 0):
            try:
                usuario_existente = usuario_repo.buscar_por_email(casal.email_usuario_2)
                if usuario_existente:
                    casal_repo.vincular_por_email(casal.email_usuario_2, usuario_existente.id)
                    casal.id_usuario_2 = usuario_existente.id
                    logger.info(f"Parceiro auto-vinculado após atualização de email: {casal.email_usuario_2}")
            except Exception as link_err:
                logger.warning(f"Não foi possível auto-vincular parceiro na atualização: {link_err}")

        return JSONResponse({
            "id": casal.id,
            "id_usuario_1": casal.id_usuario_1,
            "id_usuario_2": casal.id_usuario_2,
            "email_usuario_2": casal.email_usuario_2,
            "chave_pix": casal.chave_pix,
            "data_casamento": str(casal.data_casamento),
            "mensagem": "Casal atualizado com sucesso"
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar casal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{casal_id}")
@requer_autenticacao()
async def deletar_casal_endpoint(casal_id: int, request: Request, usuario_logado: dict = None):
    """Deleta um casal"""
    try:
        casal_repo.deletar(casal_id)
        return JSONResponse({"mensagem": "Casal deletado com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao deletar casal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{casal_id}/parceiro")
@requer_autenticacao()
async def desvincular_parceiro_endpoint(casal_id: int, request: Request, usuario_logado: dict = None):
    """Remove a vinculação do parceiro(a) ao casal. Pode ser feito pelo criador ou pelo próprio parceiro."""
    try:
        casal = casal_repo.buscar_por_id(casal_id)
        if not casal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Casal não encontrado")

        usuario_id = usuario_logado.get("id")
        if casal.id_usuario_1 != usuario_id and casal.id_usuario_2 != usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão para desvincular este casal")

        desvinculou = casal_repo.desvincular_parceiro(casal_id, usuario_id)
        if not desvinculou:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum parceiro vinculado para remover")

        return JSONResponse({"mensagem": "Parceiro(a) desvinculado(a) com sucesso"})
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao desvincular parceiro: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/publico/{casal_id}")
async def buscar_casal_publico(casal_id: int):
    """Busca informações básicas de um casal publicamente"""
    try:
        casal = casal_repo.buscar_por_id(casal_id)
        if not casal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Casal não encontrado")
        return JSONResponse({
            "id": casal.id,
            "data_casamento": str(casal.data_casamento),
            "chave_pix": casal.chave_pix,
        })
    except Exception as e:
        logger.error(f"Erro ao buscar casal público: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("")
@requer_autenticacao()
async def listar_casais_endpoint(request: Request, usuario_logado: dict = None):
    """Lista os casais associados ao usuário logado"""
    try:
        casais = casal_repo.listar_por_usuario(usuario_logado.get("id"))
        return JSONResponse([
            {
                "id": c.id,
                "id_usuario_1": c.id_usuario_1,
                "id_usuario_2": c.id_usuario_2,
                "email_usuario_2": c.email_usuario_2,
                "chave_pix": c.chave_pix,
                "data_casamento": str(c.data_casamento)
            } for c in casais
        ])
    except Exception as e:
        logger.error(f"Erro ao listar casais: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

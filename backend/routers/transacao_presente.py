from fastapi import APIRouter, Request, Body, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from util.auth_decorator import requer_autenticacao
from backend.data.model.transacao_presente import TransacaoPresente
from backend.data.repo import transacao_presente as transacao_repo

router = APIRouter(prefix="/transacao-presente", tags=["transacao-presente"])
logger = logging.getLogger(__name__)

@router.post("")
@requer_autenticacao()
async def criar_transacao_presente(request: Request, transacao_data: dict = Body(...), usuario_logado: dict = None):
    """Cria uma nova transação de presente"""
    try:
        transacao = TransacaoPresente(
            id=0,
            id_presente=transacao_data.get("id_presente"),
            id_fonte_compra=transacao_data.get("id_fonte_compra"),
            id_casal=transacao_data.get("id_casal"),
            id_convidado=transacao_data.get("id_convidado"),
            assinatura_remetente=transacao_data.get("assinatura_remetente"),
            status_pagamento=transacao_data.get("status_pagamento", "pendente")
        )
        cod_transacao = transacao_repo.inserir(transacao)
        return JSONResponse({
            "id": cod_transacao,
            "id_presente": transacao.id_presente,
            "id_fonte_compra": transacao.id_fonte_compra,
            "id_casal": transacao.id_casal,
            "id_convidado": transacao.id_convidado,
            "assinatura_remetente": transacao.assinatura_remetente,
            "status_pagamento": transacao.status_pagamento,
            "mensagem": "Transação criada com sucesso"
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erro ao criar transação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{transacao_id}")
@requer_autenticacao()
async def buscar_transacao_endpoint(transacao_id: int, request: Request, usuario_logado: dict = None):
    """Busca uma transação por ID"""
    try:
        transacao = transacao_repo.buscar_por_id(transacao_id)
        if not transacao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
        return JSONResponse({
            "id": transacao.id,
            "id_presente": transacao.id_presente,
            "id_fonte_compra": transacao.id_fonte_compra,
            "id_casal": transacao.id_casal,
            "id_convidado": transacao.id_convidado,
            "assinatura_remetente": transacao.assinatura_remetente,
            "status_pagamento": transacao.status_pagamento
        })
    except Exception as e:
        logger.error(f"Erro ao buscar transação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{transacao_id}")
@requer_autenticacao()
async def atualizar_transacao_endpoint(transacao_id: int, request: Request, transacao_data: dict = Body(...), usuario_logado: dict = None):
    """Atualiza uma transação"""
    try:
        transacao = transacao_repo.buscar_por_id(transacao_id)
        if not transacao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
        
        transacao.assinatura_remetente = transacao_data.get("assinatura_remetente", transacao.assinatura_remetente)
        transacao.status_pagamento = transacao_data.get("status_pagamento", transacao.status_pagamento)
        
        transacao_repo.atualizar(transacao)
        return JSONResponse({
            "id": transacao.id,
            "id_presente": transacao.id_presente,
            "id_fonte_compra": transacao.id_fonte_compra,
            "id_casal": transacao.id_casal,
            "id_convidado": transacao.id_convidado,
            "assinatura_remetente": transacao.assinatura_remetente,
            "status_pagamento": transacao.status_pagamento,
            "mensagem": "Transação atualizada com sucesso"
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar transação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{transacao_id}")
@requer_autenticacao()
async def deletar_transacao_endpoint(transacao_id: int, request: Request, usuario_logado: dict = None):
    """Deleta uma transação"""
    try:
        transacao_repo.deletar(transacao_id)
        return JSONResponse({"mensagem": "Transação deletada com sucesso"})
    except Exception as e:
        logger.error(f"Erro ao deletar transação: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/casal/{casal_id}")
@requer_autenticacao()
async def listar_transacoes_por_casal_endpoint(casal_id: int, request: Request, usuario_logado: dict = None):
    """Lista transações por casal"""
    try:
        transacoes = transacao_repo.listar_por_casal(casal_id)
        return JSONResponse([
            {
                "id": t.id,
                "id_presente": t.id_presente,
                "id_fonte_compra": t.id_fonte_compra,
                "id_casal": t.id_casal,
                "id_convidado": t.id_convidado,
                "assinatura_remetente": t.assinatura_remetente,
                "status_pagamento": t.status_pagamento
            } for t in transacoes
        ])
    except Exception as e:
        logger.error(f"Erro ao listar transações por casal: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/convidado/{convidado_id}")
@requer_autenticacao()
async def listar_transacoes_por_convidado_endpoint(convidado_id: int, request: Request, usuario_logado: dict = None):
    """Lista transações por convidado"""
    try:
        transacoes = transacao_repo.listar_por_convidado(convidado_id)
        return JSONResponse([
            {
                "id": t.id,
                "id_presente": t.id_presente,
                "id_fonte_compra": t.id_fonte_compra,
                "id_casal": t.id_casal,
                "id_convidado": t.id_convidado,
                "assinatura_remetente": t.assinatura_remetente,
                "status_pagamento": t.status_pagamento
            } for t in transacoes
        ])
    except Exception as e:
        logger.error(f"Erro ao listar transações por convidado: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

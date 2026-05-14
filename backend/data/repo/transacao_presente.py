from typing import Optional, List
from util.database import get_connection
from backend.data.model.transacao_presente import TransacaoPresente
from backend.data.sql.transacao_presente_sql import *

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela TransacaoPresente: {e}")
        return False

def inserir(transacao_presente: TransacaoPresente, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            transacao_presente.id_presente,
            transacao_presente.id_fonte_compra,
            transacao_presente.id_casal,
            transacao_presente.id_convidado,
            transacao_presente.assinatura_remetente,
            transacao_presente.status_pagamento
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                transacao_presente.id_presente,
                transacao_presente.id_fonte_compra,
                transacao_presente.id_casal,
                transacao_presente.id_convidado,
                transacao_presente.assinatura_remetente,
                transacao_presente.status_pagamento
            ))
            cod_transacao_presente = cursor.lastrowid
            conn.commit()
            cursor.close()
            return cod_transacao_presente

def deletar(cod_transacao_presente: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_transacao_presente,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar transacao_presente: {e}")
        return False

def atualizar(transacao_presente: TransacaoPresente) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                transacao_presente.id_presente,
                transacao_presente.id_fonte_compra,
                transacao_presente.id_casal,
                transacao_presente.id_convidado,
                transacao_presente.assinatura_remetente,
                transacao_presente.status_pagamento,
                transacao_presente.id
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar transacao_presente: {e}")
        return False

def buscar_por_id(cod_transacao_presente: int) -> Optional[TransacaoPresente]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_ID, (cod_transacao_presente,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return TransacaoPresente(
                    id=resultado[0],
                    id_presente=resultado[1],
                    id_fonte_compra=resultado[2],
                    id_casal=resultado[3],
                    id_convidado=resultado[4],
                    assinatura_remetente=resultado[5],
                    status_pagamento=resultado[6]
                )
            return None
    except Exception as e:
        print(f"Erro ao buscar transacao_presente por id: {e}")
        return None

def listar_por_casal(cod_casal: int) -> List[TransacaoPresente]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_POR_CASAL, (cod_casal,))
            resultados = cursor.fetchall()
            cursor.close()
            transacoes_presente = []
            for resultado in resultados:
                transacoes_presente.append(TransacaoPresente(
                    id=resultado[0],
                    id_presente=resultado[1],
                    id_fonte_compra=resultado[2],
                    id_casal=resultado[3],
                    id_convidado=resultado[4],
                    assinatura_remetente=resultado[5],
                    status_pagamento=resultado[6]
                ))
            return transacoes_presente
    except Exception as e:
        print(f"Erro ao listar transacoes_presente por casal: {e}")
        return []

def listar_por_convidado(cod_convidado: int) -> List[TransacaoPresente]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_POR_CONVIDADO, (cod_convidado,))
            resultados = cursor.fetchall()
            cursor.close()
            transacoes_presente = []
            for resultado in resultados:
                transacoes_presente.append(TransacaoPresente(
                    id=resultado[0],
                    id_presente=resultado[1],
                    id_fonte_compra=resultado[2],
                    id_casal=resultado[3],
                    id_convidado=resultado[4],
                    assinatura_remetente=resultado[5],
                    status_pagamento=resultado[6]
                ))
            return transacoes_presente
    except Exception as e:
        print(f"Erro ao listar transacoes_presente por convidado: {e}")
        return []

def listar_todos() -> List[TransacaoPresente]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_TODOS)
            resultados = cursor.fetchall()
            cursor.close()
            transacoes_presente = []
            for resultado in resultados:
                transacoes_presente.append(TransacaoPresente(
                    id=resultado[0],
                    id_presente=resultado[1],
                    id_fonte_compra=resultado[2],
                    id_casal=resultado[3],
                    id_convidado=resultado[4],
                    assinatura_remetente=resultado[5],
                    status_pagamento=resultado[6]
                ))
            return transacoes_presente
    except Exception as e:
        print(f"Erro ao listar transacoes_presente: {e}")
        return []

from typing import Optional
from util.database import get_connection
from backend.data.model.casal import Casal
from backend.data.sql.casal_sql import *

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela Casal: {e}")
        return False

def inserir(casal: Casal, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            casal.id_usuario_1,
            casal.id_usuario_2,
            casal.chave_pix,
            casal.data_casamento
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                casal.id_usuario_1,
                casal.id_usuario_2,
                casal.chave_pix,
                casal.data_casamento
            ))
            cod_casal = cursor.lastrowid
            conn.commit()
            cursor.close()
            return cod_casal
        
def deletar(cod_casal: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_casal,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar casal: {e}")
        return False
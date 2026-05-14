from typing import Optional, List
from util.database import get_connection
from backend.data.model.fonte_compra import FonteCompra
from backend.data.sql.fonte_compra_sql import *

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela FonteCompra: {e}")
        return False

def inserir(fonte_compra: FonteCompra, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            fonte_compra.id_presente,
            fonte_compra.tipo,
            fonte_compra.url_externa
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                fonte_compra.id_presente,
                fonte_compra.tipo,
                fonte_compra.url_externa
            ))
            cod_fonte_compra = cursor.lastrowid
            conn.commit()
            cursor.close()
            return cod_fonte_compra

def deletar(cod_fonte_compra: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_fonte_compra,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar fonte_compra: {e}")
        return False

def atualizar(fonte_compra: FonteCompra) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                fonte_compra.id_presente,
                fonte_compra.tipo,
                fonte_compra.url_externa,
                fonte_compra.id
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar fonte_compra: {e}")
        return False

def buscar_por_id(cod_fonte_compra: int) -> Optional[FonteCompra]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_ID, (cod_fonte_compra,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return FonteCompra(
                    id=resultado[0],
                    id_presente=resultado[1],
                    tipo=resultado[2],
                    url_externa=resultado[3]
                )
            return None
    except Exception as e:
        print(f"Erro ao buscar fonte_compra por id: {e}")
        return None

def listar_por_presente(cod_presente: int) -> List[FonteCompra]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_POR_PRESENTE, (cod_presente,))
            resultados = cursor.fetchall()
            cursor.close()
            fontes_compra = []
            for resultado in resultados:
                fontes_compra.append(FonteCompra(
                    id=resultado[0],
                    id_presente=resultado[1],
                    tipo=resultado[2],
                    url_externa=resultado[3]
                ))
            return fontes_compra
    except Exception as e:
        print(f"Erro ao listar fontes_compra por presente: {e}")
        return []

def listar_todos() -> List[FonteCompra]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_TODOS)
            resultados = cursor.fetchall()
            cursor.close()
            fontes_compra = []
            for resultado in resultados:
                fontes_compra.append(FonteCompra(
                    id=resultado[0],
                    id_presente=resultado[1],
                    tipo=resultado[2],
                    url_externa=resultado[3]
                ))
            return fontes_compra
    except Exception as e:
        print(f"Erro ao listar fontes_compra: {e}")
        return []

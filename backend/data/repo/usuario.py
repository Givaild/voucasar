from typing import Optional, List
from util.database import get_connection
from backend.data.model.usuario import Usuario
from backend.data.sql.usuario_sql import *

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela Usuario: {e}")
        return False

def inserir(usuario: Usuario, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                usuario.nome,
                usuario.email,
                usuario.senha
            ))
            cod_usuario = cursor.lastrowid
            conn.commit()
            cursor.close()
            return cod_usuario

def deletar(cod_usuario: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR, (cod_usuario,))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao deletar usuario: {e}")
        return False

def atualizar(usuario: Usuario) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR, (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.id
            ))
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao atualizar usuario: {e}")
        return False

def buscar_por_id(cod_usuario: int) -> Optional[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_ID, (cod_usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return Usuario(
                    id=resultado[0],
                    nome=resultado[1],
                    email=resultado[2],
                    senha=resultado[3]
                )
            return None
    except Exception as e:
        print(f"Erro ao buscar usuario por id: {e}")
        return None

def buscar_por_email(email: str) -> Optional[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(BUSCAR_POR_EMAIL, (email,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return Usuario(
                    id=resultado[0],
                    nome=resultado[1],
                    email=resultado[2],
                    senha=resultado[3]
                )
            return None
    except Exception as e:
        print(f"Erro ao buscar usuario por email: {e}")
        return None

def listar_todos() -> List[Usuario]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(LISTAR_TODOS)
            resultados = cursor.fetchall()
            cursor.close()
            usuarios = []
            for resultado in resultados:
                usuarios.append(Usuario(
                    id=resultado[0],
                    nome=resultado[1],
                    email=resultado[2],
                    senha=resultado[3]
                ))
            return usuarios
    except Exception as e:
        print(f"Erro ao listar usuarios: {e}")
        return []

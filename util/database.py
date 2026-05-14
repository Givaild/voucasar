import mysql.connector
from contextlib import contextmanager
from typing import Optional, Generator
import sys
import os

# Forçar encoding UTF-8 para evitar problemas com caracteres especiais
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexao_db import criar_conexao, fechar_conexao

@contextmanager
def get_connection() -> Generator[mysql.connector.MySQLConnection, None, None]:
    conn = criar_conexao()
    if conn is None:
        raise Exception("Não foi possível conectar ao banco de dados")
    
    try:
        yield conn
    finally:
        if conn:
            # Devolve ao pool ao invés de fechar
            fechar_conexao(conn)

def executar_script_sql(script: str) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(script)
            conn.commit()
            cursor.close()
            return True
    except Exception as e:
        print(f"Erro ao executar script SQL: {e}")
        return False

def verificar_tabela_existe(nome_tabela: str) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name = %s
                )
            """, (nome_tabela,))
            existe = cursor.fetchone()[0]
            cursor.close()
            return existe
    except Exception as e:
        print(f"Erro ao verificar existência da tabela: {e}")
        return False

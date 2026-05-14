import mysql.connector
from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# ==========================================
# VALIDAÇÃO DAS VARIÁVEIS DE AMBIENTE
# ==========================================
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Validar credenciais obrigatórias
required_vars = {
    'DB_USER': DB_USER,
    'DB_PASSWORD': DB_PASSWORD,
    'DB_HOST': DB_HOST,
    'DB_PORT': DB_PORT,
    'DB_NAME': DB_NAME
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Variáveis de ambiente obrigatórias não configuradas no .env: {', '.join(missing_vars)}")

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS MYSQL
# ==========================================
DB_CONFIG = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': int(DB_PORT),
    'database': DB_NAME,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'use_unicode': True
}

# Connection pool
connection_pool = None

def get_pool():
    """Retorna o pool de conexões do MySQL"""
    global connection_pool
    
    if connection_pool is None:
        try:
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="integracar_pool",
                pool_size=20,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print(f"✓ MySQL Connection pool criado com sucesso!")
        except Error as e:
            print(f"✗ Erro ao criar connection pool: {e}")
            return None
    
    return connection_pool

def criar_conexao():
    """Obtém uma conexão do pool"""
    try:
        pool_obj = get_pool()
        if pool_obj:
            connection = pool_obj.get_connection()
            return connection
    except Error as e:
        print(f"✗ Erro ao obter conexão: {e}")
        return None

def fechar_conexao(conexao):
    """Devolve a conexão ao pool"""
    if conexao:
        try:
            conexao.close()  # No MySQL connector, close() devolve ao pool
        except Error as e:
            print(f"✗ Erro ao fechar conexão: {e}")

def executar_query(query, parametros=None, commit=False):
    """
    Executa uma query no MySQL
    
    Args:
        query: SQL query
        parametros: Tupla ou lista de parâmetros
        commit: Se True, faz commit da transação
    
    Returns:
        cursor se sucesso, None se erro
    """
    conexao = None
    cursor = None
    
    try:
        conexao = criar_conexao()
        if not conexao:
            return None
        
        cursor = conexao.cursor(dictionary=True)  # Retorna dicionários
        
        if parametros:
            cursor.execute(query, parametros)
        else:
            cursor.execute(query)
        
        if commit:
            conexao.commit()
        
        return cursor
        
    except Error as e:
        print(f"✗ Erro ao executar query: {e}")
        if cursor:
            cursor.close()
        if conexao:
            conexao.rollback()
            fechar_conexao(conexao)
        return None

def testar_conexao():
    """Testa a conexão com o MySQL"""
    try:
        conexao = criar_conexao()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            cursor.close()
            fechar_conexao(conexao)
            print(f"✓ Conectado ao MySQL versão: {version[0]}")
            return True
        return False
    except Error as e:
        print(f"✗ Erro ao testar conexão: {e}")
        return False

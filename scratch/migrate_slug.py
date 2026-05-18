import sys
import os

# Adicionar o diretório raiz ao path para encontrar o módulo util
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.database import get_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            logger.info("Verificando se a coluna 'slug' já existe na tabela 'Template'...")
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_schema = DATABASE() 
                AND table_name = 'Template' 
                AND column_name = 'slug'
            """)
            exists = cursor.fetchone()[0]
            
            if not exists:
                logger.info("Adicionando coluna 'slug' à tabela 'Template'...")
                cursor.execute("ALTER TABLE Template ADD COLUMN slug VARCHAR(255) UNIQUE AFTER id_casal")
                conn.commit()
                logger.info("✅ Coluna 'slug' adicionada com sucesso!")
            else:
                logger.info("⚠️ Coluna 'slug' já existe.")
                
            cursor.close()
    except Exception as e:
        logger.error(f"❌ Erro na migração: {e}")

if __name__ == "__main__":
    migrate()

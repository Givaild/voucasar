import logging
from backend.data.repo import usuario, casal, presente, fonte_compra, transacao_presente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Inicializa todas as tabelas do banco de dados"""
    try:
        logger.info("Iniciando criação de tabelas...")
        
        tables = [
            ("Usuario", usuario.criar_tabela),
            ("Casal", casal.criar_tabela),
            ("Presente", presente.criar_tabela),
            ("FonteCompra", fonte_compra.criar_tabela),
            ("TransacaoPresente", transacao_presente.criar_tabela),
        ]
        
        for table_name, create_func in tables:
            try:
                if create_func():
                    logger.info(f"✅ Tabela {table_name} criada com sucesso")
                else:
                    logger.warning(f"⚠️ Tabela {table_name} já existe ou não foi criada")
            except Exception as e:
                logger.error(f"❌ Erro ao criar tabela {table_name}: {e}")
        
        logger.info("✅ Inicialização de tabelas concluída!")
        
    except Exception as e:
        logger.error(f"❌ Erro geral: {e}")
        raise

if __name__ == "__main__":
    init_database()

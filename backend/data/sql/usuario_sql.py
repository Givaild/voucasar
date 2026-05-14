CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

INSERIR = """
INSERT INTO Usuario (
    nome,
    email,
    senha
)
VALUES (%s, %s, %s);
"""

DELETAR = """
DELETE FROM Usuario
WHERE id = %s;
"""

ATUALIZAR = """
UPDATE Usuario
SET nome = %s, email = %s, senha = %s
WHERE id = %s;
"""

BUSCAR_POR_ID = """
SELECT id, nome, email, senha
FROM Usuario
WHERE id = %s;
"""

BUSCAR_POR_EMAIL = """
SELECT id, nome, email, senha
FROM Usuario
WHERE email = %s;
"""

LISTAR_TODOS = """
SELECT id, nome, email, senha
FROM Usuario;
"""

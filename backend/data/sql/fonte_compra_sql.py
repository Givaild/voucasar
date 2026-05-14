CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS FonteCompra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_presente INT NOT NULL,
    tipo VARCHAR(255),
    url_externa VARCHAR(255),
    FOREIGN KEY (id_presente) REFERENCES Presente(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

INSERIR = """
INSERT INTO FonteCompra (
    id_presente,
    tipo,
    url_externa
)
VALUES (%s, %s, %s);
"""

DELETAR = """
DELETE FROM FonteCompra
WHERE id = %s;
"""

ATUALIZAR = """
UPDATE FonteCompra
SET id_presente = %s, tipo = %s, url_externa = %s
WHERE id = %s;
"""

BUSCAR_POR_ID = """
SELECT id, id_presente, tipo, url_externa
FROM FonteCompra
WHERE id = %s;
"""

LISTAR_POR_PRESENTE = """
SELECT id, id_presente, tipo, url_externa
FROM FonteCompra
WHERE id_presente = %s;
"""

LISTAR_TODOS = """
SELECT id, id_presente, tipo, url_externa
FROM FonteCompra;
"""

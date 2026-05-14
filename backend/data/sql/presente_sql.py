CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS Presente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_casal INT NOT NULL,
    id_categoria VARCHAR(255),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_estimado DECIMAL(10, 2),
    status VARCHAR(50),
    FOREIGN KEY (id_casal) REFERENCES Casal(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

INSERIR = """
INSERT INTO Presente (
    id_casal,
    id_categoria,
    titulo,
    descricao,
    valor_estimado,
    status
)
VALUES (%s, %s, %s, %s, %s, %s);
"""

DELETAR = """
DELETE FROM Presente
WHERE id = %s;
"""

ATUALIZAR = """
UPDATE Presente
SET id_casal = %s, id_categoria = %s, titulo = %s, descricao = %s, valor_estimado = %s, status = %s
WHERE id = %s;
"""

BUSCAR_POR_ID = """
SELECT id, id_casal, id_categoria, titulo, descricao, valor_estimado, status
FROM Presente
WHERE id = %s;
"""

LISTAR_POR_CASAL = """
SELECT id, id_casal, id_categoria, titulo, descricao, valor_estimado, status
FROM Presente
WHERE id_casal = %s;
"""

LISTAR_TODOS = """
SELECT id, id_casal, id_categoria, titulo, descricao, valor_estimado, status
FROM Presente;
"""

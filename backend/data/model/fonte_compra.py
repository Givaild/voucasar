from dataclasses import dataclass

@dataclass
class FonteCompra:
    id: int
    id_presente: int
    tipo: str
    url_externa: str
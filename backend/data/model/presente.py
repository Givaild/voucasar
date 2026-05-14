from dataclasses import dataclass

@dataclass
class Presente:
    id: int
    id_casal: int
    id_categoria: str
    titulo: str
    descricao: str
    valor_estimado: float
    status: str
from dataclasses import dataclass
import datetime

@dataclass
class Casal:
    id: int
    id_usuario_1: int
    id_usuario_2: int
    chave_pix: str
    data_casamento: datetime
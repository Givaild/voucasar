from dataclasses import dataclass

@dataclass
class TransacaoPresente:
    id: int
    id_presente: int
    id_fonte_compra: int
    id_casal: int
    id_convidado: int
    assinatura_remetente: str
    status_pagamento: str
from dataclasses import dataclass


@dataclass(frozen=True)
class Loja:
    id: str
    nome: str
    endereco: str
    horario: str


@dataclass(frozen=True)
class ItemEstoque:
    isbn: str
    loja_id: str
    quantidade: int

    @property
    def disponivel(self):
        return self.quantidade > 0

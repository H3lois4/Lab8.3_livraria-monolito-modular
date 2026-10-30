from dataclasses import dataclass

from compartilhado import normalizar


@dataclass(frozen=True)
class Livro:
    isbn: str
    titulo: str
    autor: str
    preco: float

    def corresponde(self, termo):
        termo = normalizar(termo)
        return termo in normalizar(self.titulo) or termo in normalizar(self.autor)

"""Dados próprios do módulo: data/lojas_estoque/lojas.txt e estoque.txt."""
from pathlib import Path

from compartilhado import ArquivoTxt

from .dominio import ItemEstoque, Loja

LOJAS = [
    ["paulista", "Livraria Paulista", "Av. Paulista, 1000 – São Paulo",
     "Seg a sáb, 10h às 22h; dom, 12h às 20h"],
    ["pinheiros", "Livraria Pinheiros", "Rua dos Pinheiros, 500 – São Paulo",
     "Todos os dias, 9h às 21h"],
]
ESTOQUE = [
    ["9788535902775", "paulista", "3"], ["9788535902775", "pinheiros", "0"],
    ["9788571641149", "paulista", "0"], ["9788535914641", "pinheiros", "2"],
    ["9788501114775", "paulista", "1"], ["9788501114775", "pinheiros", "5"],
]


class RepositorioLojasEstoque:
    def __init__(self, pasta):
        pasta = Path(pasta) / "lojas_estoque"
        self._lojas = ArquivoTxt(pasta / "lojas.txt")
        self._estoque = ArquivoTxt(pasta / "estoque.txt")
        if not self._lojas.existe():
            self._lojas.gravar(LOJAS)
        if not self._estoque.existe():
            self._estoque.gravar(ESTOQUE)

    def lojas(self):
        return [Loja(*campos) for campos in self._lojas.ler()]

    def loja(self, loja_id):
        return next((l for l in self.lojas() if l.id == loja_id), None)

    def estoque_do_livro(self, isbn):
        return [ItemEstoque(i, l, int(q)) for i, l, q in self._estoque.ler() if i == isbn]

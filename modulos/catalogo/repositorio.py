"""Dados próprios do módulo: data/catalogo/livros.txt (isbn|titulo|autor|preco)."""
from pathlib import Path

from compartilhado import ArquivoTxt

from .dominio import Livro

LIVROS = [
    ["9788535902775", "Dom Casmurro", "Machado de Assis", "29.90"],
    ["9788571641149", "Memórias Póstumas de Brás Cubas", "Machado de Assis", "34.50"],
    ["9788535914641", "Grande Sertão: Veredas", "João Guimarães Rosa", "89.00"],
    ["9788501114775", "A Hora da Estrela", "Clarice Lispector", "39.90"],
]


class RepositorioLivros:
    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "catalogo" / "livros.txt")
        if not self._arquivo.existe():
            self._arquivo.gravar(LIVROS)

    def listar(self):
        return [Livro(i, t, a, float(p)) for i, t, a, p in self._arquivo.ler()]

    def buscar(self, isbn):
        return next((l for l in self.listar() if l.isbn == isbn), None)

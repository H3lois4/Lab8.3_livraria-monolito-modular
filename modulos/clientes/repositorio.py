"""Dados próprios do módulo: data/clientes/preferencias.txt (cliente_id|loja_favorita)."""
from pathlib import Path

from compartilhado import ArquivoTxt


class RepositorioPreferencias:
    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "clientes" / "preferencias.txt")

    def loja_favorita(self, cliente_id):
        return dict(self._arquivo.ler()).get(cliente_id)

    def definir_loja_favorita(self, cliente_id, loja_id):
        prefs = dict(self._arquivo.ler())
        prefs[cliente_id] = loja_id
        self._arquivo.gravar([[c, l] for c, l in prefs.items()])

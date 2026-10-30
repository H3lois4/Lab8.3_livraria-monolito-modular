class LojaNaoEncontrada(Exception):
    def __init__(self):
        super().__init__("Loja não encontrada")


class ServicoLojasEstoque:
    def __init__(self, repositorio):
        self._repo = repositorio

    def listar_lojas(self):
        return sorted(self._repo.lojas(), key=lambda l: l.nome)

    def obter_loja(self, loja_id):
        loja = self._repo.loja(loja_id)
        if loja is None:
            raise LojaNaoEncontrada()
        return loja

    def disponibilidade(self, isbn, loja_favorita=None):
        """Estoque do livro por loja; a favorita primeiro, depois ordem alfabética."""
        itens = []
        for item in self._repo.estoque_do_livro(isbn):
            loja = self._repo.loja(item.loja_id)
            if loja:
                itens.append({"loja": loja, "quantidade": item.quantidade,
                              "disponivel": item.disponivel, "favorita": loja.id == loja_favorita})
        return sorted(itens, key=lambda i: (not i["favorita"], i["loja"].nome))

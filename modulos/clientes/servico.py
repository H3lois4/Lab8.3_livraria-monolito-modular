class ServicoClientes:
    def __init__(self, repositorio, lojas_api):
        self._repo = repositorio
        self._lojas = lojas_api  # comunicação com outro módulo só pela API pública

    def loja_favorita(self, cliente_id):
        return self._repo.loja_favorita(cliente_id)

    def definir_loja_favorita(self, cliente_id, loja_id):
        if not self._lojas.loja_existe(loja_id):
            raise self._lojas.LojaNaoEncontrada()
        self._repo.definir_loja_favorita(cliente_id, loja_id)
        return self._lojas.nome_da_loja(loja_id)

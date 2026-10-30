from .repositorio import RepositorioLojasEstoque
from .rotas import criar_rotas
from .servico import LojaNaoEncontrada, ServicoLojasEstoque


class LojasEstoqueAPI:
    """Contrato público do módulo, usado por Catálogo e Clientes."""

    LojaNaoEncontrada = LojaNaoEncontrada

    def __init__(self, servico):
        self._servico = servico

    def loja_existe(self, loja_id):
        try:
            self._servico.obter_loja(loja_id)
            return True
        except LojaNaoEncontrada:
            return False

    def nome_da_loja(self, loja_id):
        return self._servico.obter_loja(loja_id).nome

    def disponibilidade(self, isbn, loja_favorita=None):
        return self._servico.disponibilidade(isbn, loja_favorita)


class ModuloLojasEstoque:
    def __init__(self, pasta_dados, clientes_api_fornecedor):
        servico = ServicoLojasEstoque(RepositorioLojasEstoque(pasta_dados))
        self.api = LojasEstoqueAPI(servico)
        self.blueprint = criar_rotas(servico, clientes_api_fornecedor)


def criar_modulo(pasta_dados, clientes_api_fornecedor):
    return ModuloLojasEstoque(pasta_dados, clientes_api_fornecedor)

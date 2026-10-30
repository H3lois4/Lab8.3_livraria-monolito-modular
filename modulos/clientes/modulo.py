from .repositorio import RepositorioPreferencias
from .rotas import criar_rotas
from .servico import ServicoClientes


class ClientesAPI:
    """Contrato público do módulo, usado por Catálogo e Lojas e Estoque."""

    def __init__(self, servico):
        self._servico = servico

    def loja_favorita(self, cliente_id):
        return self._servico.loja_favorita(cliente_id)

    def definir_loja_favorita(self, cliente_id, loja_id):
        return self._servico.definir_loja_favorita(cliente_id, loja_id)


class ModuloClientes:
    def __init__(self, pasta_dados, lojas_api):
        servico = ServicoClientes(RepositorioPreferencias(pasta_dados), lojas_api)
        self.api = ClientesAPI(servico)
        self.blueprint = criar_rotas(servico, lojas_api.LojaNaoEncontrada)


def criar_modulo(pasta_dados, lojas_api):
    return ModuloClientes(pasta_dados, lojas_api)

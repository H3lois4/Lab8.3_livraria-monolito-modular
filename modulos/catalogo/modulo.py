from .repositorio import RepositorioLivros
from .rotas import criar_rotas
from .servico import ServicoCatalogo


class CatalogoAPI:
    """Contrato público do módulo."""

    def __init__(self, servico):
        self._servico = servico

    def buscar(self, termo=""):
        return self._servico.buscar(termo)

    def obter(self, isbn):
        return self._servico.obter(isbn)


class ModuloCatalogo:
    def __init__(self, pasta_dados, lojas_api, clientes_api_fornecedor):
        servico = ServicoCatalogo(RepositorioLivros(pasta_dados))
        self.api = CatalogoAPI(servico)
        self.blueprint = criar_rotas(servico, lojas_api, clientes_api_fornecedor)


def criar_modulo(pasta_dados, lojas_api, clientes_api_fornecedor):
    return ModuloCatalogo(pasta_dados, lojas_api, clientes_api_fornecedor)

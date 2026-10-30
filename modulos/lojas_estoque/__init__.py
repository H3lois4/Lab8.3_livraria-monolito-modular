"""Módulo Lojas e Estoque (equivale ao "Serviço de Lojas e Estoque").

API pública: tudo o que outros módulos podem usar está aqui.
Os arquivos internos (dominio, repositorio, servico, rotas) não devem ser importados de fora.
"""
from .modulo import LojasEstoqueAPI, criar_modulo

__all__ = ["LojasEstoqueAPI", "criar_modulo"]

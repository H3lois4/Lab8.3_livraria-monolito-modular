"""Módulo Catálogo (equivale ao "Serviço de Catálogo"): livros, preços e busca.
API pública abaixo; arquivos internos não devem ser importados por outros módulos."""
from .modulo import CatalogoAPI, criar_modulo

__all__ = ["CatalogoAPI", "criar_modulo"]

"""Utilitários técnicos usados por todos os módulos. Não contém regra de negócio."""
from .arquivo_txt import ArquivoTxt
from .texto import moeda, normalizar
from .web import cliente_id

__all__ = ["ArquivoTxt", "moeda", "normalizar", "cliente_id"]

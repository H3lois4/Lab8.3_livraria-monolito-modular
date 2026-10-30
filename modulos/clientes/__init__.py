"""Módulo Clientes (equivale ao "Serviço de Clientes"): preferências do cliente.
No MVP, guarda a loja favorita. API pública abaixo; arquivos internos não devem ser importados."""
from .modulo import ClientesAPI, criar_modulo

__all__ = ["ClientesAPI", "criar_modulo"]

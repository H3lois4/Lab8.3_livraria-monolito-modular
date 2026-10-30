import uuid

from flask import session


def cliente_id():
    """Identifica o cliente da sessão (o app não tem login)."""
    if "cliente_id" not in session:
        session["cliente_id"] = uuid.uuid4().hex
    return session["cliente_id"]

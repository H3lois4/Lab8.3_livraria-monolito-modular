"""Ponto de entrada para produção (Azure App Service com Gunicorn)."""
from app import create_app

app = create_app()

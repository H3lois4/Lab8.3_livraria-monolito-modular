"""Monolito modular: um único processo e um único deploy (equivale ao API Gateway do
diagrama 8.2). Este arquivo monta os módulos, injeta as APIs públicas de um no outro
e registra as rotas de cada um.

    modulos/catalogo       ->  Serviço de Catálogo        ->  data/catalogo/
    modulos/lojas_estoque  ->  Serviço de Lojas e Estoque ->  data/lojas_estoque/
    modulos/clientes       ->  Serviço de Clientes        ->  data/clientes/
    shell/                 ->  Shell do app (layout comum)
"""
import os

from flask import Flask, render_template

from compartilhado import moeda
from modulos import catalogo, clientes, lojas_estoque
from shell import PASTA_ESTATICOS, PASTA_TEMPLATES


def montar_modulos(pasta_dados):
    registro = {}
    estoque = lojas_estoque.criar_modulo(pasta_dados, lambda: registro["clientes"].api)
    registro["clientes"] = clientes.criar_modulo(pasta_dados, estoque.api)
    livros = catalogo.criar_modulo(pasta_dados, estoque.api, lambda: registro["clientes"].api)
    return {"catalogo": livros, "lojas_estoque": estoque, "clientes": registro["clientes"]}


def create_app(pasta_dados=None):
    pasta_dados = pasta_dados or os.environ.get("PASTA_DADOS", "data")
    app = Flask(__name__, template_folder=str(PASTA_TEMPLATES), static_folder=str(PASTA_ESTATICOS))
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento")
    app.add_template_filter(moeda, "moeda")

    modulos = montar_modulos(pasta_dados)
    app.config["MODULOS"] = modulos
    for modulo in modulos.values():
        app.register_blueprint(modulo.blueprint)

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return render_template("erro.html", mensagem=erro.description), 404

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)

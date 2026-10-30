from flask import Blueprint, abort, render_template, request

from compartilhado import cliente_id

from .servico import LivroNaoEncontrado


def criar_rotas(servico, lojas_api, clientes_api_fornecedor):
    bp = Blueprint("catalogo", __name__, template_folder="templates")

    @bp.get("/")
    def buscar():
        termo = request.args.get("q", "")
        return render_template("catalogo/busca.html", livros=servico.buscar(termo), termo=termo)

    @bp.get("/livros/<isbn>")
    def detalhe(isbn):
        try:
            livro = servico.obter(isbn)
        except LivroNaoEncontrado as erro:
            abort(404, description=str(erro))
        # composição: dados de outros módulos obtidos pelas APIs públicas
        favorita = clientes_api_fornecedor().loja_favorita(cliente_id())
        lojas = lojas_api.disponibilidade(isbn, favorita)
        return render_template("catalogo/detalhe.html", livro=livro, lojas=lojas)

    return bp

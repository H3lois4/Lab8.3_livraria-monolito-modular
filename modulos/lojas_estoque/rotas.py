from flask import Blueprint, abort, render_template

from compartilhado import cliente_id

from .servico import LojaNaoEncontrada


def criar_rotas(servico, clientes_api_fornecedor):
    bp = Blueprint("lojas", __name__, url_prefix="/lojas", template_folder="templates")

    def favorita():
        return clientes_api_fornecedor().loja_favorita(cliente_id())

    @bp.get("/")
    def listar():
        return render_template("lojas_estoque/lista.html", lojas=servico.listar_lojas(),
                               favorita=favorita())

    @bp.get("/<loja_id>")
    def detalhe(loja_id):
        try:
            loja = servico.obter_loja(loja_id)
        except LojaNaoEncontrada as erro:
            abort(404, description=str(erro))
        return render_template("lojas_estoque/detalhe.html", loja=loja, favorita=favorita())

    return bp

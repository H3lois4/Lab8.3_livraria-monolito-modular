from flask import Blueprint, abort, flash, redirect, request, url_for

from compartilhado import cliente_id


def criar_rotas(servico, erro_loja):
    bp = Blueprint("clientes", __name__, url_prefix="/clientes")

    @bp.post("/favorita/<loja_id>")
    def favoritar(loja_id):
        try:
            nome = servico.definir_loja_favorita(cliente_id(), loja_id)
        except erro_loja as erro:
            abort(404, description=str(erro))
        flash(f"{nome} agora é sua loja favorita.")
        return redirect(request.form.get("voltar") or url_for("lojas.listar"))

    return bp

import pytest

from app import create_app

DOM, HORA = "9788535902775", "9788501114775"


@pytest.fixture
def cliente(tmp_path):
    app = create_app(tmp_path)
    app.config["TESTING"] = True
    return app.test_client()


def html(r):
    return r.get_data(as_text=True)


def test_busca(cliente):
    pagina = html(cliente.get("/?q=clarice"))
    assert "A Hora da Estrela" in pagina and "R$ 39,90" in pagina and "Dom Casmurro" not in pagina


def test_busca_sem_resultado(cliente):
    assert "Nenhum livro encontrado" in html(cliente.get("/?q=harry"))


def test_detalhe_junta_dados_de_tres_modulos(cliente):
    pagina = html(cliente.get(f"/livros/{DOM}"))
    assert "R$ 29,90" in pagina and "3 em estoque" in pagina and "Esgotado" in pagina


def test_lojas(cliente):
    pagina = html(cliente.get("/lojas/pinheiros"))
    assert "Rua dos Pinheiros, 500" in pagina and "Todos os dias, 9h às 21h" in pagina


def test_404(cliente):
    assert cliente.get("/livros/000").status_code == 404
    assert cliente.get("/lojas/centro").status_code == 404
    assert cliente.post("/clientes/favorita/centro").status_code == 404


def test_favorita_aparece_primeiro(cliente):
    pagina = html(cliente.post("/clientes/favorita/pinheiros", follow_redirects=True))
    assert "Livraria Pinheiros agora é sua loja favorita." in pagina
    pagina = html(cliente.get(f"/livros/{HORA}"))
    assert pagina.index("Livraria Pinheiros") < pagina.index("Livraria Paulista")
    assert "Sua loja favorita" in pagina


def test_favorita_persiste_apos_reiniciar(tmp_path):
    c = create_app(tmp_path).test_client()
    c.post("/clientes/favorita/pinheiros")
    with c.session_transaction() as sessao:
        cid = sessao["cliente_id"]
    c2 = create_app(tmp_path).test_client()
    with c2.session_transaction() as sessao:
        sessao["cliente_id"] = cid
    pagina = html(c2.get(f"/livros/{HORA}"))
    assert pagina.index("Livraria Pinheiros") < pagina.index("Livraria Paulista")

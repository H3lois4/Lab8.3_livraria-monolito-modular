"""Cada módulo testado pela sua API pública, como se fosse um serviço."""
import pytest

from app import montar_modulos

DOM, HORA = "9788535902775", "9788501114775"


@pytest.fixture
def m(tmp_path):
    return montar_modulos(tmp_path)


# ----- Catálogo -----

def test_busca_por_titulo_sem_acentos(m):
    assert [l.titulo for l in m["catalogo"].api.buscar("memorias")] == ["Memórias Póstumas de Brás Cubas"]


def test_busca_por_autor(m):
    assert [l.titulo for l in m["catalogo"].api.buscar("machado")] == \
        ["Dom Casmurro", "Memórias Póstumas de Brás Cubas"]


def test_preco(m):
    assert m["catalogo"].api.obter(DOM).preco == 29.90


def test_livro_inexistente(m):
    with pytest.raises(Exception, match="Livro não encontrado"):
        m["catalogo"].api.obter("000")


# ----- Lojas e Estoque -----

def test_estoque_por_loja(m):
    itens = {i["loja"].id: i for i in m["lojas_estoque"].api.disponibilidade(DOM)}
    assert itens["paulista"]["quantidade"] == 3 and not itens["pinheiros"]["disponivel"]


def test_sem_favorita_ordem_alfabetica(m):
    assert m["lojas_estoque"].api.disponibilidade(HORA)[0]["loja"].id == "paulista"


def test_favorita_primeiro(m):
    itens = m["lojas_estoque"].api.disponibilidade(HORA, "pinheiros")
    assert itens[0]["loja"].id == "pinheiros" and itens[0]["favorita"]


def test_loja_existe(m):
    assert m["lojas_estoque"].api.loja_existe("paulista")
    assert not m["lojas_estoque"].api.loja_existe("centro")


# ----- Clientes (conversa com Lojas e Estoque pela API) -----

def test_definir_favorita(m):
    assert m["clientes"].api.definir_loja_favorita("ana", "pinheiros") == "Livraria Pinheiros"
    assert m["clientes"].api.loja_favorita("ana") == "pinheiros"
    assert m["clientes"].api.loja_favorita("bia") is None


def test_favorita_inexistente(m):
    with pytest.raises(Exception, match="Loja não encontrada"):
        m["clientes"].api.definir_loja_favorita("ana", "centro")


# ----- Cada módulo tem seus próprios dados -----

def test_cada_modulo_grava_na_propria_pasta(m, tmp_path):
    m["clientes"].api.definir_loja_favorita("ana", "paulista")
    assert (tmp_path / "catalogo" / "livros.txt").exists()
    assert (tmp_path / "lojas_estoque" / "estoque.txt").exists()
    assert (tmp_path / "clientes" / "preferencias.txt").read_text(encoding="utf-8") == "ana|paulista\n"

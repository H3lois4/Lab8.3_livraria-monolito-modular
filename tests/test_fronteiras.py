"""Regra do monolito modular: um módulo só pode usar outro pela API pública
(o pacote raiz, ex.: `from modulos import clientes`), nunca pelos arquivos internos."""
import ast
import pathlib

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MODULOS = ["catalogo", "lojas_estoque", "clientes"]


def importacoes(modulo):
    encontrados = []
    for arquivo in (RAIZ / "modulos" / modulo).rglob("*.py"):
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            if isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
                encontrados.append(no.module)
            elif isinstance(no, ast.Import):
                encontrados += [a.name for a in no.names]
    return encontrados


@pytest.mark.parametrize("modulo", MODULOS)
def test_nao_acessa_internos_de_outro_modulo(modulo):
    proibidos = [i for i in importacoes(modulo)
                 if i.startswith("modulos.") and i.split(".")[1] != modulo and i.count(".") > 1]
    assert proibidos == []


@pytest.mark.parametrize("modulo", MODULOS)
def test_nao_depende_do_app_nem_do_shell(modulo):
    assert not {i.split(".")[0] for i in importacoes(modulo)} & {"app", "shell"}


@pytest.mark.parametrize("modulo", MODULOS)
def test_api_publica_declarada(modulo):
    pacote = __import__(f"modulos.{modulo}", fromlist=["__all__"])
    assert "criar_modulo" in pacote.__all__

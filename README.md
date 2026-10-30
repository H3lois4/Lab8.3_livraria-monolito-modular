# Livraria – Monolito Modular

MVP da livraria refatorado para uma **arquitetura monolítica modular**, baseada no diagrama
de microsserviços do exercício 8.2. Cada microsserviço virou um **módulo** dentro de uma única
aplicação Flask: um só processo e um só deploy, mas com fronteiras bem definidas.

## Do diagrama de microsserviços para os módulos

| Diagrama 8.2 | Monolito modular | Dados próprios |
|---|---|---|
| Shell do app | `shell/` (layout, menu e estilos comuns) | – |
| Micro-frontends | telas dentro de cada módulo (`modulos/*/templates/`) | – |
| API Gateway | `app.py` (um único Flask que registra as rotas de cada módulo) | – |
| Serviço de Catálogo | `modulos/catalogo/` | `data/catalogo/livros.txt` |
| Serviço de Lojas e Estoque | `modulos/lojas_estoque/` | `data/lojas_estoque/lojas.txt`, `estoque.txt` |
| Serviço de Clientes | `modulos/clientes/` | `data/clientes/preferencias.txt` |
| Serviço de Pedidos e fila de eventos | fora do MVP | – |

## Estrutura de um módulo

```
modulos/lojas_estoque/
├── __init__.py      # API pública: o único ponto que outros módulos podem importar
├── modulo.py        # LojasEstoqueAPI (contrato) e criar_modulo()
├── dominio.py       # entidades do módulo
├── repositorio.py   # dados próprios (pasta data/lojas_estoque/)
├── servico.py       # regras do módulo
├── rotas.py         # rotas HTTP do módulo
└── templates/       # telas do módulo (o "micro-frontend")
```

## Regras das fronteiras

1. Um módulo **nunca** acessa os arquivos internos de outro; usa só a API pública
   (ex.: `ClientesAPI.loja_favorita`, `LojasEstoqueAPI.disponibilidade`).
2. Cada módulo lê e grava **apenas a sua pasta de dados**, como um banco por serviço.
3. As dependências entre módulos são injetadas em `app.py`.

As regras 1 e 3 são verificadas automaticamente em `tests/test_fronteiras.py`.

Como as fronteiras já existem, qualquer módulo pode virar um microsserviço de verdade
depois: basta trocar a chamada à API Python por uma chamada HTTP.

## Funcionalidades (MVP)

- Consultar o estoque do livro em cada loja (Catálogo + Lojas e Estoque)
- Ver o preço praticado (Catálogo)
- Ver horário e endereço das lojas (Lojas e Estoque)
- Escolher loja favorita, que aparece primeiro (Clientes)

## Como rodar

```bash
pip install -r requirements.txt
pytest -v        # testes por módulo, web e de fronteiras
python app.py    # http://localhost:5000
```

## Deploy no Azure App Service

A aplicação roda no Azure com Gunicorn (`wsgi.py`). Configurações usadas:

| Configuração | Valor |
|---|---|
| Comando de inicialização | `gunicorn --bind=0.0.0.0 --timeout 600 wsgi:app` |
| `PASTA_DADOS` | `/home/data` (pasta persistente do App Service) |
| `SECRET_KEY` | uma chave secreta qualquer |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` (instala o `requirements.txt` no deploy) |

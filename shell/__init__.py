"""Shell do app (equivale ao "Shell do app" do diagrama): layout, menu e estilos comuns.
Cada módulo traz suas próprias telas e as encaixa neste layout (base.html)."""
from pathlib import Path

PASTA_TEMPLATES = Path(__file__).parent / "templates"
PASTA_ESTATICOS = Path(__file__).parent / "static"

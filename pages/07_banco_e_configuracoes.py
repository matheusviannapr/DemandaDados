from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[1] / "app" / "pages" / "07_banco_e_configuracoes.py"))

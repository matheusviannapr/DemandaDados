from __future__ import annotations

import runpy
from pathlib import Path

import streamlit as st

from app.db.database import get_engine
from app.db.repositories import Repository

st.set_page_config(page_title="Demanda e Dádio", page_icon="📈", layout="wide")

if "repo" not in st.session_state:
    st.session_state.repo = Repository(get_engine())

PAGES = {
    "🏠 Início": None,
    "1) Upload e cenário": "01_upload_e_cenario.py",
    "2) Equipamentos": "02_equipamentos.py",
    "3) Perfis": "03_perfis.py",
    "4) Sazonalidade": "04_sazonalidade.py",
    "5) Simulação": "05_simulacao.py",
    "6) Resultados": "06_resultados.py",
    "7) Banco e configurações": "07_banco_e_configuracoes.py",
}

st.sidebar.title("Navegação")
selected_page = st.sidebar.radio("Ir para", list(PAGES.keys()), index=0)

st.title("Demanda e Dádio")
st.write("Plataforma de modelagem e simulação de demanda elétrica.")

if PAGES[selected_page] is None:
    st.info("Escolha uma etapa no menu da barra lateral para continuar o fluxo.")
else:
    target = Path(__file__).resolve().parent / "app" / "pages" / PAGES[selected_page]
    runpy.run_path(str(target))

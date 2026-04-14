from __future__ import annotations

import streamlit as st

from app.db.database import get_engine
from app.db.repositories import Repository

st.set_page_config(page_title="Demanda e Dádio", page_icon="📈", layout="wide")

if "repo" not in st.session_state:
    st.session_state.repo = Repository(get_engine())

st.title("Demanda e Dádio")
st.write("Plataforma de modelagem e simulação de demanda elétrica.")
st.info("Se o menu lateral não aparecer, use os botões abaixo para abrir cada etapa.")

st.subheader("Fluxo rápido")
col1, col2, col3 = st.columns(3)
col1.page_link("pages/01_upload_e_cenario.py", label="1) Upload e cenário", icon="📥")
col1.page_link("pages/02_equipamentos.py", label="2) Equipamentos", icon="🧰")
col2.page_link("pages/03_perfis.py", label="3) Perfis", icon="🗂️")
col2.page_link("pages/04_sazonalidade.py", label="4) Sazonalidade", icon="🌦️")
col3.page_link("pages/05_simulacao.py", label="5) Simulação", icon="⚙️")
col3.page_link("pages/06_resultados.py", label="6) Resultados", icon="📊")

st.page_link("pages/07_banco_e_configuracoes.py", label="7) Banco e configurações", icon="🗄️")

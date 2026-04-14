from __future__ import annotations

import streamlit as st

from app.db.database import get_engine
from app.db.repositories import Repository

st.set_page_config(page_title="Demanda e Dádio", page_icon="📈", layout="wide")

if "repo" not in st.session_state:
    st.session_state.repo = Repository(get_engine())

st.title("Demanda e Dádio")
st.write("Plataforma de modelagem e simulação de demanda elétrica.")
st.info("Use o menu lateral para seguir o fluxo: cenário → equipamentos → perfis → sazonalidade → simulação → resultados.")

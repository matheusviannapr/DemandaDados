from __future__ import annotations

import streamlit as st


def cenario_form() -> tuple[str, str, bool, bool]:
    with st.form("cenario_form"):
        nome = st.text_input("Nome do cenário")
        descricao = st.text_area("Descrição")
        col1, col2 = st.columns(2)
        importar = col1.form_submit_button("Importar planilha")
        vazio = col2.form_submit_button("Criar cenário vazio")
    return nome, descricao, importar, vazio

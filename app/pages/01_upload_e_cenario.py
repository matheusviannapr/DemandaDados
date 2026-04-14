from __future__ import annotations

import streamlit as st

from app.core.parser_excel import parse_excel_to_equipamentos
from app.ui.forms import cenario_form

st.header("Upload e cenário")
repo = st.session_state.repo
uploaded = st.file_uploader("Planilha Excel", type=["xlsx", "xls"])

nome, descricao, importar, vazio = cenario_form()

if vazio and nome:
    cenario_id = repo.criar_cenario(nome, descricao)
    st.session_state.cenario_id = cenario_id
    st.success(f"Cenário vazio criado: #{cenario_id}")

if importar and nome and uploaded:
    equipamentos, erros = parse_excel_to_equipamentos(uploaded.read())
    if erros:
        for erro in erros:
            st.error(erro)
    else:
        cenario_id = repo.criar_cenario(nome, descricao)
        repo.inserir_equipamentos(cenario_id, equipamentos)
        st.session_state.cenario_id = cenario_id
        st.success(f"Importação concluída no cenário #{cenario_id}")

if st.session_state.get("cenario_id"):
    rows = repo.equipamentos_do_cenario(st.session_state["cenario_id"])
    potencia = sum(r["potencia_kw"] * r["quantidade"] for r in rows)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ambientes", len(set(r["ambiente"] for r in rows)))
    c2.metric("Equipamentos", len(rows))
    c3.metric("Potência instalada (kW)", f"{potencia:,.2f}")

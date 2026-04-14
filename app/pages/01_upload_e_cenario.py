from __future__ import annotations

import pandas as pd
import streamlit as st

from app.core.default_model import criar_modelo_padrao, texto_modelo_padrao
from app.core.parser_excel import parse_excel_to_equipamentos
from app.ui.forms import cenario_form

st.header("Upload e cenário")
repo = st.session_state.repo
uploaded = st.file_uploader("Planilha Excel", type=["xlsx", "xls"])

with st.expander("Modelo padrão do sistema", expanded=False):
    st.write(texto_modelo_padrao())
    demo_df = pd.DataFrame([
        {
            "ambiente": eq.ambiente,
            "equipamento": eq.nome,
            "tipo": eq.tipo_equipamento,
            "potencia_kw": eq.potencia_kw,
            "quantidade": eq.quantidade,
        }
        for eq in criar_modelo_padrao()
    ])
    st.dataframe(demo_df, use_container_width=True)

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

with st.form("modelo_padrao_form"):
    st.caption("Sem planilha? Crie automaticamente um cenário de exemplo para aprender o software.")
    nome_demo = st.text_input("Nome do cenário de exemplo", value="Modelo padrão - Hotel")
    desc_demo = st.text_input("Descrição", value="Cenário de referência para entender o fluxo")
    criar_demo = st.form_submit_button("Criar cenário com modelo padrão")

if criar_demo:
    equipamentos_demo = criar_modelo_padrao()
    cenario_id = repo.criar_cenario(nome_demo, desc_demo)
    repo.inserir_equipamentos(cenario_id, equipamentos_demo)
    st.session_state.cenario_id = cenario_id
    st.success(f"Modelo padrão criado no cenário #{cenario_id}.")

if st.session_state.get("cenario_id"):
    rows = repo.equipamentos_do_cenario(st.session_state["cenario_id"])
    potencia = sum(r["potencia_kw"] * r["quantidade"] for r in rows)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ambientes", len(set(r["ambiente"] for r in rows)))
    c2.metric("Equipamentos", len(rows))
    c3.metric("Potência instalada (kW)", f"{potencia:,.2f}")

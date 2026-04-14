from __future__ import annotations

import pandas as pd
import streamlit as st

from app.core.models import PerfilSazonal

st.header("Sazonalidade")
repo = st.session_state.repo

with st.form("sazonal_form"):
    nome = st.text_input("Nome do perfil sazonal")
    tipo = st.text_input("Tipo de equipamento")
    descricao = st.text_area("Descrição")

    st.write("Fatores por estação")
    estacoes = ["verao", "outono", "inverno", "primavera"]
    fatores_estacao: dict[str, dict[str, float]] = {}
    for est in estacoes:
        cols = st.columns(4)
        fatores_estacao[est] = {
            "probabilidade": cols[0].number_input(f"{est} prob", value=1.0, key=f"{est}_prob"),
            "duracao": cols[1].number_input(f"{est} dur", value=1.0, key=f"{est}_dur"),
            "fator_carga": cols[2].number_input(f"{est} fc", value=1.0, key=f"{est}_fc"),
            "ciclos": cols[3].number_input(f"{est} ciclos", value=1.0, key=f"{est}_cic"),
        }

    salvar = st.form_submit_button("Salvar perfil sazonal")

if salvar and nome:
    perfil = PerfilSazonal(nome=nome, tipo_equipamento=tipo, descricao=descricao, fatores_estacao=fatores_estacao)
    repo.salvar_perfil_sazonal(perfil)
    st.success("Perfil sazonal salvo.")

rows = repo.listar_perfis_sazonais()
st.subheader("Perfis sazonais cadastrados")
st.dataframe(rows, use_container_width=True)

if rows:
    payload = pd.DataFrame(rows).iloc[0]["fatores_json"]
    st.caption("Exemplo de payload sazonal (JSON):")
    st.code(payload, language="json")

from __future__ import annotations

import streamlit as st

from app.core.models import JanelaUso, PerfilConsumo

st.header("Perfis de consumo")
repo = st.session_state.repo

with st.form("perfil_consumo_form"):
    nome = st.text_input("Nome do perfil")
    tipo = st.text_input("Tipo de equipamento")
    descricao = st.text_area("Descrição")
    c1, c2, c3, c4 = st.columns(4)
    prob = c1.number_input("Probabilidade-base", min_value=0.0, max_value=1.0, value=0.5)
    dur = c2.number_input("Duração-base (h)", min_value=0.1, value=1.0)
    ciclos = c3.number_input("Ciclos/dia", min_value=0.1, value=1.0)
    fc = c4.number_input("Fator de carga", min_value=0.1, value=1.0)
    j1, j2 = st.columns(2)
    inicio = j1.slider("Início janela", 0, 23, 8)
    fim = j2.slider("Fim janela", 0, 23, 18)
    salvar = st.form_submit_button("Salvar perfil")

if salvar and nome:
    perfil = PerfilConsumo(
        nome=nome,
        tipo_equipamento=tipo,
        descricao=descricao,
        probabilidade_base=prob,
        duracao_base_h=dur,
        ciclos_por_dia=ciclos,
        fator_carga=fc,
        janelas_padrao=[JanelaUso(inicio_hora=inicio, fim_hora=fim)],
    )
    repo.salvar_perfil_consumo(perfil)
    st.success("Perfil salvo.")

st.subheader("Biblioteca de perfis")
st.dataframe(repo.listar_perfis_consumo(), use_container_width=True)

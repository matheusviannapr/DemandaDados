from __future__ import annotations

import streamlit as st

st.header("Banco e configurações")
repo = st.session_state.repo

st.subheader("Cenários")
st.dataframe(repo.listar_cenarios(), use_container_width=True)

st.subheader("Perfis")
st.dataframe(repo.listar_perfis_consumo(), use_container_width=True)

st.subheader("Perfis sazonais")
st.dataframe(repo.listar_perfis_sazonais(), use_container_width=True)

st.info("MVP: exportação/importação e duplicação de cenário planejadas para próxima iteração.")

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.ui.tables import editable_dataframe

st.header("Equipamentos")
repo = st.session_state.repo
cenario_id = st.session_state.get("cenario_id")
if not cenario_id:
    st.warning("Crie ou importe um cenário primeiro.")
    st.stop()

rows = repo.equipamentos_do_cenario(cenario_id)
df = pd.DataFrame(rows)
if df.empty:
    st.info("Nenhum equipamento cadastrado.")
    st.stop()

ambientes = ["Todos"] + sorted(df["ambiente"].unique().tolist())
ambiente_sel = st.selectbox("Filtrar ambiente", ambientes)
if ambiente_sel != "Todos":
    df = df[df["ambiente"] == ambiente_sel]

edited = editable_dataframe(df, "equipamentos_editor")
st.caption("Edição inline disponível para revisão rápida (persistência detalhada em evolução no MVP).")
st.dataframe(edited, use_container_width=True)

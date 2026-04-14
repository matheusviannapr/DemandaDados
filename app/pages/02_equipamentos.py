from __future__ import annotations

import pandas as pd
import streamlit as st

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

st.caption("Edite os parâmetros por equipamento, inclusive janela de uso (início/fim, prioridade e tipo).")

colunas_editaveis = [
    "id", "ambiente", "nome", "tipo_equipamento", "potencia_kw", "quantidade",
    "prob_uso_base", "duracao_base_h", "ciclos_por_dia_base", "fator_carga_base",
    "janela_inicio_hora", "janela_fim_hora", "janela_prioridade", "janela_tipo",
]

with st.form("equipamentos_form"):
    edited = st.data_editor(
        df[colunas_editaveis],
        use_container_width=True,
        num_rows="fixed",
        disabled=["id", "ambiente"],
        column_config={
            "janela_inicio_hora": st.column_config.NumberColumn(min_value=0, max_value=23, step=1),
            "janela_fim_hora": st.column_config.NumberColumn(min_value=0, max_value=23, step=1),
            "janela_prioridade": st.column_config.NumberColumn(min_value=1, max_value=10, step=1),
            "janela_tipo": st.column_config.SelectboxColumn(options=["preferencial", "flexivel", "restrita"]),
        },
        key="equipamentos_editor",
    )
    salvar = st.form_submit_button("Salvar alterações dos equipamentos")

if salvar:
    inconsistencias = edited[edited["janela_inicio_hora"] > edited["janela_fim_hora"]]
    if not inconsistencias.empty:
        st.error("Existem equipamentos com janela de início maior que o fim. Ajuste e salve novamente.")
    else:
        repo.atualizar_equipamentos(edited.to_dict(orient="records"))
        st.success("Alterações salvas com sucesso (incluindo janelas por equipamento).")

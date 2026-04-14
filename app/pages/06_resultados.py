from __future__ import annotations

import json

import streamlit as st

from app.ui.charts import histogram, line_chart
from app.ui.components import metric_cards
from app.utils.formatters import kw, kwh

st.header("Resultados")
repo = st.session_state.repo
cenario_id = st.session_state.get("cenario_id")
if not cenario_id:
    st.warning("Sem cenário ativo.")
    st.stop()

row = repo.ultimo_resultado(cenario_id)
if not row:
    st.info("Sem resultados salvos ainda.")
    st.stop()

payload = json.loads(row["resultados_json"])
metric_cards(
    {
        "Pico": kw(row["demanda_pico_kw"]),
        "Média": kw(row["demanda_media_kw"]),
        "Energia": kwh(row["energia_kwh_estimada"]),
        "Mês crítico": str(row["mes_critico"]),
    }
)

st.subheader("Curva média de demanda")
line_chart(payload["curva_media_kw"], "kW")

st.subheader("Distribuição dos picos")
histogram(payload["picos_iteracao_kw"])

c1, c2 = st.columns(2)
c1.write("Contribuição por ambiente")
c1.dataframe(payload["contribuicao_ambiente_kw"])
c2.write("Contribuição por tipo")
c2.dataframe(payload["contribuicao_tipo_kw"])

from __future__ import annotations

import json

import streamlit as st

from app.core.models import Equipamento, JanelaUso, ParametrosSimulacao, PerfilSazonal
from app.core.simulation import simular_mes
from app.db.repositories import Repository

st.header("Simulação")
repo: Repository = st.session_state.repo
cenario_id = st.session_state.get("cenario_id")
if not cenario_id:
    st.warning("Crie/importe um cenário antes de simular.")
    st.stop()

rows = repo.equipamentos_do_cenario(cenario_id)
if not rows:
    st.warning("Cenário sem equipamentos.")
    st.stop()

with st.form("sim_form"):
    mes = st.selectbox("Mês", options=list(range(1, 13)), index=0)
    it = st.slider("Iterações", min_value=200, max_value=5000, value=3000, step=100)
    passo = st.selectbox("Passo temporal (min)", [5, 10, 15, 30], index=2)
    seed = st.number_input("Seed (opcional, -1 = aleatório)", value=-1)
    executar = st.form_submit_button("Rodar simulação")

if executar:
    equipamentos = [
        Equipamento(
            nome=r["nome"], tipo_equipamento=r["tipo_equipamento"], potencia_kw=r["potencia_kw"],
            quantidade=r["quantidade"], ambiente=r["ambiente"], prob_uso_base=r["prob_uso_base"],
            duracao_base_h=r["duracao_base_h"], ciclos_por_dia_base=r["ciclos_por_dia_base"],
            fator_carga_base=r["fator_carga_base"], janelas_uso=[JanelaUso(8, 18)],
        )
        for r in rows
    ]

    perfis_rows = repo.listar_perfis_sazonais()
    perfis = {}
    for p in perfis_rows:
        data = json.loads(p["fatores_json"])
        perfis[p["tipo_equipamento"]] = PerfilSazonal(
            nome=p["nome"],
            tipo_equipamento=p["tipo_equipamento"],
            descricao=p["descricao"],
            fatores_estacao=data.get("fatores_estacao", {}),
            fatores_mes={int(k): v for k, v in data.get("fatores_mes", {}).items()},
        )

    params = ParametrosSimulacao(meses=[mes], numero_iteracoes=it, passo_temporal_min=passo, seed=None if seed < 0 else int(seed))
    with st.spinner("Rodando simulação..."):
        resultado = simular_mes(equipamentos, perfis, params, mes)
    sim_id = repo.salvar_resultado(cenario_id, f"Simulação mês {mes}", mes, it, passo, None if seed < 0 else int(seed), resultado)
    st.session_state.simulacao_id = sim_id
    st.success(f"Simulação concluída e salva (id={sim_id}).")

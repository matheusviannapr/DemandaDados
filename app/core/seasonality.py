from __future__ import annotations

from app.core.models import Equipamento, PerfilSazonal

ESTACAO_POR_MES = {
    1: "verao", 2: "verao", 3: "outono", 4: "outono", 5: "outono",
    6: "inverno", 7: "inverno", 8: "inverno", 9: "primavera", 10: "primavera",
    11: "primavera", 12: "verao",
}


def fator(fatores: dict[str, float], chave: str) -> float:
    return float(fatores.get(chave, 1.0))


def ajustar_parametros(equipamento: Equipamento, perfil_sazonal: PerfilSazonal | None, mes: int) -> dict[str, float]:
    estacao = ESTACAO_POR_MES[mes]
    fatores_estacao = (perfil_sazonal.fatores_estacao.get(estacao, {}) if perfil_sazonal else {})
    fatores_mes = (perfil_sazonal.fatores_mes.get(mes, {}) if perfil_sazonal else {})

    prob = equipamento.prob_uso_base * fator(fatores_estacao, "probabilidade") * fator(fatores_mes, "probabilidade")
    dur = equipamento.duracao_base_h * fator(fatores_estacao, "duracao") * fator(fatores_mes, "duracao")
    fc = equipamento.fator_carga_base * fator(fatores_estacao, "fator_carga") * fator(fatores_mes, "fator_carga")
    ciclos = equipamento.ciclos_por_dia_base * fator(fatores_estacao, "ciclos") * fator(fatores_mes, "ciclos")

    return {
        "prob": max(0.0, min(1.0, prob)),
        "dur_h": max(0.0, dur),
        "fc": max(0.0, fc),
        "ciclos": max(0.0, ciclos),
    }

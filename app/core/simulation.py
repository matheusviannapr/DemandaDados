from __future__ import annotations

import numpy as np

from app.core.models import Equipamento, ParametrosSimulacao, PerfilSazonal, ResultadoSimulacao
from app.core.seasonality import ajustar_parametros


def _marca_janela_mask(passos_dia: int, janela_inicio: int, janela_fim: int, passo_min: int) -> np.ndarray:
    mask = np.zeros(passos_dia, dtype=bool)
    i0 = int((janela_inicio * 60) / passo_min)
    i1 = int((janela_fim * 60) / passo_min)
    mask[max(i0, 0): min(i1 + 1, passos_dia)] = True
    return mask


def simular_mes(
    equipamentos: list[Equipamento],
    perfis_sazonais_por_tipo: dict[str, PerfilSazonal],
    parametros: ParametrosSimulacao,
    mes: int,
) -> ResultadoSimulacao:
    rng = np.random.default_rng(parametros.seed if parametros.seed is not None else None)
    passos_dia = int(24 * 60 / parametros.passo_temporal_min)
    cargas_iter = np.zeros((parametros.numero_iteracoes, passos_dia), dtype=np.float32)
    amb_idx: dict[str, float] = {}
    tipo_idx: dict[str, float] = {}

    for eq in equipamentos:
        sazonal = perfis_sazonais_por_tipo.get(eq.tipo_equipamento)
        p = ajustar_parametros(eq, sazonal, mes)
        ciclos = max(1, int(round(p["ciclos"])))
        dur_steps = max(1, int(round((p["dur_h"] * 60) / parametros.passo_temporal_min)))
        janela = eq.janelas_uso[0] if eq.janelas_uso else None
        janela_mask = _marca_janela_mask(passos_dia, janela.inicio_hora if janela else 0, janela.fim_hora if janela else 23, parametros.passo_temporal_min)
        candidatos = np.where(janela_mask)[0]
        if len(candidatos) == 0:
            continue
        potencia = eq.potencia_kw * eq.quantidade * p["fc"]

        ativacoes = rng.random((parametros.numero_iteracoes, ciclos)) < p["prob"]
        starts = rng.choice(candidatos, size=(parametros.numero_iteracoes, ciclos), replace=True)

        for c in range(ciclos):
            ativos = np.where(ativacoes[:, c])[0]
            if ativos.size == 0:
                continue
            s = starts[ativos, c]
            for offset in range(dur_steps):
                idx = np.minimum(s + offset, passos_dia - 1)
                cargas_iter[ativos, idx] += potencia

        amb_idx[eq.ambiente] = amb_idx.get(eq.ambiente, 0.0) + potencia
        tipo_idx[eq.tipo_equipamento] = tipo_idx.get(eq.tipo_equipamento, 0.0) + potencia

    curva_media = cargas_iter.mean(axis=0)
    picos = cargas_iter.max(axis=1)
    energia = float(curva_media.sum() * (parametros.passo_temporal_min / 60.0))

    return ResultadoSimulacao(
        mes=mes,
        demanda_pico_kw=float(picos.max()),
        demanda_media_kw=float(curva_media.mean()),
        energia_kwh_estimada=energia,
        curva_media_kw=curva_media.tolist(),
        picos_iteracao_kw=picos.tolist(),
        contribuicao_ambiente_kw=amb_idx,
        contribuicao_tipo_kw=tipo_idx,
    )

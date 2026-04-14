from __future__ import annotations

from app.core.models import ResultadoSimulacao


def consolidar_resultados(resultados: list[ResultadoSimulacao]) -> dict[str, float | int]:
    if not resultados:
        return {}
    mes_critico = max(resultados, key=lambda r: r.demanda_pico_kw).mes
    return {
        "pico_max_kw": max(r.demanda_pico_kw for r in resultados),
        "media_kw": sum(r.demanda_media_kw for r in resultados) / len(resultados),
        "energia_total_kwh": sum(r.energia_kwh_estimada for r in resultados),
        "mes_critico": mes_critico,
    }

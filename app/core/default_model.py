from __future__ import annotations

from app.core.models import Equipamento, JanelaUso


def criar_modelo_padrao() -> list[Equipamento]:
    """Modelo didático padrão para o usuário entender rapidamente o fluxo."""
    return [
        Equipamento(
            nome="Ar-condicionado quarto",
            tipo_equipamento="ar_condicionado",
            potencia_kw=1.5,
            quantidade=20,
            ambiente="Quartos",
            prob_uso_base=0.7,
            duracao_base_h=8.0,
            ciclos_por_dia_base=1.2,
            fator_carga_base=0.85,
            janelas_uso=[JanelaUso(10, 23)],
            observacoes="Modelo padrão para resfriamento em hotel",
        ),
        Equipamento(
            nome="Iluminação corredor",
            tipo_equipamento="iluminacao",
            potencia_kw=0.08,
            quantidade=150,
            ambiente="Corredores",
            prob_uso_base=0.95,
            duracao_base_h=10.0,
            ciclos_por_dia_base=1.0,
            fator_carga_base=1.0,
            janelas_uso=[JanelaUso(18, 23)],
            observacoes="Iluminação principal de circulação",
        ),
        Equipamento(
            nome="Bomba de água",
            tipo_equipamento="bomba",
            potencia_kw=3.0,
            quantidade=2,
            ambiente="Casa de máquinas",
            prob_uso_base=0.6,
            duracao_base_h=4.0,
            ciclos_por_dia_base=2.0,
            fator_carga_base=0.9,
            janelas_uso=[JanelaUso(6, 22)],
            observacoes="Ciclos distribuídos ao longo do dia",
        ),
    ]


def texto_modelo_padrao() -> str:
    return (
        "Modelo padrão: cenário de hotel com 3 ambientes, cobrindo cargas de climatização, "
        "iluminação e utilidades. Use para testar o fluxo completo sem planilha."
    )

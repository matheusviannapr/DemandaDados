from __future__ import annotations

from io import BytesIO
import pandas as pd

from app.core.models import Equipamento, JanelaUso
from app.core.validators import normalizar_colunas, validar_aba

MAPEAMENTO_COLUNAS = {
    "nome": ["nome", "equipamento"],
    "tipo_equipamento": ["tipo_equipamento", "tipo"],
    "potencia_kw": ["potencia_kw", "potencia", "potencia_kW"],
    "quantidade": ["quantidade", "qtd"],
    "prob_uso_base": ["prob_uso_base", "probabilidade"],
    "duracao_base_h": ["duracao_base_h", "duracao_h", "duracao"],
    "ciclos_por_dia_base": ["ciclos_por_dia_base", "ciclos_por_dia", "ciclos"],
    "fator_carga_base": ["fator_carga_base", "fator_carga"],
    "inicio_hora": ["inicio_hora", "janela_inicio"],
    "fim_hora": ["fim_hora", "janela_fim"],
}


def _mapear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    normalized = normalizar_colunas(df)
    rename: dict[str, str] = {}
    for alvo, aliases in MAPEAMENTO_COLUNAS.items():
        for alias in aliases:
            if alias.lower() in normalized.columns:
                rename[alias.lower()] = alvo
                break
    return normalized.rename(columns=rename)


def parse_excel_to_equipamentos(file_bytes: bytes) -> tuple[list[Equipamento], list[str]]:
    xls = pd.ExcelFile(BytesIO(file_bytes))
    equipamentos: list[Equipamento] = []
    erros: list[str] = []

    for aba in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=aba)
        if df.empty:
            continue
        df = _mapear_colunas(df)
        erros.extend(validar_aba(df, aba))
        if erros:
            continue

        for _, row in df.fillna(0).iterrows():
            janela = JanelaUso(
                inicio_hora=int(row.get("inicio_hora", 0)),
                fim_hora=int(row.get("fim_hora", 23)),
            )
            equipamentos.append(
                Equipamento(
                    nome=str(row["nome"]),
                    tipo_equipamento=str(row["tipo_equipamento"]),
                    potencia_kw=float(row["potencia_kw"]),
                    quantidade=int(row.get("quantidade", 1)),
                    ambiente=aba,
                    prob_uso_base=float(row["prob_uso_base"]),
                    duracao_base_h=float(row["duracao_base_h"]),
                    ciclos_por_dia_base=float(row["ciclos_por_dia_base"]),
                    fator_carga_base=float(row.get("fator_carga_base", 1.0)),
                    janelas_uso=[janela],
                )
            )

    return equipamentos, erros

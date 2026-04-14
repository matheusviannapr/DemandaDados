from __future__ import annotations

import pandas as pd

COLUNAS_OBRIGATORIAS = {
    "nome",
    "tipo_equipamento",
    "potencia_kw",
    "quantidade",
    "prob_uso_base",
    "duracao_base_h",
    "ciclos_por_dia_base",
}


class ValidationError(Exception):
    pass


def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {col: col.strip().lower() for col in df.columns}
    return df.rename(columns=renamed)


def validar_aba(df: pd.DataFrame, aba: str) -> list[str]:
    erros: list[str] = []
    colunas = set(df.columns)
    faltando = COLUNAS_OBRIGATORIAS - colunas
    if faltando:
        erros.append(f"Aba '{aba}' sem colunas obrigatórias: {', '.join(sorted(faltando))}")

    if "potencia_kw" in df.columns and (pd.to_numeric(df["potencia_kw"], errors="coerce") < 0).any():
        erros.append(f"Aba '{aba}' possui potencia_kw negativa")

    return erros

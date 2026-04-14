from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class JanelaUso:
    inicio_hora: int
    fim_hora: int
    prioridade: int = 1
    tipo_janela: str = "preferencial"


@dataclass(slots=True)
class Equipamento:
    nome: str
    tipo_equipamento: str
    potencia_kw: float
    quantidade: int
    ambiente: str
    prob_uso_base: float
    duracao_base_h: float
    ciclos_por_dia_base: float
    fator_carga_base: float = 1.0
    janelas_uso: list[JanelaUso] = field(default_factory=list)
    observacoes: str = ""


@dataclass(slots=True)
class PerfilConsumo:
    nome: str
    tipo_equipamento: str
    categoria: str = "geral"
    descricao: str = ""
    probabilidade_base: float = 0.5
    duracao_base_h: float = 1.0
    ciclos_por_dia: float = 1.0
    fator_carga: float = 1.0
    janelas_padrao: list[JanelaUso] = field(default_factory=list)


@dataclass(slots=True)
class PerfilSazonal:
    nome: str
    tipo_equipamento: str
    descricao: str = ""
    fatores_estacao: dict[str, dict[str, float]] = field(default_factory=dict)
    fatores_mes: dict[int, dict[str, float]] = field(default_factory=dict)


@dataclass(slots=True)
class ParametrosSimulacao:
    meses: list[int]
    numero_iteracoes: int = 3000
    passo_temporal_min: int = 15
    seed: int | None = None


@dataclass(slots=True)
class ResultadoSimulacao:
    mes: int
    demanda_pico_kw: float
    demanda_media_kw: float
    energia_kwh_estimada: float
    curva_media_kw: list[float]
    picos_iteracao_kw: list[float]
    contribuicao_ambiente_kw: dict[str, float]
    contribuicao_tipo_kw: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

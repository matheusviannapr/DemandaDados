from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.core.models import Equipamento, PerfilConsumo, PerfilSazonal, ResultadoSimulacao


class Repository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def _fetch_all(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        with self.engine.connect() as conn:
            return [dict(row) for row in conn.execute(text(query), params or {}).mappings().all()]

    def _fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        with self.engine.connect() as conn:
            row = conn.execute(text(query), params or {}).mappings().first()
            return dict(row) if row else None

    def criar_cenario(self, nome: str, descricao: str = "") -> int:
        with self.engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO cenarios (nome, descricao) VALUES (:nome, :descricao) RETURNING id"),
                {"nome": nome, "descricao": descricao},
            )
            return int(result.scalar_one())

    def listar_cenarios(self) -> list[dict[str, Any]]:
        return self._fetch_all("SELECT * FROM cenarios ORDER BY atualizado_em DESC")

    def inserir_equipamentos(self, cenario_id: int, equipamentos: list[Equipamento]) -> None:
        with self.engine.begin() as conn:
            ambientes: dict[str, int] = {}
            for eq in equipamentos:
                if eq.ambiente not in ambientes:
                    result_amb = conn.execute(
                        text("INSERT INTO ambientes (cenario_id, nome, tipo_ambiente) VALUES (:cenario_id, :nome, :tipo) RETURNING id"),
                        {"cenario_id": cenario_id, "nome": eq.ambiente, "tipo": "geral"},
                    )
                    ambientes[eq.ambiente] = int(result_amb.scalar_one())

                result_eq = conn.execute(
                    text(
                        """
                        INSERT INTO equipamentos
                        (ambiente_id, nome, tipo_equipamento, potencia_kw, quantidade, prob_uso_base, duracao_base_h,
                         ciclos_por_dia_base, fator_carga_base, observacoes)
                        VALUES (:ambiente_id, :nome, :tipo, :potencia, :quantidade, :prob, :duracao, :ciclos, :fc, :obs)
                        RETURNING id
                        """
                    ),
                    {
                        "ambiente_id": ambientes[eq.ambiente],
                        "nome": eq.nome,
                        "tipo": eq.tipo_equipamento,
                        "potencia": eq.potencia_kw,
                        "quantidade": eq.quantidade,
                        "prob": eq.prob_uso_base,
                        "duracao": eq.duracao_base_h,
                        "ciclos": eq.ciclos_por_dia_base,
                        "fc": eq.fator_carga_base,
                        "obs": eq.observacoes,
                    },
                )
                eq_id = int(result_eq.scalar_one())
                for jan in eq.janelas_uso:
                    conn.execute(
                        text(
                            "INSERT INTO janelas_uso (equipamento_id, inicio_hora, fim_hora, prioridade, tipo_janela) VALUES (:equipamento_id, :inicio, :fim, :prioridade, :tipo)"
                        ),
                        {
                            "equipamento_id": eq_id,
                            "inicio": jan.inicio_hora,
                            "fim": jan.fim_hora,
                            "prioridade": jan.prioridade,
                            "tipo": jan.tipo_janela,
                        },
                    )

    def equipamentos_do_cenario(self, cenario_id: int) -> list[dict[str, Any]]:
        return self._fetch_all(
            """
            SELECT e.id, a.nome as ambiente, e.nome, e.tipo_equipamento, e.potencia_kw, e.quantidade,
                   e.prob_uso_base, e.duracao_base_h, e.ciclos_por_dia_base, e.fator_carga_base
            FROM equipamentos e
            JOIN ambientes a ON a.id = e.ambiente_id
            WHERE a.cenario_id = :cenario_id
            ORDER BY a.nome, e.nome
            """,
            {"cenario_id": cenario_id},
        )

    def salvar_perfil_consumo(self, perfil: PerfilConsumo) -> int:
        payload = json.dumps(asdict(perfil), ensure_ascii=False)
        with self.engine.begin() as conn:
            result = conn.execute(
                text(
                    "INSERT INTO perfis_consumo (nome, tipo_equipamento, categoria, descricao, parametros_json) VALUES (:nome, :tipo, :categoria, :descricao, :payload) RETURNING id"
                ),
                {
                    "nome": perfil.nome,
                    "tipo": perfil.tipo_equipamento,
                    "categoria": perfil.categoria,
                    "descricao": perfil.descricao,
                    "payload": payload,
                },
            )
            return int(result.scalar_one())

    def listar_perfis_consumo(self) -> list[dict[str, Any]]:
        return self._fetch_all("SELECT * FROM perfis_consumo ORDER BY nome")

    def salvar_perfil_sazonal(self, perfil: PerfilSazonal) -> int:
        payload = json.dumps(asdict(perfil), ensure_ascii=False)
        with self.engine.begin() as conn:
            result = conn.execute(
                text(
                    "INSERT INTO perfis_sazonais (nome, tipo_equipamento, descricao, fatores_json) VALUES (:nome, :tipo, :descricao, :payload) RETURNING id"
                ),
                {"nome": perfil.nome, "tipo": perfil.tipo_equipamento, "descricao": perfil.descricao, "payload": payload},
            )
            return int(result.scalar_one())

    def listar_perfis_sazonais(self) -> list[dict[str, Any]]:
        return self._fetch_all("SELECT * FROM perfis_sazonais ORDER BY nome")

    def salvar_resultado(self, cenario_id: int, nome: str, mes: int, numero_iteracoes: int, passo: int, seed: int | None, resultado: ResultadoSimulacao) -> int:
        with self.engine.begin() as conn:
            result_sim = conn.execute(
                text(
                    "INSERT INTO simulacoes (cenario_id, nome, mes_referencia, numero_iteracoes, passo_temporal_min, seed, parametros_json) VALUES (:cenario_id, :nome, :mes_referencia, :iteracoes, :passo, :seed, :params) RETURNING id"
                ),
                {
                    "cenario_id": cenario_id,
                    "nome": nome,
                    "mes_referencia": str(mes),
                    "iteracoes": numero_iteracoes,
                    "passo": passo,
                    "seed": seed,
                    "params": json.dumps({"mes": mes}, ensure_ascii=False),
                },
            )
            sim_id = int(result_sim.scalar_one())
            conn.execute(
                text(
                    "INSERT INTO resultados_simulacao (simulacao_id, demanda_pico_kw, demanda_media_kw, energia_kwh_estimada, mes_critico, resultados_json) VALUES (:simulacao_id, :pico, :media, :energia, :mes_critico, :resultado)"
                ),
                {
                    "simulacao_id": sim_id,
                    "pico": resultado.demanda_pico_kw,
                    "media": resultado.demanda_media_kw,
                    "energia": resultado.energia_kwh_estimada,
                    "mes_critico": resultado.mes,
                    "resultado": json.dumps(resultado.to_dict(), ensure_ascii=False),
                },
            )
            return sim_id

    def ultimo_resultado(self, cenario_id: int) -> dict[str, Any] | None:
        return self._fetch_one(
            """
            SELECT rs.*, s.nome as nome_simulacao
            FROM resultados_simulacao rs
            JOIN simulacoes s ON s.id = rs.simulacao_id
            WHERE s.cenario_id = :cenario_id
            ORDER BY rs.id DESC
            LIMIT 1
            """,
            {"cenario_id": cenario_id},
        )

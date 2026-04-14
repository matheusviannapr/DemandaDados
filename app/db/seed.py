from __future__ import annotations

from app.core.models import Equipamento, JanelaUso, PerfilConsumo, PerfilSazonal
from app.db.database import get_engine
from app.db.repositories import Repository


def seed() -> None:
    repo = Repository(get_engine())
    cenario_id = repo.criar_cenario("Hotel Exemplo", "Seed inicial")
    repo.inserir_equipamentos(
        cenario_id,
        [
            Equipamento("Ar Condicionado 1", "ar_condicionado", 1.5, 20, "Quartos", 0.75, 8, 1.2, 0.85, [JanelaUso(10, 23)]),
            Equipamento("Iluminação Corredor", "iluminacao", 0.08, 150, "Corredores", 0.95, 10, 1.0, 1.0, [JanelaUso(18, 23)]),
        ],
    )
    repo.salvar_perfil_consumo(PerfilConsumo(nome="Ar-condicionado hotel", tipo_equipamento="ar_condicionado", probabilidade_base=0.75))
    repo.salvar_perfil_sazonal(
        PerfilSazonal(
            nome="AC Sazonal", tipo_equipamento="ar_condicionado",
            fatores_estacao={"verao": {"probabilidade": 1.3, "duracao": 1.2}, "inverno": {"probabilidade": 0.5, "duracao": 0.7}},
        )
    )


if __name__ == "__main__":
    seed()

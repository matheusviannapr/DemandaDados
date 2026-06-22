import numpy as np

from monte_carlo_hotel_app_final_v3 import (
    parse_time, parse_intervalo_fixo, gerar_intervalo_uso, Equipamento,
    calcular_indicadores_ponta_fora,
)


def test_parse_time_hh_mm():
    assert parse_time("08:30") == 510


def test_parse_intervalo_fixo_simples():
    assert parse_intervalo_fixo("08:00 as 18:00") == [(480, 1080)]


def test_gerar_intervalo_uso_probabilidade_zero():
    assert gerar_intervalo_uso("08:00", "18:00", 1.0, 2.0, probabilidade=0.0, seed=1) is None


def test_gerar_intervalo_uso_clamp_quando_duracao_maior_que_janela():
    resultado = gerar_intervalo_uso("08:00", "08:10", 1.0, 1.0, dt_min=1, probabilidade=1.0, seed=1, on_overflow="clamp")
    inicio, fim = resultado
    assert fim - inicio == 10  # janela tem 10 passos, duracao de 1h (60) e truncada


def test_equipamento_simula_carga_dentro_e_fora_intervalo():
    eq = Equipamento(nome="Teste", potencia=100, quantidade=2, intervalos=[(10, 20)], probabilidade=1.0, fator_demanda=0.5)
    carga = eq.simula_carga(tempo_total=30)
    assert carga[5] == 0
    assert carga[15] == 100 * 0.5 * 2


def test_calcular_indicadores_ponta_cruzando_meia_noite():
    perfis = np.ones((1, 1440)) * 10
    resultado = calcular_indicadores_ponta_fora(perfis, 1440, inicio_ponta_min=22*60, fim_ponta_min=1*60)
    assert resultado["demanda_media_ponta_w"] == 10.0

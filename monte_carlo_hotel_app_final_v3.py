import streamlit as st
import numpy as np
import pandas as pd
import re
import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, Union
from packaging import version
import copy
import io
import base64
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import os
import matplotlib.pyplot as plt
import zipfile

# Configuração da página
st.set_page_config(
    page_title="D² - Demanda e Dados",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para o tema marinho
st.markdown("""
<style>
    .main {
        background-color: #2c3e50;
        color: white;
    }
    
    .stApp {
        background-color: #2c3e50;
    }
    
    .stMarkdown, .stText, .stSelectbox label, .stNumberInput label, 
    .stSlider label, .stTextInput label, .stRadio label, .stFileUploader label,
    .stExpander label, .stDataFrame, .stTable {
        color: white !important;
    }
    
    .stSelectbox > div > div {
        background-color: #34495e;
        color: white;
    }
    
    .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background-color: #34495e;
        color: white;
        border: 1px solid #5d6d7e;
    }
    
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
    }
    
    .stExpander {
        background-color: #34495e;
        border: 1px solid #5d6d7e;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #34495e;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white;
    }
    
    .stMetric {
        background-color: #34495e;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #5d6d7e;
    }
    
    .stMetric label, .stMetric div {
        color: white !important;
    }
    
    .stSuccess {
        background-color: #27ae60;
        color: white;
    }
    
    .stInfo {
        background-color: #3498db;
        color: white;
    }
    
    .stWarning {
        background-color: #f39c12;
        color: white;
    }
    
    .stError {
        background-color: #e74c3c;
        color: white;
    }
    
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 10px;
        border: 2px solid #5d6d7e;
        width: 100%;
    }
    
    .logo-banner {
        width: 100%;
        height: 120px;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        border: 2px solid #5d6d7e;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .logo-banner img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    
    .title-overlay {
        position: absolute;
        right: 30px;
        top: 50%;
        transform: translateY(-50%);
        text-align: right;
        color: white;
    }
    
    .title-overlay h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .title-overlay p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .sidebar .sidebar-content {
        background-color: #34495e;
    }
    
    .credits-container {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #5d6d7e;
        margin-top: 20px;
        text-align: center;
    }
    
    .credits-container h3 {
        color: #3498db;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }
    
    .credits-container p {
        color: #bdc3c7;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    
    .credits-container a {
        color: #3498db;
        text-decoration: none;
        font-weight: bold;
    }
    
    .credits-container a:hover {
        color: #2980b9;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral com créditos
with st.sidebar:
    st.markdown("""
    <div class="credits-container">
        <h3>💻 Desenvolvido por</h3>
        <p><strong>Matheus Vianna</strong></p>
        <p>Engenheiro Especialista em Python</p>
        <p>📧 Contato: <a href="mailto:matheusviannapr@gmail.com">matheusviannapr@gmail.com</a></p>
        <p>🌐 Website: <a href="https://matheusvianna.com" target="_blank">matheusvianna.com</a></p>
        <hr style="border-color: #5d6d7e; margin: 15px 0;">
        <p style="font-size: 0.8rem; color: #95a5a6;">
            Sistema desenvolvido para análise avançada de carga elétrica utilizando técnicas de simulação Monte Carlo com instâncias individualizadas.
        </p>
        <p style="font-size: 0.8rem; color: #95a5a6;">
            © 2025 - Todos os direitos reservados
        </p>
    </div>
    """, unsafe_allow_html=True)

# Cabeçalho com logo em faixa horizontal
try:
    logo = Image.open("logo_demanda_dados.png")
    
    
    
    # Coluna para a logo
    col_esq, col_central, col_dir = st.columns([1, 3, 1])
    
    with col_central:
        st.image(logo, use_container_width=True)
    
    st.markdown("""
            ###  **Simulação Monte Carlo para Análise de Carga Elétrica - Demanda e Dados**
    """, unsafe_allow_html=True)
    
except:
    st.markdown("""
    <div class="logo-banner">
        <div class="title-overlay" style="left: 50%; transform: translate(-50%, -50%); text-align: center;">
            <h1>Simulação Monte Carlo para Análise de Carga Elétrica em Hotel</h1>
            <p>Sistema avançado de simulação para dimensionamento de infraestrutura elétrica</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Seção "Como Usar o Aplicativo"
with st.expander("📖 Como Usar o Aplicativo", expanded=False):
    st.markdown("""
    ## Guia Completo de Uso
    
    ### 🎯 **Objetivo do Aplicativo**
    Este aplicativo utiliza a técnica de **Simulação Monte Carlo** para analisar o comportamento da carga elétrica em hotéis, considerando a variabilidade natural do uso de equipamentos pelos hóspedes. O sistema simula milhares de cenários diferentes para fornecer estatísticas confiáveis para o dimensionamento da infraestrutura elétrica.
    
    ### 🔧 **Metodologia de Simulação**
    - **Instâncias Individualizadas**: Cada quarto é tratado como uma entidade única com comportamento aleatório independente
    - **Variabilidade Temporal**: Equipamentos podem ter intervalos fixos ou dinâmicos de funcionamento
    - **Fatores Probabilísticos**: Considera a probabilidade de cada equipamento estar em uso
    - **Fator de Demanda**: Aplica fatores de redução baseados no uso real dos equipamentos
    
    ### 📊 **Passo a Passo de Uso**
    
    #### **1. Configuração de Dados**
    **Opção A - Upload de Excel:**
    - Prepare um arquivo Excel com abas nomeadas pelos tipos de cômodos (ex: "Quarto Standard", "Suíte Master")
    - Cada aba deve conter as colunas: Equipamento, Potência, Quantidade, Tipo de intervalo, intervalo, probabilidade, FD
    - Faça o upload do arquivo na seção correspondente
    
    **Opção B - Entrada Direta:**
    - Defina o número de tipos de cômodos diferentes
    - Para cada cômodo, configure os equipamentos com suas características:
      - **Nome**: Identificação do equipamento
      - **Potência (W)**: Consumo nominal em watts
      - **Quantidade**: Número de unidades do equipamento no cômodo
      - **Tipo de intervalo**: "fixo" para horários definidos ou "dinâmico" para horários variáveis
      - **Intervalo**: Período de funcionamento (ex: "08:00 as 18:00" ou "Início entre 14:00-18:00, duração 6")
      - **Probabilidade**: Chance do equipamento estar ligado (0.0 a 1.0)
      - **Fator de Demanda**: Fator de redução do consumo real (0.1 a 1.0)
    
    #### **2. Parâmetros de Simulação**
    - **Número de Simulações**: Recomendado entre 1000-5000 para resultados estatisticamente significativos
    - **Tempo Total**: Período de análise em minutos (1440 = 24 horas)
    
    #### **3. Instâncias por Cômodo**
    - Defina quantas unidades de cada tipo de cômodo existem no hotel
    - Cada instância será simulada independentemente
    
    #### **4. Execução e Resultados**
    - Execute a simulação e analise os resultados em diferentes visualizações
    - Gere o relatório PDF técnico com todas as análises e recomendações
    
    ### 📈 **Interpretação dos Resultados**
    
    #### **Métricas Principais:**
    - **Pico Médio**: Valor esperado da demanda máxima
    - **Percentil 95**: Valor recomendado para dimensionamento (95% dos casos ficam abaixo)
    - **Pico Máximo**: Maior valor observado nas simulações
    - **Pico Mínimo**: Menor valor observado nas simulações
    
    #### **Gráficos de Análise:**
    - **Distribuição dos Picos**: Mostra a frequência dos diferentes valores de pico
    - **Curva de Duração**: Indica por quanto tempo cada nível de carga é mantido
    - **Perfil de Carga**: Revela os padrões de consumo ao longo do dia
    - **Potência Cumulativa**: Mostra a contribuição de cada tipo de cômodo
    
    ### ⚡ **Recomendações de Dimensionamento**
    - Use o **Percentil 95** como base para dimensionamento
    - Adicione uma margem de segurança de 15-20%
    - Considere fatores de crescimento futuro
    - Monitore o comportamento real para validar as simulações
    """, unsafe_allow_html=True)

# --- Definindo a palavra-chave para boxplot conforme a versão do Matplotlib ---
if version.parse(plt.matplotlib.__version__) >= version.parse("3.9"):
    boxplot_kw_global = {"tick_labels": ["Picos do Hotel"]}
else:
    boxplot_kw_global = {"labels": ["Picos do Hotel"]}

# --- Núcleo de simulação ---
IntervalType = Union[List[Tuple[int, int]], Callable[[], List[Tuple[int, int]]]]


def parse_time(time_str: str) -> int:
    parts = time_str.strip().split(":")
    if len(parts) == 1:
        hours = int(parts[0])
        minutes = 0
    else:
        hours = int(parts[0])
        minutes = int(parts[1])
    return hours * 60 + minutes


def parse_intervalo_fixo(interval_str: str) -> List[Tuple[int, int]]:
    interval_str = interval_str.replace("às", "as")
    parts = interval_str.split(" e ")
    intervals = []
    for part in parts:
        times = part.split(" as ")
        if len(times) != 2:
            continue
        start = parse_time(times[0])
        end = parse_time(times[1])
        intervals.append((start, end))
    return intervals


def _duracao_horas_para_passos(duracao_h: float, dt_min: int) -> int:
    return max(1, int(round((duracao_h * 60) / dt_min)))


def gerar_intervalo_uso(
    janela_inicio: str,
    janela_fim: str,
    duracao_min_h: float,
    duracao_max_h: float,
    dt_min: int = 1,
    probabilidade: float = 1.0,
    seed: Optional[int] = None,
    on_overflow: str = "clamp",
) -> Optional[Tuple[int, int]]:
    """
    Retorna (inicio_idx, fim_idx) em passos discretos (não em minutos).

    Regras implementadas:
    - probabilidade é aplicada antes do sorteio de duração/início;
    - duração é sorteada de forma uniforme contínua em horas;
    - n_passos = round(duracao_h * 60 / dt_min);
    - se duração não couber na janela: aplica clamp (reduz para caber) quando on_overflow='clamp'.
    """
    if dt_min <= 0:
        raise ValueError("dt_min deve ser > 0")

    rng = random.Random(seed) if seed is not None else random

    if rng.random() > probabilidade:
        return None

    if duracao_min_h > duracao_max_h:
        raise ValueError("duracao_min_h não pode ser maior que duracao_max_h")

    janela_inicio_min = parse_time(janela_inicio)
    janela_fim_min = parse_time(janela_fim)
    if janela_fim_min <= janela_inicio_min:
        raise ValueError("janela_fim deve ser maior que janela_inicio")

    duracao_h = rng.uniform(duracao_min_h, duracao_max_h)
    n_passos = _duracao_horas_para_passos(duracao_h, dt_min)

    janela_inicio_idx = janela_inicio_min // dt_min
    janela_fim_idx = janela_fim_min // dt_min
    tamanho_janela_passos = janela_fim_idx - janela_inicio_idx

    if n_passos > tamanho_janela_passos:
        if on_overflow == "clamp":
            n_passos = tamanho_janela_passos
        else:
            return None

    latest_start = janela_fim_idx - n_passos
    inicio_idx = rng.randint(janela_inicio_idx, latest_start)
    fim_idx = inicio_idx + n_passos
    return inicio_idx, fim_idx


def parse_intervalo_dinamico_split(interval_str: str) -> Callable[[], List[Tuple[int, int]]]:
    """
    Compatibilidade com formato legado:
      "Início entre 10:30-14:00, duração 2"
    onde duração está em horas e é fragmentada em 1 a 3 segmentos.
    """
    parts = interval_str.split(";")

    def dynamic_intervals():
        intervals = []
        for part in parts:
            part = part.strip()
            m = re.search(r"(?i)entre\s*([\d:]+)\s*-\s*([\d:]+)", part)
            m2 = re.search(r"(?i)duração\s*(\d+(?:[\.,]\d+)?)", part)
            if m and m2:
                start_lower = parse_time(m.group(1))
                start_upper = parse_time(m.group(2))
                total_duration_minutes = int(float(m2.group(1).replace(',', '.')) * 60)

                num_segments = random.randint(1, 3)
                if total_duration_minutes < 2:
                    segments = [total_duration_minutes]
                else:
                    available = total_duration_minutes - 1
                    num_cuts = min(num_segments - 1, available)
                    if num_cuts > 0:
                        cut_points = sorted(random.sample(range(1, total_duration_minutes), num_cuts))
                        segments = []
                        previous = 0
                        for cp in cut_points:
                            segments.append(cp - previous)
                            previous = cp
                        segments.append(total_duration_minutes - previous)
                    else:
                        segments = [total_duration_minutes]

                first_start = random.randint(start_lower, start_upper)
                current_start = first_start
                for seg_duration in segments:
                    intervals.append((current_start, current_start + seg_duration))
                    current_start = current_start + seg_duration + random.randint(0, 30)
        return intervals if intervals else [(0, 60)]

    return dynamic_intervals


def parse_janela_operacao(intervalo_str: str) -> Tuple[int, int]:
    intervalos = parse_intervalo_fixo(intervalo_str)
    if not intervalos:
        raise ValueError(
            "Para duração intervalar, use intervalo no formato 'HH:MM as HH:MM' para janela de operação."
        )
    return intervalos[0]


def criar_gerador_duracao_intervalar(
    janela_inicio_min: int,
    janela_fim_min: int,
    duracao_min_h: float,
    duracao_max_h: float,
    dt_min: int = 1,
    probabilidade: float = 1.0,
    seed: Optional[int] = None,
    on_overflow: str = "clamp",
) -> Callable[[], List[Tuple[int, int]]]:
    """Gera um único intervalo (em minutos) por execução, com duração aleatória em intervalo."""

    def _generator() -> List[Tuple[int, int]]:
        intervalo = gerar_intervalo_uso(
            janela_inicio=f"{janela_inicio_min // 60:02d}:{janela_inicio_min % 60:02d}",
            janela_fim=f"{janela_fim_min // 60:02d}:{janela_fim_min % 60:02d}",
            duracao_min_h=duracao_min_h,
            duracao_max_h=duracao_max_h,
            dt_min=dt_min,
            probabilidade=probabilidade,
            seed=seed,
            on_overflow=on_overflow,
        )
        if intervalo is None:
            return []
        inicio_idx, fim_idx = intervalo
        return [(inicio_idx * dt_min, fim_idx * dt_min)]

    return _generator


@dataclass
class Equipamento:
    nome: str
    potencia: float
    quantidade: int
    intervalos: IntervalType
    probabilidade: float = 1.0
    fator_demanda: float = 1.0
    probabilisticado_no_intervalo: bool = False

    def simula_carga(self, tempo_total: int = 1440):
        carga = np.zeros(tempo_total)
        intervals = self.intervalos() if callable(self.intervalos) else self.intervalos

        if self.probabilisticado_no_intervalo or np.random.rand() < self.probabilidade:
            potencia_efetiva = self.potencia * self.fator_demanda
            for inicio, fim in intervals:
                inicio = max(0, inicio)
                fim = min(tempo_total, fim)
                carga[inicio:fim] += potencia_efetiva * self.quantidade
        return carga


@dataclass
class Comodo:
    nome: str
    equipamentos: List[Equipamento]

    def simula_carga(self, tempo_total: int = 1440):
        carga_total = np.zeros(tempo_total)
        for eq in self.equipamentos:
            carga_total += eq.simula_carga(tempo_total)
        return carga_total


def _get_duration_bounds_h(row: pd.Series) -> Tuple[Optional[float], Optional[float]]:
    duracao_min = row.get("duracao_min")
    duracao_max = row.get("duracao_max")
    duracao_legacy = row.get("duracao")

    if pd.notna(duracao_min) and pd.notna(duracao_max):
        return float(duracao_min), float(duracao_max)
    if pd.notna(duracao_legacy):
        d = float(duracao_legacy)
        return d, d
    return None, None


def cria_comodo_da_planilha(sheet_df: pd.DataFrame, comodo_nome: str) -> Comodo:
    equipamentos = []
    for _, row in sheet_df.iterrows():
        nome = row["Equipamento"]
        potencia = float(row["Potência"])
        quantidade = int(row["Quantidade"])
        tipo_intervalo = str(row["Tipo de intervalo"]).strip().lower()
        intervalo_str = str(row["intervalo"]).strip()
        probabilidade = float(row["probabilidade"])
        fd = float(row["FD"])
        modo_fixo = str(row.get("modo_fixo", "FIXO_100%")).strip().upper()

        duracao_min_h, duracao_max_h = _get_duration_bounds_h(row)

        probabilisticado_no_intervalo = False

        if tipo_intervalo == "fixo":
            if duracao_min_h is not None and modo_fixo == "FIXO_DURACAO_INTERVALAR":
                inicio, fim = parse_janela_operacao(intervalo_str)
                intervalos = criar_gerador_duracao_intervalar(
                    janela_inicio_min=inicio,
                    janela_fim_min=fim,
                    duracao_min_h=duracao_min_h,
                    duracao_max_h=duracao_max_h,
                    probabilidade=probabilidade,
                    dt_min=1,
                    on_overflow="clamp",
                )
                probabilisticado_no_intervalo = True
            else:
                intervalos = parse_intervalo_fixo(intervalo_str)
        elif tipo_intervalo == "dinâmico":
            if duracao_min_h is not None:
                inicio, fim = parse_janela_operacao(intervalo_str)
                intervalos = criar_gerador_duracao_intervalar(
                    janela_inicio_min=inicio,
                    janela_fim_min=fim,
                    duracao_min_h=duracao_min_h,
                    duracao_max_h=duracao_max_h,
                    probabilidade=probabilidade,
                    dt_min=1,
                    on_overflow="clamp",
                )
                probabilisticado_no_intervalo = True
            else:
                intervalos = parse_intervalo_dinamico_split(intervalo_str)
        else:
            intervalos = parse_intervalo_fixo(intervalo_str)

        eq = Equipamento(
            nome=nome,
            potencia=potencia,
            quantidade=quantidade,
            intervalos=intervalos,
            probabilidade=probabilidade,
            fator_demanda=fd,
            probabilisticado_no_intervalo=probabilisticado_no_intervalo,
        )
        equipamentos.append(eq)
    return Comodo(nome=comodo_nome, equipamentos=equipamentos)


def cria_comodos_do_excel(uploaded_file) -> List[Comodo]:
    sheets = pd.read_excel(uploaded_file, sheet_name=None)
    return [cria_comodo_da_planilha(df, sheet_name) for sheet_name, df in sheets.items()]


def cria_comodos_do_dataframe(df_dict: dict) -> List[Comodo]:
    comodos = []
    for comodo_nome, df in df_dict.items():
        if not df.empty:
            comodos.append(cria_comodo_da_planilha(df, comodo_nome))
    return comodos


def cria_comodos_individualizados(comodos: List[Comodo], instancias_por_comodo: dict) -> List[Comodo]:
    comodos_individualizados = []
    for comodo in comodos:
        qtd = instancias_por_comodo.get(comodo.nome, 1)
        for i in range(qtd):
            equipamentos_copia = []
            for eq in comodo.equipamentos:
                equipamentos_copia.append(
                    Equipamento(
                        nome=eq.nome,
                        potencia=eq.potencia,
                        quantidade=eq.quantidade,
                        intervalos=eq.intervalos,
                        probabilidade=eq.probabilidade,
                        fator_demanda=eq.fator_demanda,
                        probabilisticado_no_intervalo=eq.probabilisticado_no_intervalo,
                    )
                )
            comodos_individualizados.append(Comodo(nome=f"{comodo.nome}.{i+1}", equipamentos=equipamentos_copia))
    return comodos_individualizados


def simula_carga_total(
    comodos: List[Comodo],
    instancias_por_comodo: dict,
    num_simulacoes: int = 1000,
    tempo_total: int = 1440,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    picos = []
    perfis = []
    consumos_diarios = []
    comodos_individualizados = cria_comodos_individualizados(comodos, instancias_por_comodo)

    for _ in range(num_simulacoes):
        load_total = np.zeros(tempo_total)
        for comodo in comodos_individualizados:
            load_total += comodo.simula_carga(tempo_total)

        picos.append(np.max(load_total))
        perfis.append(load_total)
        consumos_diarios.append(np.sum(load_total) / 1000 / 60)

    return np.array(picos), np.array(perfis), np.array(consumos_diarios)


# Função para salvar gráficos como imagens
def salvar_grafico(fig, nome_arquivo):
    """Salva um gráfico matplotlib como imagem PNG"""
    caminho = f"/tmp/{nome_arquivo}.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight", facecolor="white")
    return caminho


def gerar_graficos_relatorio(picos, perfis, pico_medio, pico_95, tempo_total, num_simulacoes, comodos, instancias_por_comodo):
    """Gera os gráficos utilizados nos relatórios e retorna metadados com os caminhos."""
    imagens_graficos = []

    # 1. Distribuição dos picos
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(picos, bins=30, alpha=0.7, edgecolor="black", density=True)
    ax.axvline(pico_medio, color="red", linestyle="dashed", linewidth=2, label=f"Média: {pico_medio:.0f} W")
    ax.axvline(pico_95, color="green", linestyle="dashed", linewidth=2, label=f"P95: {pico_95:.0f} W")
    ax.set_title("Distribuição dos Picos de Carga")
    ax.set_xlabel("Pico de Carga (W)")
    ax.set_ylabel("Frequência Normalizada")
    ax.legend()
    ax.grid(True)
    caminho_img = salvar_grafico(fig, "distribuicao_picos")
    imagens_graficos.append({"titulo": "Distribuição dos Picos de Carga", "caminho": caminho_img, "descricao": "Este histograma apresenta a distribuição estatística dos picos de demanda elétrica obtidos através das simulações Monte Carlo. A análise da forma da distribuição fornece insights sobre a previsibilidade do comportamento da carga: distribuições mais concentradas (baixo desvio padrão) indicam comportamento mais previsível, enquanto distribuições mais dispersas sugerem maior variabilidade operacional. A linha vermelha tracejada representa a demanda média máxima esperada, enquanto a linha verde indica o percentil 95 (P95), valor amplamente utilizado na engenharia elétrica como referência para dimensionamento de transformadores e sistemas de proteção, pois garante que 95% dos cenários simulados apresentem demanda inferior a este valor."})
    plt.close(fig)

    # 2. Curva de duração de carga
    todas_cargas = np.concatenate(perfis)
    todas_cargas_sorted = np.sort(todas_cargas)[::-1]
    frac_tempo = np.arange(1, len(todas_cargas_sorted) + 1) / len(todas_cargas_sorted)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frac_tempo * 100, todas_cargas_sorted, label="Load Duration Curve", linewidth=2)
    ax.set_title("Curva de Duração de Carga")
    ax.set_xlabel("Fração do Tempo (%)")
    ax.set_ylabel("Carga (W)")
    ax.grid(True)
    ax.legend()
    caminho_img = salvar_grafico(fig, "curva_duracao")
    imagens_graficos.append({"titulo": "Curva de Duração de Carga", "caminho": caminho_img, "descricao": "A Curva de Duração de Carga (CDC) é uma ferramenta fundamental para análise energética que apresenta os valores de demanda em ordem decrescente de magnitude, revelando por quanto tempo cada nível de carga é mantido ou excedido durante o período analisado. Esta curva é essencial para estudos de viabilidade econômica de sistemas de geração distribuída, dimensionamento de sistemas de armazenamento de energia e análise de contratos de fornecimento com tarifação diferenciada por horário. A inclinação da curva indica a variabilidade da demanda: curvas mais íngremes sugerem grandes variações entre picos e vales de consumo, enquanto curvas mais suaves indicam demanda mais constante ao longo do tempo."})
    plt.close(fig)

    # 3. Perfil de carga médio
    tempo = np.arange(tempo_total) / 60.0
    perfil_medio = np.mean(perfis, axis=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(tempo, perfil_medio, linewidth=2, color="blue")
    ax.set_title("Perfil Médio de Carga ao Longo do Dia")
    ax.set_xlabel("Hora do Dia")
    ax.set_ylabel("Carga Média (W)")
    ax.grid(True, alpha=0.3)
    caminho_img = salvar_grafico(fig, "perfil_carga")
    imagens_graficos.append({"titulo": "Perfil Médio de Carga ao Longo do Dia", "caminho": caminho_img, "descricao": "O perfil médio de carga representa a demanda elétrica média esperada para cada minuto do dia, calculada a partir da média de todas as simulações realizadas. Este gráfico é fundamental para o planejamento operacional do sistema elétrico, permitindo identificar os horários de maior e menor demanda, que são cruciais para estratégias de gestão energética e otimização de custos. Os picos de demanda geralmente coincidem com períodos de maior atividade dos hóspedes, como check-in/check-out, horários de refeições e períodos noturnos. A análise deste perfil também orienta decisões sobre implementação de sistemas de gestão automática de cargas, dimensionamento de sistemas de climatização e ventilação."})
    plt.close(fig)

    # 4. Gráfico de potência cumulativa por cômodo
    comodos_cargas_medias = {}
    for comodo_obj in comodos:
        comodo_copia = copy.deepcopy(comodo_obj)
        instancias_para_comodo = {comodo_copia.nome: instancias_por_comodo.get(comodo_copia.nome, 1)}
        _, perfis_comodo, _ = simula_carga_total(
            [comodo_copia],
            instancias_para_comodo,
            num_simulacoes=num_simulacoes,
            tempo_total=tempo_total
        )
        comodos_cargas_medias[comodo_obj.nome] = np.mean(perfis_comodo, axis=0)

    if comodos_cargas_medias:
        horas = np.arange(tempo_total) / 60.0

        fig, ax = plt.subplots(figsize=(14, 8))
        comodos_nomes = list(comodos_cargas_medias.keys())
        comodos_valores = [comodos_cargas_medias[nome] for nome in comodos_nomes]

        ax.stackplot(horas, *comodos_valores, labels=comodos_nomes, alpha=0.8)
        ax.set_xlabel("Hora do Dia")
        ax.set_ylabel("Potência (W)")
        ax.set_title("Potência Cumulativa por Cômodo ao Longo do Dia")
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        caminho_img = salvar_grafico(fig, "potencia_cumulativa_comodo")
        imagens_graficos.append({"titulo": "Potência Cumulativa por Cômodo ao Longo do Dia", "caminho": caminho_img, "descricao": "Este gráfico de área empilhada (stackplot) ilustra a contribuição individual de cada tipo de cômodo para a demanda total do estabelecimento ao longo do ciclo diário. A análise permite identificar quais categorias de cômodos são os principais consumidores de energia em diferentes horários, fornecendo informações valiosas para estratégias de eficiência energética e priorização de investimentos. A espessura de cada camada representa a magnitude da contribuição de cada tipo de cômodo, enquanto a variação ao longo do tempo revela padrões de uso específicos. Esta visualização é particularmente útil para gestores hoteleiros na tomada de decisões sobre retrofit de equipamentos, implementação de sistemas de gestão automática de cargas, dimensionamento de sistemas de climatização e ventilação."})
        plt.close(fig)

    return imagens_graficos


def escapar_latex(texto):
    """Escapa caracteres especiais para LaTeX."""
    substituicoes = {
        "\\": r"\\textbackslash{}",
        "&": r"\\&",
        "%": r"\\%",
        "$": r"\\$",
        "#": r"\\#",
        "_": r"\\_",
        "{": r"\\{",
        "}": r"\\}",
        "~": r"\\textasciitilde{}",
        "^": r"\\textasciicircum{}",
    }
    return "".join(substituicoes.get(c, c) for c in str(texto))




def formatar_intervalos_para_relatorio(intervalos):
    """Formata intervalos para texto de relatório sem quebrar em casos dinâmicos."""
    if callable(intervalos):
        return "Intervalo dinâmico (gerado estocasticamente a cada simulação)"

    if isinstance(intervalos, (list, tuple)):
        pares_validos = []
        for item in intervalos:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                pares_validos.append(f"[{item[0]}-{item[1]}]")
        if pares_validos:
            return "; ".join(pares_validos)
        return "Intervalos não estruturados"

    if intervalos is None:
        return "N/A"

    return str(intervalos)


def gerar_zip_relatorio_latex(resultados, instancias_por_comodo, num_simulacoes, tempo_total, imagens_graficos, comodos_config_data=None, comodos_originais=None):
    """Gera um arquivo ZIP com relatório LaTeX técnico completo e imagens dos gráficos."""
    picos = resultados["picos"]
    perfis = resultados["perfis"]
    consumos = resultados["consumos"]

    pico_medio = np.mean(picos)
    pico_max = np.max(picos)
    pico_min = np.min(picos)
    pico_95 = np.percentile(picos, 95)
    desvio_padrao = np.std(picos)
    coef_variacao = (desvio_padrao / pico_medio) * 100 if pico_medio > 0 else 0
    consumo_medio = np.mean(consumos)

    media_por_minuto = np.mean(perfis, axis=0)
    fator_carga_medio = (np.mean(media_por_minuto) / np.max(media_por_minuto)) * 100 if np.max(media_por_minuto) > 0 else 0
    ic_inferior = np.percentile(picos, 2.5)
    ic_superior = np.percentile(picos, 97.5)
    capacidade_recomendada = pico_95 * 1.2

    total_potencia_instalada_comodos = 0
    if comodos_originais:
        for comodo_obj in comodos_originais:
            total_potencia_instalada_comodos += sum(eq.potencia * eq.quantidade for eq in comodo_obj.equipamentos) * instancias_por_comodo.get(comodo_obj.nome, 1)

    fator_diversidade = pico_medio / total_potencia_instalada_comodos if total_potencia_instalada_comodos > 0 else 0

    if coef_variacao < 15:
        interpretacao_diversidade = "baixa variabilidade, comportamento previsível e estável"
    elif coef_variacao < 30:
        interpretacao_diversidade = "variabilidade moderada, comportamento típico para instalações hoteleiras"
    else:
        interpretacao_diversidade = "alta variabilidade, requer monitoramento e análise adicional"

    if fator_carga_medio > 70:
        interpretacao_fator_carga = "excelente utilização da infraestrutura instalada"
    elif fator_carga_medio > 50:
        interpretacao_fator_carga = "boa utilização da infraestrutura"
    else:
        interpretacao_fator_carga = "utilização baixa, com grande diferença entre carga média e pico"

    secoes_graficos = []
    for idx, imagem in enumerate(imagens_graficos, start=1):
        nome_arquivo = os.path.basename(imagem["caminho"])
        secoes_graficos.append(fr"""
\subsection*{{Figura {idx}: {escapar_latex(imagem['titulo'])}}}
\begin{{figure}}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{{images/{nome_arquivo}}}
    \caption{{{escapar_latex(imagem['titulo'])}}}
\end{{figure}}

\textbf{{Análise Técnica:}} {escapar_latex(imagem['descricao'])}
""")

    linhas_instancias = "\n".join(
        f"\\item {escapar_latex(nome)}: {quantidade} instância(s)"
        for nome, quantidade in instancias_por_comodo.items()
    )

    configuracao_comodos = ""
    if comodos_originais:
        blocos = []
        for comodo in comodos_originais:
            pot_instalada = sum(eq.potencia * eq.quantidade for eq in comodo.equipamentos)
            linhas_eq = []
            for eq in comodo.equipamentos:
                intervalos = formatar_intervalos_para_relatorio(eq.intervalos)
                linhas_eq.append(
                    f"{escapar_latex(eq.nome)} & {eq.potencia:.1f} & {eq.quantidade} & {eq.probabilidade:.2f} & {eq.fator_demanda:.2f} & {escapar_latex(intervalos)} \\\\" 
                )
            tabela_eq = "\n".join(linhas_eq) if linhas_eq else "Sem equipamentos cadastrados."
            blocos.append(fr"""
\subsection*{{{escapar_latex(comodo.nome)}}}
Instâncias deste tipo de cômodo: {instancias_por_comodo.get(comodo.nome, 1)}. Potência instalada por unidade: {pot_instalada:.1f} W.

\begin{{longtable}}{{p{{4.2cm}}rrrrp{{4.2cm}}}}
\toprule
Equipamento & Potência (W) & Qtde & Prob. & Fator Demanda & Intervalos \\
\midrule
{tabela_eq}
\bottomrule
\end{{longtable}}
""")
        configuracao_comodos = "\n".join(blocos)

    configuracao_manual = ""
    if comodos_config_data:
        blocos_man = [r"\subsection*{Configuração Detalhada (Entrada Manual)}"]
        for comodo_nome, equipamentos_df_list in comodos_config_data.items():
            blocos_man.append(f"\\paragraph{{{escapar_latex(comodo_nome)}}}")
            for df in equipamentos_df_list:
                if not df.empty:
                    for _, row in df.iterrows():
                        blocos_man.append(
                            "\\begin{itemize}"
                            + f"\\item Equipamento: {escapar_latex(row.get('nome', 'N/A'))}"
                            + f"\\item Potência: {escapar_latex(row.get('potencia', 'N/A'))} W"
                            + f"\\item Quantidade: {escapar_latex(row.get('quantidade', 'N/A'))}"
                            + f"\\item Intervalos: {escapar_latex(row.get('intervalos', 'N/A'))}"
                            + f"\\item Probabilidade: {escapar_latex(row.get('probabilidade', 'N/A'))}"
                            + f"\\item Fator de Demanda: {escapar_latex(row.get('fator_demanda', 'N/A'))}"
                            + "\\end{itemize}"
                        )
        configuracao_manual = "\n".join(blocos_man)

    conteudo_tex = fr"""\documentclass[12pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[brazil]{{babel}}
\usepackage{{lmodern}}
\usepackage{{geometry}}
\usepackage{{graphicx}}
\usepackage{{float}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{array}}
\geometry{{margin=2.5cm}}

\title{{RELATÓRIO TÉCNICO DE SIMULAÇÃO MONTE CARLO\\Análise de Carga Elétrica para Dimensionamento de Infraestrutura Hoteleira}}
\author{{Sistema Desenvolvido por Matheus Vianna\\Engenheiro Especialista em Simulação Monte Carlo}}
\date{{Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}}}

\begin{{document}}
\maketitle

\section*{{1. Metodologia e Fundamentos Teóricos}}
A simulação Monte Carlo é uma técnica estatística que utiliza amostragem aleatória repetitiva para obter resultados numéricos de problemas complexos. No contexto deste estudo, a metodologia foi aplicada para modelar o comportamento estocástico da demanda elétrica em estabelecimentos hoteleiros, considerando a variabilidade natural do uso de equipamentos pelos hóspedes.

O sistema implementado realiza {num_simulacoes:,} simulações independentes, cada uma representando um cenário possível de operação do hotel durante um período de {tempo_total // 60} horas. Esta abordagem permite capturar a incerteza inerente ao comportamento dos usuários e fornecer estatísticas robustas para o dimensionamento da infraestrutura elétrica.

\subsection*{{1.1 Modelagem de Instâncias Individualizadas}}
Uma característica fundamental desta simulação é o tratamento individualizado de cada unidade habitacional. Quando o hotel possui múltiplas unidades do mesmo tipo, cada uma é modelada como uma entidade independente com seu próprio comportamento aleatório. Esta abordagem é crucial para capturar adequadamente o fator de diversidade.

\subsection*{{1.2 Parâmetros de Entrada e Configuração}}
\begin{{itemize}}
    \item Número total de simulações realizadas: {num_simulacoes:,}
    \item Período de análise por simulação: {tempo_total} minutos ({tempo_total // 60} horas)
    \item Resolução temporal: 1 minuto
    \item Método de amostragem: pseudo-aleatório com distribuições específicas por equipamento
\end{{itemize}}

\section*{{2. Configuração do Sistema Simulado}}
\subsection*{{2.1 Instâncias por Cômodo}}
\begin{{itemize}}
{linhas_instancias}
\end{{itemize}}

\subsection*{{2.2 Potência Instalada e Caracterização por Cômodo}}
{configuracao_comodos if configuracao_comodos else 'Configuração detalhada por cômodo não disponível nesta execução.'}

{configuracao_manual}

\section*{{3. Resultados Consolidados da Simulação}}
\begin{{table}}[H]
    \centering
    \begin{{tabular}}{{lr}}
        \toprule
        Métrica & Valor \\
        \midrule
        Pico médio & {pico_medio:.2f} W \\
        Pico máximo & {pico_max:.2f} W \\
        Pico mínimo & {pico_min:.2f} W \\
        Percentil 95 (P95) & {pico_95:.2f} W \\
        Consumo médio diário & {consumo_medio:.2f} kWh \\
        \bottomrule
    \end{{tabular}}
\end{{table}}

\section*{{4. Análise Gráfica da Demanda}}
Os gráficos a seguir fornecem insights fundamentais sobre o comportamento da demanda elétrica do estabelecimento, permitindo uma compreensão abrangente dos padrões de consumo e suas implicações para o dimensionamento da infraestrutura.
{''.join(secoes_graficos)}

\section*{{5. Análise Estatística Avançada}}
\begin{{itemize}}
    \item Desvio padrão dos picos: {desvio_padrao:.2f} W
    \item Coeficiente de variação: {coef_variacao:.2f}\% ({escapar_latex(interpretacao_diversidade)})
    \item Intervalo de confiança (95\%): {ic_inferior:.2f} W a {ic_superior:.2f} W
    \item Amplitude de variação: {(pico_max - pico_min):.2f} W
    \item Fator de carga médio: {fator_carga_medio:.2f}\% ({escapar_latex(interpretacao_fator_carga)})
    \item Fator de diversidade: {fator_diversidade:.4f}
    \item Densidade de carga: {(pico_medio / sum(instancias_por_comodo.values())):.2f} W/unidade
\end{{itemize}}

\section*{{6. Recomendações Técnicas para Dimensionamento}}
\begin{{itemize}}
    \item Capacidade recomendada para transformadores: {capacidade_recomendada:.0f} W (P95 + 20\% de margem de segurança).
    \item Dimensionamento de condutores: considerar fatores de correção por temperatura e agrupamento conforme NBR 5410.
    \item Sistemas de proteção: ajustes baseados no P95 com coordenação seletiva para garantir continuidade do serviço.
    \item Fator de demanda global de referência: {(pico_95 / (pico_medio * 1.2)):.4f}.
\end{{itemize}}

\section*{{7. Conclusões e Considerações Finais}}
A simulação Monte Carlo realizada com {num_simulacoes:,} cenários independentes fornece uma base estatisticamente robusta para o dimensionamento da infraestrutura elétrica do estabelecimento hoteleiro. A metodologia de instâncias individualizadas permite capturar adequadamente o fator de diversidade, resultando em dimensionamentos mais precisos e economicamente otimizados.

Os resultados apresentados baseiam-se nas configurações de equipamentos e padrões de uso fornecidos. Mudanças significativas no perfil de ocupação, introdução de novos tipos de equipamentos ou alterações nos hábitos dos usuários podem impactar os resultados e requerem reavaliação da simulação.

A capacidade recomendada de {capacidade_recomendada:.0f} W oferece um equilíbrio adequado entre confiabilidade operacional e viabilidade econômica. Recomenda-se implementar monitoramento contínuo para validação dos resultados e refinamento progressivo dos modelos de simulação.

\vspace{{1em}}
\begin{{center}}
Relatório Técnico Gerado Automaticamente\\
Sistema: Simulação Monte Carlo com Instâncias Individualizadas\\
Desenvolvido por Matheus Vianna --- matheusvianna.com
\end{{center}}

\end{{document}}
"""

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("relatorio_monte_carlo.tex", conteudo_tex)

        for imagem in imagens_graficos:
            caminho = imagem["caminho"]
            nome_arquivo = os.path.basename(caminho)
            with open(caminho, "rb") as arquivo_imagem:
                zip_file.writestr(f"images/{nome_arquivo}", arquivo_imagem.read())

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# Função para gerar PDF com os resultados (versão aprimorada com FPDF2)
def gerar_pdf_relatorio(resultados, instancias_por_comodo, num_simulacoes, tempo_total, imagens_graficos=None, comodos_config_data=None, comodos_originais=None):
    """Gera um relatório PDF técnico aprimorado com os resultados da simulação usando FPDF2"""
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)

    # Título do Relatório
    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(190, 10, "RELATÓRIO TÉCNICO DE SIMULAÇÃO MONTE CARLO", align="C")
    pdf.set_font("Times", "", 12)
    # Ajustando a largura da célula para o título secundário
    pdf.multi_cell(190, 8, "Análise de Carga Elétrica para Dimensionamento de Infraestrutura Hoteleira", align="C")
    pdf.ln(5)
    pdf.multi_cell(190, 6, f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", align="C")
    pdf.multi_cell(190, 6, "Sistema: Simulação Monte Carlo com Instâncias Individualizadas", align="C")
    pdf.ln(10)

    # Créditos do Desenvolvedor
    pdf.set_text_color(44, 62, 80) # Dark blue text
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 8, " Sistema Desenvolvido por Matheus Vianna", align="C")
    pdf.set_font("Times", "", 10)
    pdf.multi_cell(190, 6, "Engenheiro Especialista em Simulação Monte Carlo", align="C")
    pdf.multi_cell(190, 6, "Website: matheusvianna.com", align="C", link="https://matheusvianna.com")
    pdf.multi_cell(190, 6, "Sistema avançado para análise de carga elétrica utilizando técnicas de simulação Monte Carlo", align="C")
    pdf.set_text_color(0, 0, 0) # Reset text color
    pdf.ln(10)

    # 1. Metodologia e Fundamentos Teóricos
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "1. METODOLOGIA E FUNDAMENTOS TEÓRICOS", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "A simulação Monte Carlo é uma técnica estatística que utiliza amostragem aleatória repetitiva para obter resultados numéricos de problemas complexos. No contexto deste estudo, a metodologia foi aplicada para modelar o comportamento estocástico da demanda elétrica em estabelecimentos hoteleiros, considerando a variabilidade natural do uso de equipamentos pelos hóspedes.", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"O sistema implementado realiza {num_simulacoes:,} simulações independentes, cada uma representando um cenário possível de operação do hotel durante um período de {tempo_total // 60} horas. Esta abordagem permite capturar a incerteza inerente ao comportamento dos usuários e fornecer estatísticas robustas para o dimensionamento da infraestrutura elétrica.", align="J")
    pdf.ln(5)
    pdf.set_font("Times", "B", 12)
    pdf.multi_cell(190, 7, "1.1 Modelagem de Instâncias Individualizadas", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "Uma característica fundamental desta simulação é o tratamento individualizado de cada unidade habitacional. Quando o hotel possui múltiplas unidades do mesmo tipo (por exemplo, 28 quartos padrão), cada uma é modelada como uma entidade independente com seu próprio comportamento aleatório. Esta abordagem é crucial para capturar adequadamente o fator de diversidade, que representa a probabilidade de que nem todos os equipamentos operem simultaneamente em sua capacidade máxima.", align="J")
    pdf.ln(5)
    pdf.set_font("Times", "B", 12)
    pdf.multi_cell(190, 7, "1.2 Parâmetros de Entrada e Configuração", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Número total de simulações realizadas: {num_simulacoes:,}", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Período de análise por simulação: {tempo_total} minutos ({tempo_total // 60} horas)", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Resolução temporal: 1 minuto", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Método de amostragem: Pseudo-aleatório com distribuições específicas por equipamento", align="J")
    pdf.ln(10)

    # Calcula estatísticas adicionais
    picos = resultados["picos"]
    perfis = resultados["perfis"]
    consumos = resultados["consumos"]
    
    pico_medio = np.mean(picos)
    pico_max = np.max(picos)
    pico_min = np.min(picos)
    pico_95 = np.percentile(picos, 95)
    desvio_padrao = np.std(picos)
    coef_variacao = (desvio_padrao / pico_medio) * 100
    consumo_medio = np.mean(consumos)
    
    # Calcula fator de carga médio
    media_por_minuto = np.mean(perfis, axis=0)
    fator_carga_medio = (np.mean(media_por_minuto) / np.max(media_por_minuto)) * 100
    
    # Intervalo de confiança 95%
    ic_inferior = np.percentile(picos, 2.5)
    ic_superior = np.percentile(picos, 97.5)
    
    # Capacidade recomendada (P95 + 20%)
    capacidade_recomendada = pico_95 * 1.2
    
    # Fator de diversidade
    total_potencia_instalada_comodos = 0
    if comodos_originais:
        for comodo_obj in comodos_originais:
            total_potencia_instalada_comodos += sum(eq.potencia * eq.quantidade for eq in comodo_obj.equipamentos) * instancias_por_comodo.get(comodo_obj.nome, 1)

    fator_diversidade = pico_medio / total_potencia_instalada_comodos if total_potencia_instalada_comodos > 0 else 0
    
    # Interpretações técnicas
    if coef_variacao < 15:
        interpretacao_diversidade = "baixa variabilidade, comportamento previsível e estável"
    elif coef_variacao < 30:
        interpretacao_diversidade = "variabilidade moderada, comportamento típico para instalações hoteleiras"
    else:
        interpretacao_diversidade = "alta variabilidade, requer monitoramento e análise adicional"
    
    if fator_carga_medio > 70:
        interpretacao_fator_carga = "indica utilização eficiente da infraestrutura elétrica"
    elif fator_carga_medio > 50:
        interpretacao_fator_carga = "indica utilização moderada da infraestrutura elétrica"
    else:
        interpretacao_fator_carga = "indica potencial de otimização da infraestrutura elétrica"
    
    # 2. Resultados Estatísticos e Análise de Demanda
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "2. RESULTADOS ESTATÍSTICOS E ANÁLISE DE DEMANDA", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Demanda Média Máxima: {pico_medio:.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Demanda Máxima Absoluta: {pico_max:.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Demanda Mínima Observada: {pico_min:.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Percentil 95 (P95): {pico_95:.0f} W", align="J")
    pdf.ln(5)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"O Percentil 95 (P95) de {pico_95:.0f} W representa o valor de demanda que é excedido em apenas 5% dos cenários simulados. Este valor é amplamente reconhecido na engenharia elétrica como referência para dimensionamento de sistemas, pois oferece um equilíbrio adequado entre segurança operacional e viabilidade econômica.", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"A Demanda Média Máxima de {pico_medio:.0f} W indica o valor esperado da demanda de pico, enquanto a Demanda Máxima Absoluta de {pico_max:.0f} W representa o cenário mais crítico observado nas simulações, que possui probabilidade muito baixa de ocorrência.", align="J")
    pdf.ln(10)

    # 3. Configuração Detalhada dos Cômodos
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "3. CONFIGURAÇÃO DETALHADA DOS CÔMODOS", align="J")
    pdf.set_font("Times", "B", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "3.1 Resumo por Tipo de Cômodo", align="J")
    pdf.set_font("Times", "", 10)
    pdf.set_x(pdf.l_margin)
    

    # Tabela de Resumo por Tipo de Cômodo
    table_data = [["Tipo de Cômodo", "Número de Instâncias", "Demanda Estimada por Instância (W)", "Contribuição Total (%)"]]
    total_instancias = sum(instancias_por_comodo.values())
    for comodo, instancias in instancias_por_comodo.items():
        potencia_estimada = (pico_medio / total_instancias * instancias) if total_instancias > 0 else 0
        table_data.append([
            comodo,
            str(instancias),
            f"{potencia_estimada:.0f}",
            f"{(instancias / total_instancias * 100):.1f}%"
        ])
    
    # Calculate column widths to fit content and page width
    col_widths = [pdf.get_string_width(str(item)) for item in table_data[0]]
    for row in table_data[1:]:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], pdf.get_string_width(str(cell)))
    
    # Add some padding
    col_widths = [w + 6 for w in col_widths]
    
    # Distribute remaining space if total width is less than page width
    total_table_width = sum(col_widths)
    page_width = pdf.w - 2 * pdf.l_margin
    if total_table_width < page_width:
        extra_space_per_col = (page_width - total_table_width) / len(col_widths)
        col_widths = [w + extra_space_per_col for w in col_widths]

    for row in table_data:
        for i, cell in enumerate(row):
            pdf.multi_cell(col_widths[i], 8, cell, border=1, align="C" if i > 0 else "L", ln=3)
        pdf.ln(8)
    pdf.ln(5)

    # Tabela de Especificação Técnica dos Equipamentos
    if comodos_config_data:
        pdf.set_font("Times", "B", 12)
        pdf.multi_cell(190, 7, "3.2 Especificação Técnica dos Equipamentos", align="J")
        pdf.set_font("Times", "", 10)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(190, 7, "A tabela a seguir apresenta a configuração detalhada de cada equipamento por tipo de cômodo, incluindo características operacionais e parâmetros de simulação utilizados.", align="J")
        pdf.ln(5)
        
        for comodo_nome, equipamentos_df_list in comodos_config_data.items():
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(190, 7, f"Cômodo: {comodo_nome}", align="J")
            pdf.set_font("Times", "", 9)
            
            equip_table_data = [["Equipamento", "Potência (W)", "Quantidade", "Tipo de Operação", "Período de Funcionamento", "Probabilidade de Uso", "Fator de Demanda"]]
            for row in equipamentos_df_list:
                equip_table_data.append([
                    row["Equipamento"],
                    str(row["Potência"]),
                    str(row["Quantidade"]),
                    str(row["Tipo de intervalo"]).title(),
                    str(row["intervalo"]),
                    f"{row['probabilidade'] * 100:.1f}%",
                    f"{row['FD']:.2f}"
                ])
            
            # Calculate column widths for equipment table
            equip_col_widths = [pdf.get_string_width(str(item)) for item in equip_table_data[0]]
            for row in equip_table_data[1:]:
                for i, cell in enumerate(row):
                    equip_col_widths[i] = max(equip_col_widths[i], pdf.get_string_width(str(cell)))
            
            equip_col_widths = [w + 4 for w in equip_col_widths] # Add padding
            
            total_equip_table_width = sum(equip_col_widths)
            if total_equip_table_width < page_width:
                extra_space_per_col = (page_width - total_equip_table_width) / len(equip_col_widths)
                equip_col_widths = [w + extra_space_per_col for w in equip_col_widths]

            for row in equip_table_data:
                for i, cell in enumerate(row):
                    pdf.multi_cell(equip_col_widths[i], 7, cell, border=1, align="C" if i in [1,2,5,6] else "L", ln=3)
                pdf.ln(7)
            pdf.ln(5)

    pdf.ln(10)

    # 4. Análises Gráficas e Interpretações Técnicas
    if imagens_graficos:
        pdf.set_font("Times", "B", 14)
        pdf.multi_cell(190, 10, "4. ANÁLISES GRÁFICAS E INTERPRETAÇÕES TÉCNICAS", align="J")
        pdf.set_font("Times", "", 12)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(190, 7, "As análises gráficas apresentadas a seguir fornecem insights fundamentais sobre o comportamento da demanda elétrica do estabelecimento, permitindo uma compreensão abrangente dos padrões de consumo e suas implicações para o dimensionamento da infraestrutura.", align="J")
        pdf.ln(5)
        
        for imagem in imagens_graficos:
            pdf.set_font("Times", "B", 12)
            pdf.multi_cell(190, 7, imagem["titulo"], align="C")
            pdf.ln(2)
            
            # Adiciona a imagem
            img_path = imagem["caminho"]
            if img_path and os.path.exists(img_path):
                # Get image dimensions to fit page
                img = Image.open(img_path)
                img_width, img_height = img.size
                
                # Max width for image in PDF
                max_img_width = pdf.w - 2 * pdf.l_margin - 10 # 10 for extra padding
                
                # Calculate new dimensions to maintain aspect ratio
                if img_width > max_img_width:
                    scale_factor = max_img_width / img_width
                    img_width = max_img_width
                    img_height = img_height * scale_factor
                
                # Center image
                x_pos = (pdf.w - img_width) / 2
                pdf.image(img_path, x=x_pos, w=img_width)
                pdf.ln(5)
            
            pdf.set_font("Times", "", 10)
            pdf.multi_cell(190, 6, "Análise Técnica: " + imagem["descricao"], align="J")
            pdf.ln(10)

    # 5. Análise Estatística Avançada
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "5. ANÁLISE ESTATÍSTICA AVANÇADA", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Desvio Padrão dos Picos: {desvio_padrao:.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Coeficiente de Variação: {coef_variacao:.1f}% - {interpretacao_diversidade}", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Intervalo de Confiança (95%): {ic_inferior:.0f} W - {ic_superior:.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Amplitude de Variação: {(pico_max - pico_min):.0f} W", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.ln(5)
    pdf.multi_cell(190, 7, f"Consumo Médio Diário: {consumo_medio:.1f} kWh", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Fator de Carga Médio: {fator_carga_medio:.1f}% - {interpretacao_fator_carga}", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Fator de Diversidade: {fator_diversidade:.2f}", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Densidade de Carga: {(pico_medio / sum(instancias_por_comodo.values())):.2f} W/unidade", align="J")
    pdf.ln(10)

    # 6. Recomendações Técnicas para Dimensionamento
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "6. RECOMENDAÇÕES TÉCNICAS PARA DIMENSIONAMENTO", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Capacidade Recomendada para Transformadores: {capacidade_recomendada:.0f} W (P95 + 20% de margem de segurança)", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "Dimensionamento de Condutores: Baseado na capacidade recomendada, considerando fatores de correção por temperatura e agrupamento conforme NBR 5410", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "Sistemas de Proteção: Ajustes baseados no P95 com coordenação seletiva para garantir continuidade do serviço", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"Fator de Demanda Global: {(pico_95 / (pico_medio * 1.2)):.2f} para aplicação em projetos similares", align="J")
    pdf.ln(10)

    # 7. Conclusões e Considerações Finais
    pdf.set_font("Times", "B", 14)
    pdf.multi_cell(190, 10, "7. CONCLUSÕES E CONSIDERAÇÕES FINAIS", align="J")
    pdf.set_font("Times", "", 12)
    pdf.set_x(pdf.l_margin)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"A simulação Monte Carlo realizada com {num_simulacoes:,} cenários independentes fornece uma base estatisticamente robusta para o dimensionamento da infraestrutura elétrica do estabelecimento hoteleiro. A metodologia de instâncias individualizadas permite capturar adequadamente o fator de diversidade, resultando em dimensionamentos mais precisos e economicamente otimizados.", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "Os resultados apresentados baseiam-se nas configurações de equipamentos e padrões de uso fornecidos. Mudanças significativas no perfil de ocupação, introdução de novos tipos de equipamentos ou alterações nos hábitos dos usuários podem impactar os resultados e requerem reavaliação da simulação.", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, f"A capacidade recomendada de {capacidade_recomendada:.0f} W (baseada no P95 com margem de segurança) oferece um equilíbrio adequado entre confiabilidade operacional e viabilidade econômica. Esta recomendação considera as melhores práticas da engenharia elétrica e está alinhada com normas técnicas nacionais e internacionais.", align="J")
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(190, 7, "Recomenda-se fortemente a implementação de sistemas de monitoramento contínuo para validação dos resultados e refinamento progressivo dos modelos de simulação. Esta abordagem permite otimização contínua da operação e identificação precoce de necessidades de adequação da infraestrutura.", align="J")
    pdf.ln(10)

    # Rodapé
    pdf.set_font("Times", "I", 10)
    pdf.multi_cell(190, 6, "Relatório Técnico Gerado Automaticamente", align="C")
    pdf.multi_cell(190, 6, "Sistema: Simulação Monte Carlo com Instâncias Individualizadas", align="C")
    pdf.multi_cell(190, 6, "Desenvolvido por Matheus Vianna | matheusvianna.com", align="C", link="https://matheusvianna.com")
    pdf.multi_cell(190, 6, f"Análise baseada em {num_simulacoes:,} simulações independentes | Metodologia validada conforme práticas da engenharia elétrica", align="C")
    pdf.multi_cell(190, 6, "Para questões técnicas ou esclarecimentos adicionais, consulte a documentação técnica do sistema", align="C")

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()

# --- Interface do Streamlit ---

# Seção 1: Configuração de Dados
st.header("⚙️ Configuração de Dados")

# Opção de entrada de dados
entrada_dados = st.radio(
    "Método de entrada de dados:",
    ["📁 Upload de arquivo Excel", "✏️ Entrada direta de dados"],
    help="Escolha como deseja inserir os dados dos cômodos",
    horizontal=True
)

if entrada_dados == "📁 Upload de arquivo Excel":
    # Upload do arquivo Excel
    uploaded_file = st.file_uploader(
        "Carregar arquivo Excel com dados dos cômodos",
        type=["xlsx", "xls"],
        help="O arquivo deve conter abas com os nomes dos cômodos e colunas: Equipamento, Potência, Quantidade, Tipo de intervalo, intervalo, probabilidade, FD (+ duracao_min/duracao_max opcionais)"
    )
    
    if uploaded_file is not None:
        try:
            # Carrega os cômodos do arquivo Excel
            if "comodos" not in st.session_state or st.session_state.get("data_source") != "excel":
                st.session_state.comodos = cria_comodos_do_excel(uploaded_file)
                st.session_state.data_source = "excel"
            
            # Mostra informações sobre os cômodos carregados
            st.success(f"✅ {len(st.session_state.comodos)} cômodos carregados:")
            for comodo in st.session_state.comodos:
                st.write(f"- {comodo.nome}")
                
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
            st.info("Verifique se o arquivo Excel possui o formato correto com as colunas necessárias.")

else:  # Entrada direta de dados
    st.subheader("✏️ Entrada direta de dados")
    
    # Inicializa o estado se necessário
    if "comodos_data" not in st.session_state:
        st.session_state.comodos_data = {}
    
    # Número de tipos de cômodos
    num_comodos = st.number_input(
        "Número de tipos de cômodos:",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )
    
    # Interface para cada tipo de cômodo
    for i in range(num_comodos):
        with st.expander(f"🏠 Cômodo {i+1}"):
            comodo_nome = st.text_input(
                f"Nome do cômodo {i+1}:",
                value=f"Quarto {i+1}",
                key=f"nome_comodo_{i}"
            )
            
            num_equipamentos = st.number_input(
                f"Número de equipamentos:",
                min_value=1,
                max_value=10,
                value=3,
                step=1,
                key=f"num_eq_{i}"
            )
            
            # Dados dos equipamentos para este cômodo
            equipamentos_data = []
            for j in range(num_equipamentos):
                st.write(f"**Equipamento {j+1}:**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    nome_eq = st.text_input(
                        "Nome:",
                        value=f"Equipamento {j+1}",
                        key=f"nome_eq_{i}_{j}"
                    )
                    
                    potencia = st.number_input(
                        "Potência (W):",
                        min_value=1,
                        max_value=10000,
                        value=100,
                        step=10,
                        key=f"pot_{i}_{j}"
                    )
                
                with col2:
                    quantidade = st.number_input(
                        "Quantidade:",
                        min_value=1,
                        max_value=50,
                        value=1,
                        step=1,
                        key=f"qtd_{i}_{j}"
                    )
                    
                    tipo_intervalo = st.selectbox(
                        "Tipo de intervalo:",
                        ["fixo", "dinâmico"],
                        key=f"tipo_{i}_{j}"
                    )
                
                with col3:
                    if tipo_intervalo == "fixo":
                        intervalo = st.text_input(
                            "Intervalo (HH:MM as HH:MM):",
                            value="08:00 as 18:00",
                            key=f"int_{i}_{j}"
                        )
                    else:
                        intervalo = st.text_input(
                            "Intervalo dinâmico:",
                            value="Início entre 08:00-10:00, duração 8",
                            key=f"int_{i}_{j}"
                        )
                    
                    probabilidade = st.slider(
                        "Probabilidade:",
                        min_value=0.0,
                        max_value=1.0,
                        value=1.0,
                        step=0.1,
                        key=f"prob_{i}_{j}"
                    )
                    
                    fd = st.slider(
                        "Fator de Demanda:",
                        min_value=0.1,
                        max_value=1.0,
                        value=1.0,
                        step=0.1,
                        key=f"fd_{i}_{j}"
                    )

                    duracao_min = st.number_input(
                        "Duração mínima (h, opcional):",
                        min_value=0.0,
                        max_value=24.0,
                        value=0.0,
                        step=0.5,
                        key=f"dur_min_{i}_{j}",
                        help="Se >0, ativa duração intervalar com janela definida em 'intervalo'."
                    )
                    duracao_max = st.number_input(
                        "Duração máxima (h, opcional):",
                        min_value=0.0,
                        max_value=24.0,
                        value=0.0,
                        step=0.5,
                        key=f"dur_max_{i}_{j}"
                    )

                    modo_fixo = "FIXO_100%"
                    if tipo_intervalo == "fixo":
                        modo_fixo = st.selectbox(
                            "Modo fixo:",
                            ["FIXO_100%", "FIXO_DURACAO_INTERVALAR"],
                            key=f"modo_fixo_{i}_{j}",
                        )
                
                row = {
                    "Equipamento": nome_eq,
                    "Potência": potencia,
                    "Quantidade": quantidade,
                    "Tipo de intervalo": tipo_intervalo,
                    "intervalo": intervalo,
                    "probabilidade": probabilidade,
                    "FD": fd,
                }
                if duracao_min > 0 and duracao_max > 0:
                    row["duracao_min"] = duracao_min
                    row["duracao_max"] = duracao_max
                if tipo_intervalo == "fixo":
                    row["modo_fixo"] = modo_fixo
                equipamentos_data.append(row)
            
            # Armazena os dados do cômodo
            st.session_state.comodos_data[comodo_nome] = pd.DataFrame(equipamentos_data)
    
    # Botão para processar dados inseridos
    if st.button("📝 Processar Dados Inseridos", type="primary"):
        try:
            # Cria os cômodos a partir dos dados inseridos
            st.session_state.comodos = cria_comodos_do_dataframe(st.session_state.comodos_data)
            st.session_state.data_source = "manual"
            
            st.success(f"✅ {len(st.session_state.comodos)} cômodos processados:")
            for comodo in st.session_state.comodos:
                st.write(f"- {comodo.nome}")
                
        except Exception as e:
            st.error(f"Erro ao processar dados: {str(e)}")

# Continua apenas se houver cômodos carregados
if "comodos" in st.session_state and st.session_state.comodos:
    
    # Seção 2: Parâmetros de Simulação
    st.header("🎯 Parâmetros de Simulação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_simulacoes = st.slider(
            "Número de simulações",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Maior número de simulações = resultados mais precisos, mas processamento mais lento"
        )
    
    with col2:
        tempo_total = st.slider(
            "Tempo total (minutos)",
            min_value=60,
            max_value=1440,
            value=1440,
            step=60,
            help="1440 minutos = 24 horas (1 dia completo)"
        )
    
    # Seção 3: Instâncias por Cômodo
    st.header("🏠 Instâncias por Cômodo")
    
    instancias_por_comodo = {}
    
    # Organiza em colunas para melhor layout
    num_cols = min(3, len(st.session_state.comodos))
    cols = st.columns(num_cols)
    
    for idx, comodo in enumerate(st.session_state.comodos):
        col_idx = idx % num_cols
        with cols[col_idx]:
            instancias_por_comodo[comodo.nome] = st.number_input(
                f"{comodo.nome}",
                min_value=1,
                max_value=200,
                value=1,
                step=1,
                key=f"inst_{comodo.nome}"
            )
    
    # Seção 4: Executar Simulação
    st.header("🚀 Executar Simulação")
    
    if st.button("🚀 Executar Simulação Monte Carlo", type="primary", use_container_width=True):
        with st.spinner("Executando simulação Monte Carlo..."):
            # Executa a simulação principal
            picos, perfis, consumos = simula_carga_total(
                st.session_state.comodos,
                instancias_por_comodo,
                num_simulacoes=num_simulacoes,
                tempo_total=tempo_total
            )
            
            # Armazena os resultados no session_state
            st.session_state.resultados = {
                "picos": picos,
                "perfis": perfis,
                "consumos": consumos,
                "instancias_por_comodo": instancias_por_comodo,
                "num_simulacoes": num_simulacoes,
                "tempo_total": tempo_total
            }
        
        st.success("✅ Simulação concluída!")
    
    # Seção 5: Resultados (exibidos abaixo se disponíveis)
    if "resultados" in st.session_state:
        st.header("📊 Resultados da Simulação")
        
        resultados = st.session_state.resultados
        picos = resultados["picos"]
        perfis = resultados["perfis"]
        consumos = resultados["consumos"]
        
        # Estatísticas dos picos
        pico_medio = np.mean(picos)
        pico_max = np.max(picos)
        pico_min = np.min(picos)
        pico_95 = np.percentile(picos, 95)
        
        # Botões para geração de relatórios
        col_relatorio1, col_relatorio2, col_relatorio3 = st.columns([2, 1, 1])

        with col_relatorio2:
            if st.button("📄 Gerar Relatório PDF", type="secondary"):
                with st.spinner("Gerando relatório PDF técnico..."):
                    imagens_graficos = gerar_graficos_relatorio(
                        picos,
                        perfis,
                        pico_medio,
                        pico_95,
                        tempo_total,
                        num_simulacoes,
                        st.session_state.comodos,
                        instancias_por_comodo
                    )

                    pdf_data = gerar_pdf_relatorio(
                        resultados,
                        instancias_por_comodo,
                        num_simulacoes,
                        tempo_total,
                        imagens_graficos,
                        st.session_state.comodos_data if st.session_state.data_source == "manual" else None,
                        st.session_state.comodos
                    )

                    b64_pdf = base64.b64encode(pdf_data).decode("latin1")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="relatorio_tecnico_monte_carlo.pdf">📥 Download do Relatório Técnico PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("✅ Relatório técnico PDF gerado com sucesso!")

        with col_relatorio3:
            if st.button("🧾 Gerar ZIP LaTeX", type="secondary"):
                with st.spinner("Gerando pacote ZIP com relatório em LaTeX e imagens..."):
                    imagens_graficos = gerar_graficos_relatorio(
                        picos,
                        perfis,
                        pico_medio,
                        pico_95,
                        tempo_total,
                        num_simulacoes,
                        st.session_state.comodos,
                        instancias_por_comodo
                    )

                    zip_data = gerar_zip_relatorio_latex(
                        resultados,
                        instancias_por_comodo,
                        num_simulacoes,
                        tempo_total,
                        imagens_graficos,
                        st.session_state.comodos_data if st.session_state.data_source == "manual" else None,
                        st.session_state.comodos
                    )

                    st.download_button(
                        label="📥 Baixar ZIP do Relatório LaTeX",
                        data=zip_data,
                        file_name="relatorio_monte_carlo_latex.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    st.success("✅ Pacote ZIP com .tex e imagens gerado com sucesso!")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pico Médio", f" {pico_medio:.0f} W")
        
        with col2:
            st.metric("Pico Máximo", f" {pico_max:.0f} W")
        
        with col3:
            st.metric("Pico Mínimo", f" {pico_min:.0f} W")
        
        with col4:
            st.metric("Percentil 95", f" {pico_95:.0f} W")
        
        # Tabs para diferentes análises (removida a aba "Variação da Carga")
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Distribuição dos Picos",
            "📈 Curva de Duração",
            "⚡ Perfil de Carga",
            "📈 Potência Cumulativa por Cômodo"
        ])
        
        with tab1:
            st.subheader("Distribuição Global dos Picos de Carga")
            st.write("Este histograma apresenta a distribuição estatística dos picos de demanda elétrica obtidos através das simulações Monte Carlo. A análise da forma da distribuição fornece insights sobre a previsibilidade do comportamento da carga: distribuições mais concentradas (baixo desvio padrão) indicam comportamento mais previsível, enquanto distribuições mais dispersas sugerem maior variabilidade operacional. A linha vermelha tracejada representa a demanda média máxima esperada, enquanto a linha verde indica o percentil 95 (P95), valor amplamente utilizado na engenharia elétrica como referência para dimensionamento de transformadores e sistemas de proteção, pois garante que 95% dos cenários simulados apresentem demanda inferior a este valor.")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(picos, bins=30, alpha=0.7, edgecolor="black", density=True, color="#3498db")
            ax.axvline(pico_medio, color="red", linestyle="dashed", linewidth=2, label=f"Média: {pico_medio:.0f} W")
            ax.axvline(pico_95, color="green", linestyle="dashed", linewidth=2, label=f"P95: {pico_95:.0f} W")
            ax.set_title("Distribuição Global dos Picos de Carga")
            ax.set_xlabel("Pico de Carga (W)")
            ax.set_ylabel("Frequência Normalizada")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Probabilidade de Excedência dos Picos
            st.subheader("Probabilidade de Excedência dos Picos")
            st.write("Este gráfico mostra a probabilidade de um determinado pico de carga ser excedido. É uma ferramenta importante para avaliar o risco de sobrecarga e para o dimensionamento de sistemas de proteção.")
            
            picos_sorted = np.sort(picos)
            prob_excedencia = 1 - (np.arange(1, len(picos_sorted) + 1) / len(picos_sorted))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(picos_sorted, prob_excedencia * 100, label="Probabilidade de Excedência", linewidth=2, color="#e74c3c")
            ax.set_title("Probabilidade de Excedência dos Picos Diários")
            ax.set_xlabel("Pico de Carga (W)")
            ax.set_ylabel("Probabilidade de Excedência (%)")
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        
        with tab2:
            st.subheader("Curva de Duração de Carga (Load Duration Curve)")
            st.write("A Curva de Duração de Carga apresenta os valores de demanda em ordem decrescente, revelando por quanto tempo cada nível de carga é mantido. É essencial para estudos de viabilidade econômica e dimensionamento de sistemas de armazenamento de energia.")
            
            todas_cargas = np.concatenate(perfis)
            todas_cargas_sorted = np.sort(todas_cargas)[::-1]
            frac_tempo = np.arange(1, len(todas_cargas_sorted) + 1) / len(todas_cargas_sorted)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(frac_tempo * 100, todas_cargas_sorted, label="Curva de Duração", linewidth=2, color="#9b59b6")
            ax.set_title("Curva de Duração de Carga (Hotel)")
            ax.set_xlabel("Fração do Tempo (%)")
            ax.set_ylabel("Carga (W)")
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        
        with tab3:
            st.subheader("Perfil de Carga Médio ao Longo do Dia")
            st.write("Este gráfico exibe o comportamento típico da demanda elétrica durante um ciclo diário, revelando padrões de consumo e horários de pico. É fundamental para o planejamento operacional e estratégias de gestão energética.")
            
            media_por_minuto = np.mean(perfis, axis=0)
            horas = np.arange(tempo_total) / 60.0
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(horas, media_por_minuto, linewidth=2, label="Carga Média", color='#2c3e50')
            ax.fill_between(horas, media_por_minuto, alpha=0.3, color='#3498db')
            ax.set_xlabel("Hora do Dia")
            ax.set_ylabel("Carga (W)")
            ax.set_title("Perfil de Carga Médio Durante o Dia")
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
            
            # Fator de Carga por Hora
            st.subheader("Fator de Carga por Hora do Dia")
            st.write("O fator de carga indica a eficiência da utilização da capacidade elétrica em cada hora. Valores mais altos sugerem uso mais consistente da infraestrutura.")
            
            pico_por_minuto = np.max(perfis, axis=0)
            fator_carga_por_hora = []
            for h in range(24):
                inicio = h * 60
                fim = inicio + 60
                carga_media_h = np.mean(media_por_minuto[inicio:fim])
                pico_h = np.max(pico_por_minuto[inicio:fim])
                fator = carga_media_h / pico_h if pico_h > 0 else 0
                fator_carga_por_hora.append(fator)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(np.arange(24), fator_carga_por_hora, color='#f39c12', alpha=0.8)
            ax.set_xlabel("Hora do Dia")
            ax.set_ylabel("Fator de Carga")
            ax.set_title("Fator de Carga por Hora do Dia")
            ax.set_xticks(np.arange(24))
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)
        
        with tab4:
            st.subheader("Gráfico de Potência Cumulativa por Cômodo")
            st.write("Este gráfico de área empilhada mostra a contribuição de cada tipo de cômodo para a demanda total, permitindo identificar os maiores consumidores e orientar estratégias de eficiência energética.")
            
            # Calcula a carga média de cada cômodo individualmente
            comodos_cargas_medias = {}
            for comodo_obj in st.session_state.comodos:
                comodo_copia = copy.deepcopy(comodo_obj)
                instancias_para_comodo = {comodo_copia.nome: instancias_por_comodo.get(comodo_copia.nome, 1)}
                _, perfis_comodo, _ = simula_carga_total(
                    [comodo_copia],
                    instancias_para_comodo,
                    num_simulacoes=num_simulacoes,
                    tempo_total=tempo_total
                )
                comodos_cargas_medias[comodo_obj.nome] = np.mean(perfis_comodo, axis=0)

            if comodos_cargas_medias:
                horas = np.arange(tempo_total) / 60.0
                
                fig, ax = plt.subplots(figsize=(14, 8))
                comodos_nomes = list(comodos_cargas_medias.keys())
                comodos_valores = [comodos_cargas_medias[nome] for nome in comodos_nomes]
                
                ax.stackplot(horas, *comodos_valores, labels=comodos_nomes, alpha=0.8)
                ax.set_xlabel("Hora do Dia")
                ax.set_ylabel("Potência (W)")
                ax.set_title("Potência Cumulativa por Cômodo ao Longo do Dia")
                ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("Não foi possível gerar o gráfico de potência cumulativa por cômodo. Verifique a configuração dos cômodos.")

else:
    if entrada_dados == "📁 Upload de arquivo Excel":
        st.info("👆 Por favor, carregue um arquivo Excel acima para começar a simulação.")
        
        # Exemplo de formato esperado
        st.subheader("📋 Formato Esperado do Arquivo Excel")
        
        exemplo_df = pd.DataFrame({
            'Equipamento': ['Ar Condicionado', 'Iluminação', 'TV'],
            'Potência': [2000, 100, 150],
            'Quantidade': [1, 4, 1],
            'Tipo de intervalo': ['dinâmico', 'fixo', 'fixo'],
            'intervalo': ['07:00 as 22:00', '18:00 as 23:00', '19:00 as 23:00'],
            'probabilidade': [0.8, 1.0, 0.9],
            'FD': [0.8, 1.0, 1.0],
            'duracao_min': [1.0, np.nan, np.nan],
            'duracao_max': [3.0, np.nan, np.nan],
            'modo_fixo': [np.nan, 'FIXO_100%', 'FIXO_DURACAO_INTERVALAR']
        })
        
        st.dataframe(exemplo_df)
        
        st.markdown("""
        **Instruções:**
        - Cada aba do Excel deve representar um tipo de cômodo (ex: "Quarto 1", "Quarto 3", etc.)
        - As colunas obrigatórias são: Equipamento, Potência, Quantidade, Tipo de intervalo, intervalo, probabilidade, FD
        - Colunas opcionais para duração intervalar: **duracao_min** e **duracao_max** (em horas).
        - Compatibilidade: se usar apenas **duracao** (legado), o sistema mapeia para min=max.
        - Para tipo **fixo**, a coluna opcional **modo_fixo** aceita: `FIXO_100%` ou `FIXO_DURACAO_INTERVALAR`.
        - **Tipo de intervalo**: "fixo" ou "dinâmico"
        - **intervalo**: para duração intervalar use janela no formato "HH:MM as HH:MM".
        - **probabilidade**: Valor entre 0 e 1 (probabilidade do equipamento estar ligado)
        - **FD**: Fator de demanda (valor entre 0 e 1)
        """)
    else:
        st.info("👆 Por favor, configure os dados dos cômodos acima e clique em 'Processar Dados Inseridos'.")

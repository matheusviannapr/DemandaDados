# Simulação Monte Carlo para Análise de Carga Elétrica em Hotel

Sistema avançado de simulação Monte Carlo para dimensionamento de infraestrutura elétrica em estabelecimentos hoteleiros.

## 🎯 Objetivo

Este aplicativo utiliza a técnica de **Simulação Monte Carlo** para analisar o comportamento da carga elétrica em hotéis, considerando a variabilidade natural do uso de equipamentos pelos hóspedes. O sistema simula milhares de cenários diferentes para fornecer estatísticas confiáveis para o dimensionamento da infraestrutura elétrica.

## 🚀 Como Executar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Aplicativo

```bash
streamlit run monte_carlo_hotel_app_final_v3.py
```

### 3. Acessar no Navegador

O aplicativo será aberto automaticamente no navegador em `http://localhost:8501`

## 📁 Arquivos Incluídos

- `monte_carlo_hotel_app_final_v3.py` - Aplicativo Streamlit principal
- `exemplo_hotel.xlsx` - Arquivo Excel de exemplo para testes
- `logo_demanda_dados.png` - Logo do aplicativo
- `requirements.txt` - Dependências Python necessárias
- `README.md` - Este arquivo de instruções

## 🔧 Funcionalidades

### Entrada de Dados
- **Upload de Excel**: Carregue arquivos Excel com configuração dos cômodos
- **Entrada Direta**: Interface para inserir dados diretamente no aplicativo

### Simulação Monte Carlo
- Instâncias individualizadas de cada cômodo
- Variabilidade temporal com intervalos fixos ou dinâmicos
- Fatores probabilísticos e de demanda
- Análise estatística avançada

### Resultados e Análises
- Distribuição dos picos de carga
- Curva de duração de carga
- Perfil de carga médio
- Potência cumulativa por cômodo
- Relatório PDF técnico completo

## 📊 Formato do Arquivo Excel

O arquivo Excel deve conter abas nomeadas pelos tipos de cômodos com as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| Equipamento | Nome do equipamento | "Ar Condicionado" |
| Potência | Potência nominal em watts | 2000 |
| Quantidade | Número de unidades | 1 |
| Tipo de intervalo | "fixo" ou "dinâmico" | "dinâmico" |
| intervalo | Período de funcionamento | "Início entre 14:00-18:00, duração 6" |
| probabilidade | Chance de estar ligado (0.0-1.0) | 0.8 |
| FD | Fator de demanda (0.1-1.0) | 0.8 |

## 🎨 Características Técnicas

- **Interface**: Streamlit com tema marinho personalizado
- **Simulação**: Monte Carlo com instâncias individualizadas
- **Relatórios**: PDF técnico com análises detalhadas
- **Visualizações**: Gráficos interativos e explicações técnicas

## 👨‍💻 Desenvolvedor

**Matheus Vianna**  
Engenheiro Especialista em Simulação Monte Carlo  
Website: [matheusvianna.com](https://matheusvianna.com)

## 📄 Licença

© 2025 - Todos os direitos reservados

## 🆘 Suporte

Para questões técnicas ou esclarecimentos, consulte a documentação técnica do sistema ou entre em contato através do website oficial.


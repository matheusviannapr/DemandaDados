# Demanda e Dádio (MVP Streamlit)

Plataforma de modelagem e simulação de demanda elétrica com foco em:
- Cenários e equipamentos persistidos em banco de dados
- Perfis de consumo e sazonalidade
- Simulação Monte Carlo vetorizada com NumPy
- Interface multipágina em Streamlit

## Banco de dados (SQLite local ou Neon/PostgreSQL)

Por padrão, o app usa SQLite local em `data/demanda.db`.

Para persistência em nuvem (Neon), defina `DATABASE_URL` antes de iniciar:

```bash
export DATABASE_URL='postgresql+psycopg://USER:SENHA@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require'
streamlit run monte_carlo_hotel_app_final_v3.py
```

Sem `DATABASE_URL`, o fallback é SQLite local.

## Executar

```bash
pip install -r requirements.txt
streamlit run monte_carlo_hotel_app_final_v3.py
```

## Seed opcional

```bash
python -m app.db.seed
```

## Estrutura

- `app/core`: modelos, parser, sazonalidade e simulação
- `app/db`: conexão, schema e repositórios
- `app/pages`: fluxo do usuário (upload até resultados)
- `app/ui`: componentes reutilizáveis da interface


> Entry point padrão para deploy atual: `monte_carlo_hotel_app_final_v3.py` (agora apontando para a arquitetura modular).

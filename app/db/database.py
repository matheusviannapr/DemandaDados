from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.db.schema import get_schema_sql


@st.cache_resource(show_spinner=False)
def get_engine(database_url: str | None = None) -> Engine:
    db_url = database_url or os.getenv("DATABASE_URL") or "sqlite:///data/demanda.db"
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgresql://") and "+" not in db_url.split("://", 1)[0]:
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if db_url.startswith("sqlite"):
        Path("data").mkdir(parents=True, exist_ok=True)

    engine = create_engine(db_url, future=True, pool_pre_ping=True)
    dialect = engine.url.get_backend_name()
    schema_sql = get_schema_sql(dialect)

    with engine.begin() as conn:
        if dialect == "sqlite":
            conn.execute(text("PRAGMA foreign_keys = ON"))
        for statement in [s.strip() for s in schema_sql.split(";") if s.strip()]:
            conn.execute(text(statement))
    return engine

from __future__ import annotations

import pandas as pd
import streamlit as st


def line_chart(values: list[float], y_label: str = "kW") -> None:
    df = pd.DataFrame({y_label: values})
    st.line_chart(df, use_container_width=True)


def histogram(values: list[float], label: str = "picos_kw") -> None:
    df = pd.DataFrame({label: values})
    st.bar_chart(df[label].value_counts(bins=20).sort_index())

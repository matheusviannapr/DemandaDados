from __future__ import annotations

import streamlit as st


def metric_cards(metrics: dict[str, str]) -> None:
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label, value)

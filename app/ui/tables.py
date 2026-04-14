from __future__ import annotations

import pandas as pd
import streamlit as st


def editable_dataframe(df: pd.DataFrame, key: str) -> pd.DataFrame:
    return st.data_editor(df, key=key, use_container_width=True, num_rows="dynamic")

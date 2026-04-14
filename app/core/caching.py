from __future__ import annotations

import streamlit as st


@st.cache_data(show_spinner=False)
def cache_bytes(content: bytes) -> bytes:
    return content

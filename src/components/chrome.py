"""Shared page framing and safety notice."""

import streamlit as st

from src.config.settings import PRODUCT_ICON, PRODUCT_NAME, PRODUCT_TAGLINE


def header() -> None:
    st.title(f"{PRODUCT_ICON} {PRODUCT_NAME}")
    st.caption(PRODUCT_TAGLINE)


def disclaimer() -> None:
    st.divider()
    st.caption("Med Key provides general educational information, not medical advice, diagnosis, or treatment. A licensed clinician should interpret your results in context. For urgent symptoms or concerns, seek appropriate medical care.")

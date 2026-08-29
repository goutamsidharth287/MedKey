"""Groq client adapter kept separate from presentation code."""

from collections.abc import Sequence

import streamlit as st
from groq import Groq

from src.config.settings import GROQ_MODEL, GROQ_RESPONSE_TOKEN_LIMIT, GROQ_TEMPERATURE


@st.cache_resource
def client() -> Groq:
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def complete(system_message: str, messages: Sequence[dict[str, str]]) -> str:
    response = client().chat.completions.create(
        model=GROQ_MODEL,
        temperature=GROQ_TEMPERATURE,
        max_tokens=GROQ_RESPONSE_TOKEN_LIMIT,
        messages=[{"role": "system", "content": system_message}, *messages],
    )
    text = response.choices[0].message.content
    if not text:
        raise RuntimeError("The AI service returned an empty response.")
    return text

"""Streamlit state lifecycle, intentionally independent of the database layer."""

import time

import streamlit as st

from src.config.settings import INACTIVITY_TIMEOUT_SECONDS

_DEFAULTS = {
    "signed_in": False,
    "account": None,
    "last_seen": 0.0,
    "active_record_id": None,
    "analysis": None,
    "report_text": None,
    "profile": None,
    "messages": [],
}


def initialize() -> None:
    for key, value in _DEFAULTS.items():
        st.session_state.setdefault(key, value)


def note_activity() -> None:
    st.session_state.last_seen = time.time()


def expired() -> bool:
    return bool(st.session_state.signed_in) and (
        time.time() - st.session_state.last_seen > INACTIVITY_TIMEOUT_SECONDS
    )


def clear_account() -> None:
    for key, value in _DEFAULTS.items():
        st.session_state[key] = value


def begin_new_report() -> None:
    for key in ("active_record_id", "analysis", "report_text", "profile"):
        st.session_state[key] = None
    st.session_state.messages = []

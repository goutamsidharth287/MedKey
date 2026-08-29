"""Sidebar for saved reports and account controls."""

import streamlit as st

from src.auth.repository import MedKeyRepository
from src.auth.state import begin_new_report, clear_account
from src.config.settings import ANALYSES_PER_DAY, PRODUCT_ICON, PRODUCT_NAME


def render() -> None:
    store = MedKeyRepository()
    account = st.session_state.account
    with st.sidebar:
        st.markdown(f"## {PRODUCT_ICON} {PRODUCT_NAME}")
        if st.button("New report", use_container_width=True, type="primary"):
            begin_new_report()
            st.rerun()
        used = store.usage(account.id)
        st.progress(min(used / ANALYSES_PER_DAY, 1.0), text=f"{used} of {ANALYSES_PER_DAY} reviews used today")
        st.divider()
        st.markdown("#### Saved reports")
        for record in store.list_reports(account.id):
            left, right = st.columns([5, 1])
            with left:
                if st.button(record.get("title") or "Untitled report", key=f"open_{record['id']}", use_container_width=True):
                    _open(store, record)
                    st.rerun()
            with right:
                if st.button("×", key=f"delete_{record['id']}", help="Delete report"):
                    store.delete_report(record["id"])
                    if st.session_state.active_record_id == record["id"]:
                        begin_new_report()
                    st.rerun()
        st.divider()
        if st.button("Sign out", use_container_width=True):
            store.logout()
            clear_account()
            st.rerun()


def _open(store: MedKeyRepository, record: dict) -> None:
    st.session_state.active_record_id = record["id"]
    st.session_state.analysis = record["analysis"]
    messages = store.messages_for(record["id"])
    st.session_state.messages = messages[1:] if messages and messages[0]["role"] == "assistant" else messages

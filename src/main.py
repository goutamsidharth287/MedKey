"""Med Key Streamlit entry point."""

import streamlit as st

from src.agents.report_chat import answer
from src.auth.repository import MedKeyRepository
from src.auth.state import begin_new_report, clear_account, expired, initialize, note_activity
from src.components.account import render as render_account
from src.components.chrome import disclaimer, header
from src.components.navigation import render as render_navigation
from src.components.report_upload import render as render_report_upload
from src.config.settings import PRODUCT_ICON, PRODUCT_NAME


def _conversation() -> None:
    st.subheader("Your report explanation")
    st.markdown(st.session_state.analysis)
    st.divider()
    st.subheader("Ask a follow-up question")
    st.caption("Questions are answered from the saved explanation and are not medical advice.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    question = st.chat_input("Ask about a value or term in this report")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    response = answer(question, st.session_state.analysis, st.session_state.messages)
                except Exception as exc:
                    response = f"I couldn't answer that question right now: {exc}"
                st.markdown(response)
        st.session_state.messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": response},
        ])
        if st.session_state.active_record_id:
            try:
                store = MedKeyRepository()
                store.save_message(st.session_state.active_record_id, "user", question)
                store.save_message(st.session_state.active_record_id, "assistant", response)
            except Exception:
                st.toast("Your response was not saved, but it remains visible this session.", icon="⚠️")


def main() -> None:
    st.set_page_config(page_title=PRODUCT_NAME, page_icon=PRODUCT_ICON, layout="centered")
    initialize()
    if expired():
        clear_account()
        st.warning("You were signed out after inactivity. Please sign in again.")

    header()
    if not st.session_state.signed_in:
        render_account()
        disclaimer()
        return

    note_activity()
    render_navigation()
    if st.session_state.analysis:
        _conversation()
    else:
        render_report_upload()
    disclaimer()


if __name__ == "__main__":
    main()

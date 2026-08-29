"""Sign-in and registration interface."""

import streamlit as st

from src.auth.repository import MedKeyRepository
from src.auth.state import note_activity


def render() -> None:
    store = MedKeyRepository()
    sign_in, create_account = st.tabs(["Sign in", "Create account"])

    with sign_in:
        with st.form("med_key_login"):
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            if not email or not password:
                st.error("Enter both your email address and password.")
            else:
                try:
                    response = store.login(email, password)
                    if not response.user:
                        st.error("We could not sign you in with those details.")
                    else:
                        st.session_state.signed_in = True
                        st.session_state.account = response.user
                        note_activity()
                        st.rerun()
                except Exception:
                    st.error("Sign-in failed. Check your details and try again.")

    with create_account:
        with st.form("med_key_register"):
            name = st.text_input("Display name")
            email = st.text_input("Email address", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", use_container_width=True)
        if submitted:
            if not all((name.strip(), email.strip(), password, confirm)):
                st.error("Complete every field to create an account.")
            elif len(password) < 8:
                st.error("Use a password with at least 8 characters.")
            elif password != confirm:
                st.error("The passwords do not match.")
            else:
                try:
                    store.register(email, password, name.strip())
                    st.success("Account created. Check your email if confirmation is enabled, then sign in.")
                except Exception:
                    st.error("We could not create the account. Try a different email or try again later.")

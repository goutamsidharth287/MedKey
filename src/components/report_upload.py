"""Report upload and review workflow."""

import streamlit as st
from pypdf import PdfReader

from src.agents.report_reviewer import review
from src.auth.repository import MedKeyRepository
from src.config.demo_report import DEMO_PATIENT, DEMO_REPORT
from src.config.settings import ANALYSES_PER_DAY, PDF_PAGE_LIMIT, PDF_SIZE_LIMIT_MB


def _read_pdf(uploaded_file) -> str:
    if uploaded_file.size > PDF_SIZE_LIMIT_MB * 1024 * 1024:
        raise ValueError(f"Choose a PDF smaller than {PDF_SIZE_LIMIT_MB} MB.")
    document = PdfReader(uploaded_file)
    return "\n".join((page.extract_text() or "") for page in document.pages[:PDF_PAGE_LIMIT]).strip()


def render() -> None:
    store = MedKeyRepository()
    account = st.session_state.account
    if not store.may_analyze(account.id):
        st.warning(f"You've used today's {ANALYSES_PER_DAY} report reviews. Please return tomorrow.")
        return

    st.subheader("Understand a lab report")
    st.caption("PDF text is processed to create an educational explanation. Do not upload an emergency record.")
    source = st.radio("Choose a report", ("Upload a PDF", "Try the demo"), horizontal=True)
    report_text = ""
    using_demo = source == "Try the demo"
    if using_demo:
        st.info("You are viewing a fictional demonstration report.")
        report_text = DEMO_REPORT
    else:
        uploaded = st.file_uploader("Lab report PDF", type="pdf")
        if uploaded:
            try:
                report_text = _read_pdf(uploaded)
                if not report_text:
                    st.error("No readable text was found in that PDF. A text-based PDF works best.")
            except Exception as exc:
                st.error(f"That PDF could not be read: {exc}")

    defaults = DEMO_PATIENT if using_demo else {"name": "", "age": 30, "sex": "Prefer not to say"}
    st.markdown("#### Optional profile")
    one, two, three = st.columns(3)
    with one:
        name = st.text_input("Name", value=defaults["name"])
    with two:
        age = st.number_input("Age", min_value=0, max_value=120, value=defaults["age"])
    with three:
        sex = st.selectbox("Sex", ("Female", "Male", "Intersex", "Prefer not to say"), index=("Female", "Male", "Intersex", "Prefer not to say").index(defaults["sex"]))

    if st.button("Explain my report", type="primary", use_container_width=True, disabled=not report_text):
        profile = {"name": name, "age": age, "sex": sex}
        with st.spinner("Preparing an easy-to-read explanation…"):
            try:
                analysis = review(report_text, profile)
            except Exception as exc:
                st.error(f"The report explanation could not be created: {exc}")
                return
        st.session_state.report_text = report_text
        st.session_state.profile = profile
        st.session_state.analysis = analysis
        st.session_state.messages = []
        report_title = f"{name.strip() or 'Lab report'} — {age}"
        try:
            report_id = store.create_report(account.id, report_title, analysis)
            st.session_state.active_record_id = report_id
            store.save_message(report_id, "assistant", analysis)
            store.record_analysis(account.id)
        except Exception as exc:
            st.warning(f"Your explanation is ready, but it could not be saved: {exc}")
        st.rerun()

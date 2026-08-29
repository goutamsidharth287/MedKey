"""Supabase operations for accounts and saved report conversations."""

from datetime import UTC, date, datetime

import streamlit as st
from supabase import Client, create_client

from src.config.settings import ANALYSES_PER_DAY


@st.cache_resource
def database() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


class MedKeyRepository:
    def __init__(self) -> None:
        self.db = database()

    def register(self, email: str, password: str, display_name: str):
        return self.db.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}},
        })

    def login(self, email: str, password: str):
        return self.db.auth.sign_in_with_password({"email": email, "password": password})

    def logout(self) -> None:
        self.db.auth.sign_out()

    def usage(self, user_id: str) -> int:
        record = self.db.table("profiles").select("analysis_count, analysis_date").eq("id", user_id).single().execute().data
        if not record or record.get("analysis_date") != str(date.today()):
            self.db.table("profiles").update({"analysis_count": 0, "analysis_date": str(date.today())}).eq("id", user_id).execute()
            return 0
        return int(record.get("analysis_count") or 0)

    def may_analyze(self, user_id: str) -> bool:
        return self.usage(user_id) < ANALYSES_PER_DAY

    def record_analysis(self, user_id: str) -> None:
        self.db.table("profiles").update({"analysis_count": self.usage(user_id) + 1, "analysis_date": str(date.today())}).eq("id", user_id).execute()

    def create_report(self, user_id: str, title: str, analysis: str) -> str:
        result = self.db.table("report_sessions").insert({"user_id": user_id, "title": title, "analysis": analysis}).execute()
        return result.data[0]["id"]

    def list_reports(self, user_id: str) -> list[dict]:
        result = self.db.table("report_sessions").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
        return result.data or []

    def delete_report(self, report_id: str) -> None:
        self.db.table("report_sessions").delete().eq("id", report_id).execute()

    def save_message(self, report_id: str, role: str, content: str) -> None:
        self.db.table("report_messages").insert({"report_id": report_id, "role": role, "content": content}).execute()
        self.db.table("report_sessions").update({"updated_at": datetime.now(UTC).isoformat()}).eq("id", report_id).execute()

    def messages_for(self, report_id: str) -> list[dict]:
        return self.db.table("report_messages").select("role, content").eq("report_id", report_id).order("created_at").execute().data or []

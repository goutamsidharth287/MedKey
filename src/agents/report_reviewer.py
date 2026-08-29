"""Creates an educational explanation of extracted lab-report text."""

from src.config.prompts import REPORT_REVIEW_PROMPT, build_report_request
from src.services.llm import complete


def review(report_text: str, profile: dict[str, object]) -> str:
    request = build_report_request(report_text, profile)
    return complete(REPORT_REVIEW_PROMPT, [{"role": "user", "content": request}])

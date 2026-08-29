"""Answers questions while grounding every turn in the existing explanation."""

from src.config.prompts import FOLLOW_UP_PROMPT
from src.services.llm import complete


def answer(question: str, analysis: str, conversation: list[dict[str, str]]) -> str:
    recent_turns = conversation[-10:]
    return complete(
        FOLLOW_UP_PROMPT.format(analysis=analysis),
        [*recent_turns, {"role": "user", "content": question}],
    )

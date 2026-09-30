import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json(text: str) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(
    content: str
) -> list[dict[str, Any]]:

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational content below.

Return ONLY valid JSON.

Do not use Markdown.

Required format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A",
    "explanation": "Short explanation"
  }}
]

Rules:

- Exactly 3 questions.
- Exactly 4 options for every question.
- Only one correct answer.
- Questions must be based on the provided content.
- Use simple student-friendly English.

Educational Content:

{content}
"""

    raw_response = generate_text(
        prompt,
        temperature=0.2
    )

    try:

        data = json.loads(
            clean_json(raw_response)
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "The AI returned an invalid quiz format. "
            "Please try again."
        ) from error

    if not isinstance(data, list):

        raise RuntimeError(
            "Quiz response is not a list."
        )

    if len(data) != 3:

        raise RuntimeError(
            "The quiz must contain exactly 3 questions."
        )

    for question in data:

        if not isinstance(question, dict):

            raise RuntimeError(
                "Invalid quiz question."
            )

        if not isinstance(
            question.get("question"),
            str
        ):

            raise RuntimeError(
                "Invalid question text."
            )

        options = question.get(
            "options"
        )

        if not isinstance(
            options,
            list
        ) or len(options) != 4:

            raise RuntimeError(
                "Each question must have exactly 4 options."
            )

        if question.get(
            "answer"
        ) not in options:

            raise RuntimeError(
                "Correct answer is not one of the options."
            )

    return data
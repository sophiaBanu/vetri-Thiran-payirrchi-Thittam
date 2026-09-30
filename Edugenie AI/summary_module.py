from gemini_client import generate_text


def summarize_text(content: str) -> str:

    prompt = f"""
You are EduGenie, an educational assistant.

Summarize the following educational content.

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple English.
- Make it useful for quick revision.
- Do not add information that is not present
  in the original content.

Content:

{content}
"""

    return generate_text(
        prompt,
        temperature=0.2
    )
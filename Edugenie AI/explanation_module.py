from gemini_client import generate_text


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie, an educational assistant.

Explain the following topic in simple,
beginner-friendly English.

Use this structure:

1. Definition
2. Key points
3. Simple example
4. Real-life or academic use

Topic:

{topic}
"""

    return generate_text(
        prompt,
        temperature=0.25
    )
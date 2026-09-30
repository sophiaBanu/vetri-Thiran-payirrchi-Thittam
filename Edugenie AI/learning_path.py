from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    prompt = f"""
You are EduGenie, an educational learning-path assistant.

Create a structured learning path for:

{topic}

Organize the learning path into:

1. Prerequisites
2. Beginner Level
3. Intermediate Level
4. Advanced Level
5. Practice Activities
6. Recommended Resource Types
7. Suggested Learning Order

Keep the plan suitable for a student.

Use simple English.

Explain what the learner should learn
at each stage.
"""

    return generate_text(
        prompt,
        temperature=0.35
    )
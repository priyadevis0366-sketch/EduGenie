from ai_client import generate_text


def get_learning_recommendations(topic, level="Beginner"):
    prompt = (
        f"Create a practical learning plan for the topic '{topic}' for a {level.lower()} learner. "
        "Give 4 to 6 ordered stages. For each stage include a goal, what to study, and a small "
        "practice task. End with a simple way to check progress. Keep it specific and achievable."
    )
    return generate_text(prompt)
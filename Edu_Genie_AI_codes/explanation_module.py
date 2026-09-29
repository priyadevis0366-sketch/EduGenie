from ai_client import generate_text


def explain_topic(text):
    prompt = (
        "Explain this topic to a student in plain language. Start with the core idea, "
        "then give a concrete example and finish with one short takeaway. "
        "Keep the explanation accurate and avoid assuming prior knowledge.\n\n"
        f"Topic or source material:\n{text}"
    )
    return generate_text(prompt)
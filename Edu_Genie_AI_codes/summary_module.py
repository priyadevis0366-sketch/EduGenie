from ai_client import generate_text


def summarize_text(text):
    prompt = (
        "Summarize the material for a student. Preserve the key facts and important "
        "relationships, remove repetition, and use a short heading with concise bullets.\n\n"
        f"Material:\n{text}"
    )
    return generate_text(prompt)
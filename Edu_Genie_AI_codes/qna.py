from ai_client import generate_text


def answer_question(text):
    prompt = (
        "You are EduGenie, a supportive and accurate learning assistant. "
        "Answer the student's question clearly, explain important reasoning, "
        "and mention uncertainty rather than inventing facts.\n\n"
        f"Student question or notes:\n{text}"
    )
    return generate_text(prompt)
import json

from ai_client import generate_text


def _decode_quiz(response):
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end < start:
        raise ValueError("The quiz response was not valid JSON. Please try again.")

    try:
        data = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError("The quiz response was not valid JSON. Please try again.") from exc

    questions = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(questions, list) or not questions:
        raise ValueError("The quiz response did not contain any questions. Please try again.")

    validated = []
    for item in questions[:10]:
        if not isinstance(item, dict):
            continue
        options = item.get("options")
        answer = item.get("answer")
        if not isinstance(item.get("question"), str) or not isinstance(options, list) or len(options) < 2:
            continue
        if isinstance(answer, str):
            try:
                answer = options.index(answer)
            except ValueError:
                continue
        if not isinstance(answer, int) or isinstance(answer, bool) or not 0 <= answer < len(options):
            continue
        if not all(isinstance(option, str) for option in options):
            continue
        validated.append({
            "question": item["question"],
            "options": options,
            "answer": answer,
            "explanation": str(item.get("explanation", "")),
        })

    if not validated:
        raise ValueError("The quiz response did not contain usable questions. Please try again.")
    return validated


def generate_quiz(text):
    prompt = (
        "Create 5 multiple-choice questions from the material below. Return only valid JSON "
        "with this shape: {\"questions\":[{\"question\":\"...\",\"options\":[\"...\",\"...\",\"...\",\"...\"],\"answer\":0,\"explanation\":\"...\"}]}. "
        "The answer must be a zero-based integer index into options. Make distractors plausible.\n\n"
        f"Study material:\n{text}"
    )
    return _decode_quiz(generate_text(prompt))
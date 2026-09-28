import json
from typing import Any

from flask import current_app

from ..schemas.question_schema import validate_exam_payload

PROMPT_TEMPLATE = """
Generate a strict JSON object only, with fields: title, subject, difficulty, questions.
Constraints:
- subject: {subject}
- difficulty: {difficulty}
- number_of_questions: {count}
- question_types_allowed: {types}
- categories/topics: {categories}
- Each question fields: id,type,question,options,correct_answer or correct_answers,explanation,category,difficulty,marks,negative_marks.
- Use type one of: single_choice,multiple_choice,true_false.
- Do not include markdown fences.
""".strip()


class GeminiGenerationError(Exception):
    pass


def _fallback_exam(subject: str, difficulty: str, count: int, qtypes: list[str], categories: list[str]) -> dict[str, Any]:
    questions = []
    for idx in range(1, count + 1):
        qtype = qtypes[(idx - 1) % len(qtypes)]
        category = categories[(idx - 1) % len(categories)] if categories else "General"
        if qtype == "true_false":
            questions.append(
                {
                    "id": f"q{idx}",
                    "type": "true_false",
                    "question": f"{subject}: {category} concept statement {idx} is valid.",
                    "correct_answer": True,
                    "explanation": "Sample fallback question.",
                    "category": category,
                    "difficulty": difficulty.lower(),
                    "marks": 1,
                    "negative_marks": 0,
                }
            )
        elif qtype == "multiple_choice":
            options = ["A", "B", "C", "D"]
            questions.append(
                {
                    "id": f"q{idx}",
                    "type": "multiple_choice",
                    "question": f"Select all correct options for {subject} topic {category} ({idx}).",
                    "options": options,
                    "correct_answers": ["A", "C"],
                    "explanation": "Sample fallback question.",
                    "category": category,
                    "difficulty": difficulty.lower(),
                    "marks": 2,
                    "negative_marks": 0,
                }
            )
        else:
            options = ["Option A", "Option B", "Option C", "Option D"]
            questions.append(
                {
                    "id": f"q{idx}",
                    "type": "single_choice",
                    "question": f"{subject} question {idx} on {category}?",
                    "options": options,
                    "correct_answer": "Option A",
                    "explanation": "Sample fallback question.",
                    "category": category,
                    "difficulty": difficulty.lower(),
                    "marks": 1,
                    "negative_marks": 0,
                }
            )
    return {
        "title": f"{subject} Assessment",
        "subject": subject,
        "difficulty": difficulty.lower(),
        "questions": questions,
    }


def _call_gemini(prompt: str) -> dict[str, Any]:
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        raise GeminiGenerationError("GEMINI_API_KEY not configured")

    try:
        from google import genai
    except Exception as exc:  # pragma: no cover
        raise GeminiGenerationError("Google GenAI SDK is not installed") from exc

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=current_app.config.get("GEMINI_MODEL"),
            contents=prompt,
        )
        text = (response.text or "").strip()
        return json.loads(text)
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc


def generate_exam_questions(subject: str, difficulty: str, count: int, question_types: list[str], categories: list[str]) -> dict[str, Any]:
    prompt = PROMPT_TEMPLATE.format(
        subject=subject,
        difficulty=difficulty,
        count=count,
        types=", ".join(question_types),
        categories=", ".join(categories) if categories else "General",
    )

    retries = max(0, current_app.config.get("QUESTION_GENERATION_RETRIES", 2))
    last_error = None

    for _ in range(retries + 1):
        try:
            payload = _call_gemini(prompt)
            validated = validate_exam_payload(payload)
            return validated.model_dump()
        except Exception as exc:
            last_error = exc

    fallback = _fallback_exam(subject, difficulty, count, question_types, categories)
    try:
        validated = validate_exam_payload(fallback)
        return validated.model_dump()
    except Exception as exc:
        raise GeminiGenerationError(f"Generation failed: {last_error}; fallback invalid: {exc}") from exc

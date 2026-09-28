from .. import db
from ..models import Exam, Question


def create_exam_with_questions(payload: dict, question_count: int, time_limit_seconds: int) -> Exam:
    exam = Exam(
        title=payload["title"],
        subject=payload["subject"],
        difficulty=payload["difficulty"],
        question_count=question_count,
        time_limit_seconds=time_limit_seconds,
    )
    db.session.add(exam)
    db.session.flush()

    for q in payload["questions"]:
        correct_payload = q.get("correct_answers") if q["type"] == "multiple_choice" else q.get("correct_answer")
        question = Question(
            exam_id=exam.id,
            external_id=q["id"],
            qtype=q["type"],
            text=q["question"],
            options_json=q.get("options", []),
            correct_answer_json=correct_payload,
            explanation=q.get("explanation", ""),
            category=q.get("category", "General"),
            difficulty=q.get("difficulty", "medium"),
            marks=float(q.get("marks", 1)),
            negative_marks=float(q.get("negative_marks", 0)),
        )
        db.session.add(question)

    db.session.commit()
    return exam

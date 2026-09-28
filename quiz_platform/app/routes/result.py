from flask import Blueprint, abort, render_template, session

from ..models import Candidate, ExamAttempt
from ..services.analytics_service import attempt_insights

result_bp = Blueprint("result", __name__)


@result_bp.get("/result/<int:attempt_id>")
def view_result(attempt_id: int):
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    if session.get("candidate_id") and attempt.candidate_id != session.get("candidate_id"):
        abort(403)

    answers = sorted(attempt.answers, key=lambda a: a.question_id)
    status_counts = {"CORRECT": 0, "INCORRECT": 0, "PARTIALLY_CORRECT": 0, "UNANSWERED": 0}
    for a in answers:
        status_counts[a.status or "UNANSWERED"] = status_counts.get(a.status or "UNANSWERED", 0) + 1

    insights = attempt_insights(attempt)

    return render_template(
        "result.html",
        attempt=attempt,
        candidate=Candidate.query.get(attempt.candidate_id),
        answers=answers,
        status_counts=status_counts,
        insights=insights,
    )


@result_bp.get("/review/<int:attempt_id>")
def review(attempt_id: int):
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    if session.get("candidate_id") and attempt.candidate_id != session.get("candidate_id"):
        abort(403)

    answers = sorted(attempt.answers, key=lambda a: a.question_id)
    return render_template("review.html", attempt=attempt, answers=answers)


@result_bp.get("/history")
def history():
    candidate_id = session.get("candidate_id")
    if not candidate_id:
        return render_template("history.html", attempts=[])
    attempts = (
        ExamAttempt.query.filter_by(candidate_id=candidate_id, status="submitted")
        .order_by(ExamAttempt.submitted_at.desc())
        .all()
    )
    return render_template("history.html", attempts=attempts)

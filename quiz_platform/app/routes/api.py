from datetime import datetime

from flask import Blueprint, jsonify, request, session

from .. import db
from ..models import Answer, ExamAttempt

api_bp = Blueprint("api", __name__)


@api_bp.post("/answer")
def save_answer():
    data = request.get_json(force=True)
    attempt = _attempt_or_404()
    answer = Answer.query.filter_by(attempt_id=attempt.id, question_id=int(data.get("question_id"))).first_or_404()

    answer.selected_answer_json = data.get("answer")
    answer.is_marked_review = bool(data.get("marked_review", False))
    answer.is_visited = True
    answer.time_spent_seconds = max(0, int(data.get("time_spent", 0)))
    db.session.commit()
    return jsonify({"ok": True})


@api_bp.post("/visit")
def mark_visit():
    data = request.get_json(force=True)
    attempt = _attempt_or_404()
    answer = Answer.query.filter_by(attempt_id=attempt.id, question_id=int(data.get("question_id"))).first_or_404()
    answer.is_visited = True
    db.session.commit()
    return jsonify({"ok": True})


@api_bp.get("/attempt-state")
def attempt_state():
    attempt = _attempt_or_404()
    now = datetime.utcnow()
    remaining = max(0, int((attempt.started_at.timestamp() + attempt.exam.time_limit_seconds) - now.timestamp()))
    payload = {
        "remaining_seconds": remaining,
        "submitted": attempt.status == "submitted",
    }
    return jsonify(payload)


def _attempt_or_404():
    attempt_id = session.get("attempt_id")
    return ExamAttempt.query.filter_by(id=attempt_id).first_or_404()

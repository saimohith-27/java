from datetime import datetime, timedelta

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from .. import db
from ..models import Answer, Candidate, ExamAttempt
from ..services.evaluation_service import evaluate_attempt
from ..services.gemini_service import GeminiGenerationError, generate_exam_questions
from ..services.question_service import create_exam_with_questions

exam_bp = Blueprint("exam", __name__)

SUBJECTS = [
    "Python Programming",
    "C Programming",
    "Java",
    "Data Structures",
    "General Knowledge",
    "Computer Science",
    "Custom Subject",
]


@exam_bp.route("/configure", methods=["GET", "POST"])
def configure_exam():
    if not session.get("candidate_id"):
        return redirect(url_for("main.candidate"))

    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        custom_subject = request.form.get("custom_subject", "").strip()
        if subject == "Custom Subject" and custom_subject:
            subject = custom_subject
        difficulty = request.form.get("difficulty", "Medium").lower()
        count = int(request.form.get("question_count", 10))
        time_limit_minutes = int(request.form.get("time_limit", 10))
        qtypes = request.form.getlist("question_types") or ["single_choice"]
        categories = [c.strip() for c in request.form.get("categories", "").split(",") if c.strip()]

        if count not in {5, 10, 15, 20, 30}:
            flash("Invalid question count.", "danger")
            return render_template("configure_exam.html", subjects=SUBJECTS)

        try:
            payload = generate_exam_questions(subject, difficulty, count, qtypes, categories)
            exam = create_exam_with_questions(payload, count, time_limit_minutes * 60)
        except GeminiGenerationError as exc:
            flash(f"Question generation failed: {exc}", "danger")
            return render_template("configure_exam.html", subjects=SUBJECTS)

        attempt = ExamAttempt(candidate_id=session["candidate_id"], exam_id=exam.id)
        db.session.add(attempt)
        db.session.flush()

        for q in exam.questions:
            db.session.add(Answer(attempt_id=attempt.id, question_id=q.id, is_visited=False))

        db.session.commit()
        session["attempt_id"] = attempt.id
        session["question_idx"] = 0

        return redirect(url_for("exam.exam_page"))

    return render_template("configure_exam.html", subjects=SUBJECTS)


@exam_bp.get("/exam")
def exam_page():
    attempt = _get_active_attempt()
    if not attempt:
        return redirect(url_for("exam.configure_exam"))

    if attempt.status == "submitted":
        return redirect(url_for("result.view_result", attempt_id=attempt.id))

    candidate = Candidate.query.get(attempt.candidate_id)
    answers = sorted(attempt.answers, key=lambda a: a.question_id)
    now = datetime.utcnow()
    end_time = attempt.started_at + timedelta(seconds=attempt.exam.time_limit_seconds)
    remaining_seconds = max(0, int((end_time - now).total_seconds()))

    return render_template(
        "exam.html",
        candidate=candidate,
        attempt=attempt,
        answers=answers,
        remaining_seconds=remaining_seconds,
    )


@exam_bp.post("/submit")
def submit_exam():
    attempt = _get_active_attempt()
    if not attempt:
        return redirect(url_for("exam.configure_exam"))

    if attempt.status == "submitted":
        return redirect(url_for("result.view_result", attempt_id=attempt.id))

    summary = evaluate_attempt(attempt)
    attempt.score = summary["score"]
    attempt.max_score = summary["max_score"]
    attempt.percentage = summary["percentage"]
    attempt.status = "submitted"
    attempt.submitted_at = datetime.utcnow()
    db.session.commit()
    session.pop("attempt_id", None)
    return redirect(url_for("result.view_result", attempt_id=attempt.id))


@exam_bp.post("/autosubmit")
def auto_submit_exam():
    attempt = _get_active_attempt()
    if not attempt:
        return jsonify({"ok": False}), 400

    if attempt.status != "submitted":
        summary = evaluate_attempt(attempt)
        attempt.score = summary["score"]
        attempt.max_score = summary["max_score"]
        attempt.percentage = summary["percentage"]
        attempt.status = "submitted"
        attempt.submitted_at = datetime.utcnow()
        db.session.commit()
    return jsonify({"ok": True, "redirect": url_for("result.view_result", attempt_id=attempt.id)})


def _get_active_attempt():
    attempt_id = session.get("attempt_id")
    if not attempt_id:
        return None
    return ExamAttempt.query.get(attempt_id)

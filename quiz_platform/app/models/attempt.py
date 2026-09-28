from datetime import datetime

from .. import db


class ExamAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, default=0.0, nullable=False)
    max_score = db.Column(db.Float, default=0.0, nullable=False)
    percentage = db.Column(db.Float, default=0.0, nullable=False)
    status = db.Column(db.String(20), default="in_progress", nullable=False)
    meta_json = db.Column(db.JSON, default=dict, nullable=False)

    candidate = db.relationship("Candidate", back_populates="attempts")
    exam = db.relationship("Exam", back_populates="attempts")
    answers = db.relationship("Answer", back_populates="attempt", cascade="all, delete-orphan")


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("exam_attempt.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    selected_answer_json = db.Column(db.JSON, nullable=True)
    is_marked_review = db.Column(db.Boolean, default=False, nullable=False)
    is_visited = db.Column(db.Boolean, default=False, nullable=False)
    time_spent_seconds = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(32), nullable=True)
    marks_awarded = db.Column(db.Float, nullable=True)

    attempt = db.relationship("ExamAttempt", back_populates="answers")
    question = db.relationship("Question", back_populates="answers")

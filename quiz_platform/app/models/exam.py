from datetime import datetime

from .. import db


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(32), nullable=False)
    question_count = db.Column(db.Integer, nullable=False)
    time_limit_seconds = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    questions = db.relationship("Question", back_populates="exam", cascade="all, delete-orphan")
    attempts = db.relationship("ExamAttempt", back_populates="exam")

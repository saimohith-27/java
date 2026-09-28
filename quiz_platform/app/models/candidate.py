from datetime import datetime

from .. import db


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    candidate_code = db.Column(db.String(64), nullable=False, unique=True)
    branch = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(32), nullable=False)
    section = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    attempts = db.relationship("ExamAttempt", back_populates="candidate")

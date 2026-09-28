from .. import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"), nullable=False)
    external_id = db.Column(db.String(64), nullable=False)
    qtype = db.Column(db.String(32), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.JSON, nullable=True)
    correct_answer_json = db.Column(db.JSON, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.String(32), nullable=False)
    marks = db.Column(db.Float, nullable=False, default=1.0)
    negative_marks = db.Column(db.Float, nullable=False, default=0.0)

    exam = db.relationship("Exam", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question")

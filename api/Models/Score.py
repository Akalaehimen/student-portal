from ..utils import db
from datetime import datetime

class ScoreModel(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    grade = db.Column(db.String(), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    student = db.relationship("StudentModel", backref="scores")

    def __repr__(self):
        return f"<Score {self.score}>"
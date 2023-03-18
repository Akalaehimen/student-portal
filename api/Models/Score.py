from ..utils import db
from datetime import datetime

class ScoreModel(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    grade = db.Column(db.String(150), nullable=False)
    average_gpa = db.Column(db.Float, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("Courses.id"), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    student = db.relationship("StudentModel", backref="scores")


    def __init__(self, name, grade, average_gpa, course_id=None, student_id=None):
        self.name = name
        self.grade = grade
        self.average_gpa = average_gpa
        self.course_id = course_id
        self.student_id = student_id


    def __repr__(self):
        return f"<Score {self.score}>"
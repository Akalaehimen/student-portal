from ..utils import db
from datetime import datetime
# from ..auth.retrive import Base



class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id'))
    grade = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Score {self.score}>"












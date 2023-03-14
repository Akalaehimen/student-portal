from ..utils import db
from datetime import datetime


class CourseModel(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=False, nullable=False)
    course_name = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    Lecturer_name = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

   

    def __repr__(self):
        return f"<Course {self.course_code}>"
        
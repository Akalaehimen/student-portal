from ..utils import db
from datetime import datetime


class CourseModel(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(150), unique=False, nullable=False)
    firstname = db.Column(db.String(150), unique=False, nullable=False)
    course_code = db.Column(db.Integer, unique=False, nullable=False)
    course_name = db.Column(db.String, unique=False, nullable=False)
    # credit_hour = db.Column(db.Integer, unique=False, nullable=False)
    Lecturer_name = db.Column(db.String, unique=False, nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime)
    

   

    def __repr__(self):
        return f"<Course {self.course_code}>"
        
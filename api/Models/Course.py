from utils import db
from datetime import datetime

class CourseModel(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True)
    Surname = db.Column(db.String(150), unique=False, nullable=False)
    Firstname = db.Column(db.String(150), unique=False, nullable=False)
    course_code = db.Column(db.Integer, unique=True, nullable=False)
    course_name = db.Column(db.String, unique=True, nullable=False)
    credit_hour = db.Column(db.Integer, unique=False, nullable=False)
    Lecturer_name = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(db.Datetime(), nullable=False, default=datetime)
    

def __repr__(self):
    return f"<User {self.Surname}>"
        
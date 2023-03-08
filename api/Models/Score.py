from utils import db

class UserModel(db.Model):
    __tablename__ = "Score"
    id = db.Column(db.Integer, primary_key=True)
    Name_of_course = db.Column(db.String(150), unique=False, nullable=False)
    No_of_course_reg = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.String(80),  nullable=False)

def __repr__(self):
        return f"<User {self.Grade}>"
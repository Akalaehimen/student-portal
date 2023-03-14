from ..utils import db
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> 20516bdc5ec9b4448244fdb4d9c39ba79f78a175

class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(150), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    

    def __repr__(self):
        return f"<Student {self.surname}, {self.firstname}>"
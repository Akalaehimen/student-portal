from ..utils import db
from datetime import datetime

class AdminModel(db.Model):
    __tablename__ = "Admins"
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(150), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Student {self.surname}, {self.firstname}>"
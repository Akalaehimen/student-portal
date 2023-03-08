from utils import db

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    Surname = db.Column(db.String(150), unique=False, nullable=False)
    Firstname = db.Column(db.String(150), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

def __repr__(self):
        return f"<User {self.Firstname}>"
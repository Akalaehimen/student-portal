import random
from datetime import timedelta

from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from Blocklist import BLOCKLIST
<<<<<<< HEAD
from api.schema import UserSchema, UsersSchema

from ..Models.User import StudentModel
from ..utils import db
from flask import request
=======
from schema import UserSchema

from ..Models.User import UserModel
from ..utils import db
>>>>>>> 20516bdc5ec9b4448244fdb4d9c39ba79f78a175

blp = Blueprint("Users", "users", description="Operations on Users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if StudentModel.query.filter_by(email=user_data["email"]).first():
            abort(409, message="This Email already exists")
        
        user = StudentModel(
            surname=user_data["surname"],
            firstname=user_data["firstname"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        user_matric_no = self.generate_unique_id()
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully", "matric_no": user_matric_no}, 201
        
    def generate_unique_id(self, length=4):
        letters = 'ST'
        unique_id = ''.join(random.choice(letters) for i in range(length))
        user_number = f"{unique_id}{random.randint(1000, 9999)}"
        return user_number


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = StudentModel.query.filter(
            StudentModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"message": "User successfully logged in", "access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid Credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta(days=5)
        )

        return {"access_token": new_token}

@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
         BLOCKLIST.add(jti)

        except IntegrityError:
         abort(400, message="you need to be logged in to have access")

        return ({"message": "Successfully logged out"})

@blp.route("/user/<int:user_id>")
class User(MethodView):
    # Get a student by id
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = StudentModel.query.get_or_404(user_id)
        return user
    
    # Delete a student by id
    def delete(self, user_id):
        user = StudentModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "Student Deleted"}, 200
    


@blp.route("/users")
class UserList(MethodView):
    # retrieving all student
    @blp.response(200, UserSchema(many=True))
    def get(self):
        all_student = StudentModel.query.all()
        return all_student
    
# update a student
@blp.route("/students/<int:student_id>", methods=["PUT"])
class UpdateStudent(MethodView):
    @blp.arguments(UsersSchema)
    @blp.response(200, UsersSchema)
    def put(self, student_data, student_id):
        student = StudentModel.query.get(student_id)
        if student:
            student.firstname = student_data.get("firstname")
            student.surname = student_data.get("surname")
            student.email = student_data.get("email")
            db.session.commit()
            return student, 200
        else:
            abort(404, message="Student not found")
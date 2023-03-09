import random
from datetime import timedelta

from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from Blocklist import BLOCKLIST
from schema import UserSchema

from ..Models.User import UserModel
from ..utils import db

blp = Blueprint("Users", "users", description="Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="This Email already exist")
        
        user = UserModel(
            Surname = user_data["Surname"],
            Firstname = user_data["Firstname"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        
        db.session.add(user)
        db.session.commit()
    
    def generate_unique_id(length=4):
     letters = 'ST'
     unique_id = ''.join(random.choice(letters) for i in range(length))
     user_number = unique_id()
     return {"User created succesfully your matric no is:", user_number}, 201



@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}
        
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
        user = UserModel.query.get_or_404(user_id)
        return user
    
    # Delete a student by id
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "Student Deleted"}, 200

@blp.route("/users")
class UserList(MethodView):
    # retrieving all student
    @blp.response(200, UserSchema(many=True))
    def get(self):
        all_student = UserModel.query.all()
        return all_student
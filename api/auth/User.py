import random
from datetime import timedelta

from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from Blocklist import BLOCKLIST
from api.schema import UserSchema, UsersSchema
from ..Models.User import StudentModel
from ..Models.admin import AdminModel
from ..utils import db
from flask import request, jsonify
from ..schema import UserSchema
from ..utils import db




blp = Blueprint("Users", "users", description="Operations on Users")
user_bp = Blueprint('user_bp', __name__, url_prefix='/users')
update_bp = Blueprint('update_bp', __name__, url_prefix='/students')
delete_bp = Blueprint('delete_bp', __name__, url_prefix='/delete')
retrive_bp = Blueprint('retrive_bp', __name__, url_prefix='/retrive')


# register a student  
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

# login a student 
@blp.route("/login", methods=['POST'])
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user_data = request.get_json()
        user = StudentModel.query.filter(
            StudentModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({"message": "User successfully logged in", "access_token": access_token, "refresh_token": refresh_token})
        
        return jsonify({"message": "Invalid credentials"}), 401


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta(days=5)
        )

        return {"access_token": new_token}

# logout a student  
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

    
    # Delete a student by id
class DeleteView(MethodView):
    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        user = StudentModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "Student Deleted"}, 200
    
user_view = DeleteView.as_view('user_view')
delete_bp.add_url_rule('/<int:user_id>', view_func=user_view)
    

# retrieving all student  
class RetriveView(MethodView):
      @jwt_required()
      @blp.response(200, UsersSchema(many=True))
      def get(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        all_student = StudentModel.query.all()
        return all_student
    
user_view = RetriveView.as_view('user_view')
retrive_bp.add_url_rule('', view_func=user_view)

# update a student
class Updateview(MethodView):
    @jwt_required()
    @blp.arguments(UsersSchema)
    @blp.response(200, UsersSchema)
    def put(self, student_data, student_id):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        student = StudentModel.query.get(student_id)
        if student:
            student.firstname = student_data.get("firstname")
            student.surname = student_data.get("surname")
            student.email = student_data.get("email")
            db.session.commit()
            return student, 200
        else:
            abort(404, message="Student not found")

user_view = Updateview.as_view('update_view')
update_bp.add_url_rule('/<int:student_id>', view_func=user_view)


# get a student by is id 
class UserView(MethodView):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        user = StudentModel.query.get_or_404(user_id)
        user_data = UserSchema().dump(user)
        return user_data

user_view = UserView.as_view('user_view')
user_bp.add_url_rule('/<int:user_id>', view_func=user_view)
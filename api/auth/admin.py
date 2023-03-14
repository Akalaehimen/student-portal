from functools import wraps

from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..utils import db
# from schema import AdminSchema
from passlib.hash import pbkdf2_sha256
from ..Models.admin import AdminModel
from ..schema import AdminSchema, AdminlogSchema
from flask_jwt_extended import  jwt_required

blp = Blueprint("Admins", "admins", description="Operations on Admins")

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "3c62c7ca4baefb92"  
jwt = JWTManager(app)

# an administrator
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


@blp.route('/register-admin')
class AdminRegister(MethodView):
    @blp.arguments(AdminSchema)
    def post(self, user):
    # load user data from the request body
        admin_data = AdminSchema().load(request.json)
    
    # check if an admin user with this email already exists
        if AdminModel.query.filter_by(email=admin_data["email"]).first():
           abort(409, message="This Email already exists")
    
    # create a new AdminModel instance with the user data
        new_admin = AdminModel(
        surname=admin_data["surname"],
        firstname=admin_data["firstname"],
        email=admin_data["email"],
        password=pbkdf2_sha256.hash(admin_data["password"]),
        # is_administrator=True  
    )
    
    # add the new admin user to the database and commit the changes
        db.session.add(new_admin)
        db.session.commit()
    
    # return a success message and a 201 Created status code
        return {"message": "Admin user created successfully"}, 201
    


@blp.route('/login-admin')
class Login(MethodView):
    @blp.arguments(AdminlogSchema)
    @jwt_required()
    def post(self, user):
    # load user data from the request body
        admin_data = request.get_json()
        email = admin_data.get('email')
        password = admin_data.get('password')

    # try to find an admin user with the given email
        admin = AdminModel.query.filter_by(email=email).first()

    # if no admin user is found, return an error response
        if not admin:
          return {"message": "Invalid email or password"}, 401

    # verify the password against the stored hash
        if not pbkdf2_sha256.verify(password, admin.password):
           return {"message": "Invalid email or password"}, 401

    # if the password is correct, generate a JWT token with the user's email and is_administrator status
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=user.email)

    # return the access token as a JSON response
        return {"message": "User successfully logged in", "access_token": access_token, "refresh_token": refresh_token}, 200


@blp.route('/refresh')
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        # get the user identity from the refresh token
        email = get_jwt_identity()

        # generate a new access token for the user
        access_token = create_access_token(identity=email)

        # return the new access token as a JSON response
        return {"access_token": access_token}, 200

@blp.route("/admins")
class Adminlist(MethodView):
    # retrieving all admin
    @blp.response(200, AdminSchema(many=True))
    def get(self):
        all_admin = AdminModel.query.all()
        return all_admin

        
        
@app.route("/protected", methods=["GET"])
@admin_required()
def protected():
    return jsonify(foo="bar")

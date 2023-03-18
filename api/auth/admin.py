from functools import wraps

from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from flask_jwt_extended import JWTManager
from flask import request
from functools import wraps
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..utils import db
from passlib.hash import pbkdf2_sha256
from ..Models.admin import AdminModel
from ..schema import AdminSchema, AdminlogSchema, AdminsSchema
from Blocklist import BLOCKLIST
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import  jwt_required


blp = Blueprint("Admins", "admins", description="Operations on Admins")
refresh_bp = Blueprint('refresh_bp', __name__, url_prefix='/refresh')
Admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admins')

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "3c62c7ca4baefb92"  
jwt = JWTManager(app)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # Only allow access to users with the role "admin"
        if current_user_id.role != "admin":
            return {"message": "You are not authorized to access this resource."}, 403
        return fn(*args, **kwargs)
    return wrapper


@blp.route('/admin_only')
@admin_required
def admin_only():
    return {"message": "This route is only accessible by administrators."}
   



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
    

# login an admin  
@blp.route('/login-admin')
class Login(MethodView):
    @blp.arguments(AdminlogSchema)
    def post(self, user_data):
        user_data = request.get_json()
        user = AdminModel.query.filter(
            AdminModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({"message": "User successfully logged in", "access_token": access_token, "refresh_token": refresh_token})
        
        return jsonify({"message": "Invalid credentials"}), 401
    


# @blp.route('/refresh')
 
class Refreshview(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        # get the user identity from the refresh token
        email = get_jwt_identity()

        # generate a new access token for the user
        access_token = create_access_token(identity=email)

        # return the new access token as a JSON response
        return {"access_token": access_token}, 200
    
user_view = Refreshview.as_view('refresh_view')
refresh_bp.add_url_rule('', view_func=user_view)



# retrieving all admin 

class Adminview(MethodView):
    @jwt_required()
    @blp.response(200, AdminsSchema(many=True))
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        all_admin = AdminModel.query.all()
        return all_admin
    
user_view = Adminview.as_view('Admin_view')
Admin_bp.add_url_rule('', view_func=user_view)

        
# protected route  

@app.route("/protected", methods=["GET"])
@jwt_required()
@admin_required
def protected():
    return jsonify(foo="bar")


# logout an admin 
@blp.route("/logouts")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        jti = get_jwt()['jti']
        try:
         BLOCKLIST.add(jti)

        except IntegrityError:
         abort(400, message="you need to be logged in to have access")

        return ({"message": "Successfully logged out"})

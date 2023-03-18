import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from .utils import db
from flask_migrate import Migrate
from Blocklist import BLOCKLIST
from datetime import timedelta
from api.auth.User import blp as auth_blueprint
from api.auth.Score import blp as score_blueprint
from api.auth.Course import blp as course_blueprint
from api.auth.admin import blp as admin_blueprint
from api.auth.User import user_bp as user_blueprint
from api.auth.User import update_bp as update_blueprint
from api.auth.User import delete_bp as delete_blueprint
from api.auth.User import retrive_bp as retrive_blueprint
from api.auth.Score import score_bp as scores_blueprint
from api.auth.Score import result_bp as result_blueprint
from api.auth.Course import student_bp as student_blueprint
from api.auth.Course import register_bp as register_blueprint
from api.auth.Course import store_bp as store_blueprint
from api.auth.retrive import get_bp as get_blueprint
from api.auth.admin import refresh_bp as refresh_blueprint
from api.auth.admin import Admin_bp as admins_blueprint
from api.config.config import config_dict


def create_app(db_url=None, config=config_dict['dev']):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Student Portal API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)



    api = Api(app)

    migrate = Migrate(app, db)

    
    app.config["JWT_SECRET_KEY"] = "veryrandomstuff"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "description": "This token has expired",
                "error": "token_expired"
            }), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "description": "Signature verification failed",
                "error": "invalid_token"
            }), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "desciption": "Request does not contain an access token",
                "error": "authorization_required"
            }), 401
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(auth_blueprint)
    api.register_blueprint(score_blueprint)
    api.register_blueprint(course_blueprint)
    api.register_blueprint(admin_blueprint)
    api.register_blueprint(user_blueprint)
    api.register_blueprint(update_blueprint)
    api.register_blueprint(delete_blueprint)
    api.register_blueprint(retrive_blueprint)
    api.register_blueprint(scores_blueprint)
    api.register_blueprint(result_blueprint)
    api.register_blueprint(student_blueprint)
    api.register_blueprint(register_blueprint)
    api.register_blueprint(store_blueprint)
    api.register_blueprint(get_blueprint)
    api.register_blueprint(refresh_blueprint)
    api.register_blueprint(admins_blueprint)




    # api.register_blueprint(course_blueprint)


    return app
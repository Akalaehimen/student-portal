from flask import jsonify

from flask_smorest import Blueprint
from ..Models.Score import ScoreModel
from ..Models.User import  StudentModel
from ..Models.Course import CourseModel
from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask.views import MethodView
from ..Models.admin import AdminModel


get_bp = Blueprint('get_bp', __name__, url_prefix='/grades')


# retriveing a student result per course  
class GetView(MethodView):
    @jwt_required()
    def get(self, course_name, student_surname):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403

        # Query the database for the student's grade
        grade = ScoreModel.query.join(StudentModel).join(CourseModel).filter(CourseModel.course_name==course_name, StudentModel.surname==student_surname).first()
        if grade:
            return jsonify({"course_name": course_name, "student_surname": student_surname, "grade": grade.grade})
        else:
            return jsonify({"message": f"No grade found for student {student_surname} in course {course_name}"})
        
user_view = GetView.as_view('get_view')
get_bp.add_url_rule('/courses/<string:course_name>/students/<string:student_surname>', view_func=user_view, methods=['GET'])

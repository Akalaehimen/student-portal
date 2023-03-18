from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..Models.Course import CourseModel
from ..utils import db
from api.schema import CourseSchema
from ..schema import CourseSchema
from ..Models.admin import AdminModel

from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask import jsonify
from datetime import datetime

blp = Blueprint("Courses", "courses", description="Operations on Courses")
student_bp = Blueprint('student_bp', __name__, url_prefix='/students')
register_bp = Blueprint('register_bp', __name__, url_prefix='/registercourses')
store_bp = Blueprint('store_bp', __name__, url_prefix='/Courses')


# student registering there course  
class Registerview(MethodView):
    @jwt_required()
    @blp.arguments(CourseSchema)
    def post(self, user_data):
        if 'id' in user_data and CourseModel.query.filter(CourseModel.id== user_data["id"]).first():
            abort(409, message="A student with this id has already been registered for this course")

        new_course = CourseModel(
            course_code = user_data["course_code"],
            course_name = user_data["course_name"],  
            Lecturer_name = user_data["Lecturer_name"],
            firstname = user_data["firstname"],
            surname = user_data["surname"],
            date_created=datetime.now()
        )

        db.session.add(new_course)
        db.session.commit()

        return {"message": "Student course Created Successfully"}, 201

user_view = Registerview.as_view('register_view')
register_bp.add_url_rule('', view_func=user_view)

    
# Getting all courses

class Storeview(MethodView):
    @jwt_required()
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        return CourseModel.query.all()

user_view = Storeview.as_view('store_view')
store_bp.add_url_rule('', view_func=user_view)


# Retrieving student offering a course by its course name

class StudentView(MethodView):
      @jwt_required()
      def get(self, course):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        students_with_course = []
        for student in CourseModel.query.filter(CourseModel.course_name.contains(course)):
               students_with_course.append({'firstname': student.firstname, 'surname': student.surname, 'course_code': student.course_code})
        return jsonify(students_with_course)

user_view = StudentView.as_view('student_view')
student_bp.add_url_rule('/<course>', view_func=user_view)



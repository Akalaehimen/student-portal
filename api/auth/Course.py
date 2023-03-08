from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Models.Course import CourseModel
from utils import db
from schema import CourseSchema
from flask_jwt_extended import  jwt_required


blp = Blueprint("Courses", "courses", description="Operations on Courses")

@blp.route("/registercourses")
class Registercourses(MethodView):
    @blp.arguments(CourseSchema)
    def post(self, user_data):
        if CourseModel.query.filter(CourseModel.id== user_data["id"]).first():
            abort(409, message="A student with this id has already been registered for this course")

        new_course = CourseModel(
            Surname = user_data["Surname"],
            Firstname = user_data["Firstname"],
            course_code = user_data["course_code"],
            course_name = user_data["course_name"],
            credit_hour = user_data["credit_hour"],  
            Lecturer_name = user_data["Lecturer_name"],
        )

        
        db.session.add(new_course)
        db.session.commit()
        return {"message": "Student course Created Successfully"}, 201
    
# Getting all courses
@blp.route("/Courses")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return CourseModel.query.all()


# Retrieving student offering a course by its course name
@blp.route("/Courses/Course_name")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, CourseSchema)
    def get(self, Course_name):
        Course = CourseModel.query.get_or_404(Course_name)
        return Course
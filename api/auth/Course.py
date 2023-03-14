from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..Models.Course import CourseModel
from ..utils import db
<<<<<<< HEAD
from api.schema import CourseSchema, CoursesSchema
=======
from schema import CourseSchema
>>>>>>> 20516bdc5ec9b4448244fdb4d9c39ba79f78a175
from flask_jwt_extended import  jwt_required
from ..auth.admin import admin_required
from flask import jsonify




blp = Blueprint("Courses", "courses", description="Operations on Courses")


@blp.route("/registercourses")
class Registercourses(MethodView):
    @blp.arguments(CourseSchema)
    def post(self, user_data):
        if 'id' in user_data and CourseModel.query.filter(CourseModel.id== user_data["id"]).first():
            abort(409, message="A student with this id has already been registered for this course")

        new_course = CourseModel(
            course_code = user_data["course_code"],
            course_name = user_data["course_name"],  
            Lecturer_name = user_data["Lecturer_name"],
            firstname = user_data["firstname"],
            surname = user_data["surname"]
        )

        
        db.session.add(new_course)
        db.session.commit()
        return {"message": "Student course Created Successfully"}, 201
    
# Getting all courses
@blp.route("/Courses")
class StoreList(MethodView):
    # @jwt_required()
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        return CourseModel.query.all()


# Retrieving student offering a course by its course name

@blp.route('/students/<course>', methods=['GET'])
def get_students_by_course(course):
    students_with_course = []
    for student in CourseModel.query.filter(CourseModel.course_name.contains(course)):
        students_with_course.append({'firstname': student.firstname, 'surname': student.surname, 'course_code': student.course_code})
    return jsonify(students_with_course)




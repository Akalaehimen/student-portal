from flask.views import MethodView
<<<<<<< HEAD
from flask_smorest import Blueprint, abort
from ..utils import db
from api.schema import ScoreSchema
=======
from flask_smorest import Blueprint
from ..utils import db
from schema import ScoreSchema
>>>>>>> 20516bdc5ec9b4448244fdb4d9c39ba79f78a175
from flask_jwt_extended import  jwt_required
from api.schema import ResultSchema
from ..Models.User import StudentModel
from ..Models.retrive import Grade
from flask import jsonify


blp = Blueprint("Scores", "scores", description="Operations on Score")

@blp.route("/scores")
class CalculateGPA(MethodView):
    @blp.arguments(ScoreSchema(many=True))
    def post(self, scores):
        # dictionary to map grades to their corresponding values
        grade_values = {
            'A+': 4.0,
            'A': 4.0,
            'A-': 3.7,
            'B+': 3.3,
            'B': 3.0,
            'B-': 2.7,
            'C+': 2.3,
            'C': 2.0,
            'C-': 1.7,
            'D+': 1.3,
            'D': 1.0,
            'D-': 0.7,
            'F': 0,
        }

        # initialize variable to store the total gpa and the number of courses
        total_gpa = 0
        count = 0

        # loop through each course
        for score in scores:
            name_of_course = score['name']
            grade = score['grade']

            # convert the grade to uppercase to make it non-case sensitive
            grade = grade.upper()

            # check if the grade is valid
            if grade not in grade_values:
                abort(400, message="Invalid grade, please enter a valid grade.")

            # print the course and grade
            print(f'({name_of_course.capitalize()}:{grade})')

            # add the gpa value of the grade to the total gpa
            total_gpa += grade_values[grade]
            count += 1

        # calculate the average gpa
        average_gpa = total_gpa / count

        # return the average gpa
        return {"Your average_gpa is": average_gpa}





# retrieving a student by is matric no
@blp.route("/results/<string:unique_id>")
class StudentResult(MethodView):
    @jwt_required()
    @blp.response(200, ResultSchema)
    def get(self, unique_id):
        student = StudentModel.query.filter_by(matric_no=unique_id).first()
        if student is None:
            abort(404, message="Student not found")
        
        # assuming the grades are stored in a separate model
        grades = Grade.query.filter_by(student_id=student.id).all()
        
        if grades is None or len(grades) == 0:
            abort(404, message="No grades found for this student")
        
        # calculate the average grade for the student
        total_grade = 0
        for grade in grades:
            total_grade += grade.grade
        
        average_grade = total_grade / len(grades)
        
        # create a dictionary representing the student's result
        result = {
            "unique_id": unique_id,
            "name": f"{student.surname} {student.firstname}",
            "average_grade": average_grade
        }
        
        return result
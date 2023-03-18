from flask.views import MethodView

from flask_smorest import Blueprint, abort
from ..utils import db
from api.schema import ScoreSchema
from flask_smorest import Blueprint
from ..utils import db
from datetime import datetime
from ..schema import ScoreSchema
from flask_jwt_extended import  jwt_required, get_jwt_identity
from api.schema import ResultSchema
from ..Models.User import StudentModel

from ..Models.Score import ScoreModel
from flask import jsonify, request
from flask_restful import Resource
from ..Models.admin import AdminModel

blp = Blueprint("Scores", "scores", description="Operations on Score")
score_bp = Blueprint('score_bp', __name__, url_prefix='/score')
result_bp = Blueprint('result_bp', __name__, url_prefix='/result')

# calculate the result of a student  
class CalculateView(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        # get the list of scores from the request body
        scores = request.json

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
            if 'name' not in score:
               return {'message': 'Invalid score, please provide a name for the course.'}, 400
            name_of_course = score['name']
            grade = score['grade']

            # convert the grade to uppercase to make it non-case sensitive
            grade = grade.upper()

            # check if the grade is valid
            if grade not in grade_values:
                return {'message': 'Invalid grade, please enter a valid grade.'}, 400

            # add the gpa value of the grade to the total gpa
            total_gpa += grade_values[grade]
            count += 1

        # calculate the average gpa
        average_gpa = total_gpa / count

        # create a new GPA object
        new_gpa = ScoreModel(name=name_of_course, grade=grade, average_gpa=average_gpa)
        # add the new GPA to the database
        db.session.add(new_gpa)
        db.session.commit()

        # return the average gpa and a success message
        return {'average_gpa': average_gpa, 'message': 'GPA successfully saved to database.'}, 200

calculate_view = CalculateView.as_view('calculate_view')
score_bp.add_url_rule('', view_func=calculate_view)





# retrieving a student by is surname


class Resultview(Resource):
    @jwt_required()
    def get(self, surname):
        current_user_id = get_jwt_identity()
        current_user = AdminModel.query.get(current_user_id)
        if current_user is None:
            return {"message": "Invalid user ID in JWT token"}, 401
        elif current_user.role != "admin":
            return {"message": "You are not authorized to perform this action"}, 403
        # Retrieve the student(s) with the given surname
        students = StudentModel.query.filter_by(surname=surname).all()
        if not students:
            abort(404, message="No student found with this surname")

        # Retrieve the grades for all matching students
        grades = []
        for student in students:
            grades.extend(ScoreModel.query.filter_by(student_id=student.id).all())
        if not grades:
            abort(404, message="No grades found for students with this surname")

        # Calculate the average grade for all matching students
        total_grade = sum(grade.grade for grade in grades)
        average_grade = total_grade / len(grades)

        # Create a list of dictionaries representing the results for each matching student
        results = []
        for student in students:
            result = {
                "name": f"{student.surname} {student.firstname}",
                "average_grade": average_grade
            }
            results.append(result)

        # Serialize the results list to JSON using the ResultSchema
        return ResultSchema(many=True).dump(results)


calculate_view = Resultview.as_view('Result_view')
result_bp.add_url_rule('/<string:surname>', view_func=calculate_view)
from flask.views import MethodView
from flask_smorest import Blueprint
from utils import db
from schema import ScoreSchema
from flask_jwt_extended import  jwt_required

blp = Blueprint("Scores", "scores", description="Operations on Score")

@blp.route("/scores")
class Registerscores(MethodView):
    @blp.arguments(ScoreSchema)
    def post(self):
        # dictionary to map grades to it's corresponding values
        grade_values = {
            'A+':4.0,
            'A':4.0,
            'A-':3.7,
            'B+':3.3,
            'B':3.0,
            'B-':2.7,
            'C+':2.3,
            'C':2.0,
            'C-':1.7,
            'D+':1.3,
            'D':1.0,
            'D-':0.7,
            'F':0,
        }

        # prompt the user to enter the number of courses
        No_of_course_reg = int(input('Enter the number of courses registered: '))

        # initialize variable to store the total gpa and the number of subject
        total_gpa = 0
        count = 0

        # loop through each course
        while count < No_of_course_reg:

        #  prompt the user to enter the name of the course and the grade 
         Name_of_course = input('Enter the name of the course registered: ')
         Grade = input('Enter the Grade: ') 

        #  convert the grade to uppercase to make it non-case sensitive
        Grade = Grade.upper

        # check if the grade is valid
        if Grade not in grade_values:
           return {"message": "invalid grade please enter a valid grade."}
        else:
           pass

        # print the course and grade
        print(f'({Name_of_course.capitalize()}:{Grade})')
    
        # prompt the user  to confirm the entry
        Confirmation = input('is this entry correct?(yes/no)')
        if Confirmation.lower() != 'yes':
           pass

        # add the gpa value of the grade to the total gpa
        total_gpa += grade_values[Grade]
        count += 1

        # calculate the average Gpa
        average_gpa = total_gpa / count

        # print the average_gpa
        return{f'Your Average Gpa is:{average_gpa:.2f}'}
    
        



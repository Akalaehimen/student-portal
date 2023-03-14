from flask import jsonify
from sqlalchemy import create_engine
from flask_smorest import Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..Models.retrive import Grade


# Create a database engine and sessionmaker
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)

# Define a declarative base
Base = declarative_base()


# Define a blueprint for grades
grades_bp = Blueprint("grades", __name__, description="retrieving of score for a student")

@grades_bp.route("/courses/<int:course_id>/students/<int:student_id>/grades", methods=["GET"])
def get_student_grades(course_id, student_id):
    # Query the database for the grade
    session = Session()
    grade = session.query(Grade).filter_by(course_id=course_id, student_id=student_id).first()
    
    # If a grade is found, return a JSON response with the grade
    if grade:
        return jsonify({"student_id": student_id, "grade": grade.grade})
    # If no grade is found, return a JSON response with a message indicating that no grade was found
    else:
        return jsonify({"message": f"No grades found for student {student_id} in course {course_id}"})
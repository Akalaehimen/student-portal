Student Management System
This is a web-based application that allows students to register for courses and for lecturers to manage students' academic records. The application is built with Python Flask framework and uses a Flask-SQLAlchemy database for data storage. It also uses JSON Web Tokens (JWT) for authentication and authorization, ensuring that only authorized users have access to sensitive data.

Features
The application has the following features:

User authentication and authorization using JWT
User roles: administrators and students
Admin functionality: updating, deleting, retrieving students and courses, retrieving grades, calculating GPA
Student functionality: registering for courses
only admin can have a view of list of all courses

Installation
To install and run the application, follow these steps:

Clone the repository to your local machine: git clone https://github.com/Akalaehimen/student-portal.git
Install the required dependencies: pip install -r requirements.txt
Create a .env file in the root directory of the project and set the following environment variables:
makefile
Copy code
FLASK_APP=runserver
FLASK_DEBUG=1
DATABASE_URL=your-database-uri
JWT_SECRET=your-jwt-secret
Initialize the database: flask db init
Migrate the database: flask db migrate
Upgrade the database: flask db upgrade
Start the application: flask run
Open your browser and navigate to http://localhost:5000
Usage
Admin functionality
To access the admin functionality, you need to log in as an admin. To do this, go to the login page (/login) and enter your admin credentials. Once logged in, you can access the following pages:

Dashboard (/dashboard): displays a summary of the number of students, courses, and grades in the system
Students (/students): allows you to view, update, and delete student records
Courses (/courses): allows you to view course records
Grades (/grades): allows you to view and calculate grades for each student
Student functionality
To access the student functionality, you need to log in as a student. To do this, go to the login page (/login) and enter your student credentials. Once logged in, you can access the following pages:

Dashboard (/dashboard): displays a summary of the courses you are registered for
Courses (/courses): allows you to register for courses
Security
The application uses JWT for authentication and authorization. JWTs are issued when a user logs in and must be included in every subsequent request to the server. The server verifies the JWT and grants access to the requested resource if the user is authorized. All sensitive data is only accessible to admins, while students only have access to their own records.

Future Improvements
Some potential improvements for the application include:

Adding pagination to the list of students and courses to improve performance
Adding a feature to allow admins to assign grades to students for each course
Adding a feature to allow students to view their grades and GPA
Conclusion
This student management system is a useful tool for managing student records and courses. Its authentication and authorization features ensure that only authorized users have access to sensitive data.


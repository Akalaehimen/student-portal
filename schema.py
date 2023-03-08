from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    Surname = fields.Str(required=True)
    Firstname = fields.Str(required=True)
    password = fields.Str(required=True)


class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    Surname = fields.Str(required=True)
    Firstname = fields.Str(required=True)
    password = fields.Str(required=True)
    Course_code = fields.Int(required=True)
    Credit_hour = fields.Int(required=True)
    Lecturer_name = fields.Str(required=True)


class ScoreSchema(Schema):
    id = fields.Int(dump_only=True)
    Name_of_course = fields.Str(required=True)
    No_of_course_reg = fields.Int(required=True)
    Grade = fields.Str(required=True)
    
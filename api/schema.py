from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)
    password = fields.Str(required=True)
    


class CourseSchema(Schema):
    id = fields.Int(dump_only=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)
    course_name = fields.Str(required=True)
    course_code = fields.Int(required=True)
    Lecturer_name = fields.Str(required=True)


class ScoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    grade = fields.Str(required=True)
    

class UpdatestudentSchema(Schema):
    id = fields.Int(dump_only=True)
    Surname = fields.Str(required=True)
    Firstname = fields.Str(required=True)
    email = fields.Str(required=True)


class AdminSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)
    password = fields.Str(required=True)


class ResultSchema(Schema):
    id = fields.Int(dump_only=True)
    course_code = fields.Str(required=True)
    course_title = fields.Str(required=True)
    grade = fields.Int(required=True)
    

class AdminlogSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)


class AdminsSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)

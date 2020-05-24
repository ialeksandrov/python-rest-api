from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

STUDENTS = {
  '1': {'name': 'Mark', 'age': 23, 'spec': 'math'},
  '2': {'name': 'Jane', 'age': 20, 'spec': 'biology'},
  '3': {'name': 'Peter', 'age': 21, 'spec': 'history'},
  '4': {'name': 'Kate', 'age': 22, 'spec': 'science'},
}


class StudentsList(Resource):
    @staticmethod
    def get():
        return STUDENTS

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")

        args = parser.parse_args()
        student_id = int(max(STUDENTS.keys())) + 1
        student_id = '%i' % student_id
        STUDENTS[student_id] = {
            "name": args["name"],
            "age": args["age"],
            "spec": args["spec"],
        }

        return STUDENTS[student_id], 201


class Student(Resource):
    @staticmethod
    def get(student_id):
        if student_id not in STUDENTS:
            return "Not Found", 404

        return STUDENTS[student_id]

    @staticmethod
    def put(student_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")

        args = parser.parse_args()
        if student_id not in STUDENTS:
            return "Record not found", 404

        student = STUDENTS[student_id]
        student["name"] = args["name"] if args["name"] is not None else student["name"]
        student["age"] = args["age"] if args["age"] is not None else student["age"]
        student["spec"] = args["spec"] if args["spec"] is not None else student["spec"]

        return student, 200

    @staticmethod
    def delete(student_id):
        if student_id not in STUDENTS:
            return "Not found", 404

        del STUDENTS[student_id]
        return '', 204


api.add_resource(StudentsList, '/students/')
api.add_resource(Student, '/students/<student_id>')

if __name__ == "__main__":
    app.run(debug=True)

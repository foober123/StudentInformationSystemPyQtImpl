from model.student import StudentModel
from PyQt5.QtSql import QSqlQuery
import re
from errors.validation_error import ValidationError
from core.signals import signals

class StudentService:

    @staticmethod
    def create_student(data):
        StudentService._validate_student(data)

        result = StudentModel.add(data)
        signals.data_changed.emit("student")
        return result

    @staticmethod
    def get_students(limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return StudentModel.get_all(limit, offset, field, text, sort, sort_order)

    @staticmethod
    def count_students(field=None, text=None):
        return StudentModel.count(field, text)


    @staticmethod
    def get_student_by_id(student_id):
        query = QSqlQuery()
        query.prepare("""
            SELECT * FROM student WHERE id = ?
        """)
        query.addBindValue(student_id)
        query.exec()

        if query.next():
            return {
                "id": query.value("id"),
                "firstname": query.value("firstname"),
                "lastname": query.value("lastname"),
                "course": query.value("course"),
                "year": query.value("year"),
                "gender": query.value("gender"),
            }
        return None

    @staticmethod
    def update_student(data):
        StudentService._validate_student(data, update=True)

        result = StudentModel.update(data)
        signals.data_changed.emit("student")
        return result

    @staticmethod
    def remove(student_id):
        if not StudentService._student_exists(student_id):
            raise ValueError("Student not found")

        result = StudentModel.delete(student_id)
        signals.data_changed.emit("student")
        return result

    @staticmethod
    def _validate_student(data, update=False):
        errors = {}
        name_pattern = r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$"


        if not update:
            if not data.get("id"):
                errors["id"] = "ID required"
            else:
                if not re.match(r"^20\d{2}-\d{4}$", data["id"]):
                    errors["id"] = "Format must be 20XX-XXXX"

            if not data.get("firstname"):
                errors["firstname"] = "Firstname required"
            elif not re.match(name_pattern, data["firstname"]):
                errors["firstname"] = "Firstname must contain letters only"

            if not data.get("lastname"):
                errors["lastname"] = "Lastname required"
            elif not re.match(name_pattern, data["lastname"]):
                errors["lastname"] = "Lastname must contain letters only"

            if StudentService._student_exists(data["id"]):
                errors["id"] = ("Student already exists")

        else:

            if "firstname" in data and not data["firstname"]:
                errors["firstname"] = "Firstname cannot be empty"
            elif not re.match(name_pattern, data["firstname"]):
                errors["firstname"] = "Firstname must contain letters only"

            if "lastname" in data and not data["lastname"]:
                errors["lastname"] = "Lastname cannot be empty"
            elif not re.match(name_pattern, data["lastname"]):
                errors["lastname"] = "Lastname must contain letters only"

        if "course" not in data or not data["course"]:
            errors["course"] = "Course is required"

        if "year" in data:
            if not isinstance(data["year"], int) or not (1 <= data["year"] <= 5):
                errors["year"] = "Year must be between 1 and 5"

        if "gender" in data and data["gender"] is not None:
            if data["gender"] not in ["Male", "Female", "Other"]:
                errors["gender"] = "Invalid gender"

        if data.get("course") and not StudentService._program_exists(data["course"]):
            raise ValueError("Invalid program")

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def _student_exists(student_id):
        query = QSqlQuery()
        query.prepare("SELECT 1 FROM student WHERE id = ?")
        query.addBindValue(student_id)
        query.exec()
        return query.next()

    @staticmethod
    def _program_exists(program_code):
        query = QSqlQuery()
        query.prepare("SELECT 1 FROM program WHERE code = ?")
        query.addBindValue(program_code)
        query.exec()
        return query.next()

from model.college import CollegeModel
from PyQt5.QtSql import QSqlQuery
from errors.validation_error import ValidationError
from core.signals import signals
import re

class CollegeService:

    @staticmethod
    def create(data):
        code = data.get("code", "").strip()
        name = data.get("name", "").strip()

        CollegeService._validate_college(data) 
        result = CollegeModel.add({
            "code": code,
            "name": name
        })
        signals.data_changed.emit("college")
        return result


    @staticmethod
    def update(data):
        CollegeService._validate_college(data, update=True)
        
        result = CollegeModel.update(data)
        signals.data_changed.emit("college")
        return result

    @staticmethod
    def get_by_code(code):
        query = QSqlQuery()
        query.prepare("SELECT code, name FROM college WHERE code = ?")
        query.addBindValue(code)
        query.exec()

        if query.next():
            return {
                "code": query.value(0),
                "name": query.value(1)
            }
        return None

    @staticmethod
    def get(limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return CollegeModel.get_all(limit, offset, field, text, sort, sort_order)

    @staticmethod
    def count(field=None, text=None):
        return CollegeModel.count(field, text)

    @staticmethod
    def remove(code):
        result = CollegeModel.delete(code)
        signals.data_changed.emit("college")
        return result

    @staticmethod
    def _validate_college(data, update=False):
        errors = {}

        code = data.get("code", "").strip()
        name = data.get("name", "").strip()

        # Code validation
        if not code:
            errors["code"] = "Code required"

        elif not re.fullmatch(r"[A-Z]+", code):
            errors["code"] = "Code must contain uppercase letters only (A-Z)"

        else:
            existing = CollegeService.get_by_code(code)

            if not update:
                if existing:
                    errors["code"] = "College code already exists"

            else:
                original_code = data.get("original_code")

                if (
                    existing
                    and code != original_code
                ):
                    errors["code"] = "College code already exists"

        # Name validation
        if not name:
            errors["name"] = "Name required"

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def get_college_codes():
        return CollegeModel.get_college_codes()

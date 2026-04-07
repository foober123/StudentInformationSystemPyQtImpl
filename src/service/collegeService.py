from model.college import CollegeModel
from PyQt5.QtSql import QSqlQuery
from errors.validationError import ValidationError
from core.signals import signals

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

        if not update:
            if not data.get("code"):
                errors["code"] = "Code required"
            else:
                if CollegeService.get_by_code(data["code"]):
                    errors["code"] = "College code already exists"

        if not data.get("name"):
            errors["name"] = "Name required"

        else:
            if "name" in data and not data["name"]:
                errors["name"] = "Name cannot be empty"


        if errors:
            raise ValidationError(errors)

from model.program import ProgramModel
from service.college_service import CollegeService
from errors.validation_error import ValidationError
from core.signals import signals
import re

class ProgramService:

    @staticmethod
    def create(data):
        ProgramService._validate_program(data)

        result = ProgramModel.add(data)
        signals.data_changed.emit("program")
        return result 

    @staticmethod
    def update(data):
        ProgramService._validate_program(data, update=True)

        result = ProgramModel.update(data)
        signals.data_changed.emit("program")
        return result

    @staticmethod
    def remove(code):
        if not code:
            raise ValidationError("Missing program code")

        result = ProgramModel.delete(code)
        signals.data_changed.emit("program")
        return result

    def get_by_code(code):
        if not code:
            raise ValidationError("Missing program code")
        return ProgramModel.get_by_code(code)

    @staticmethod
    def get(limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return ProgramModel.get_all(limit, offset, field, text, sort, sort_order)

    @staticmethod
    def count(field=None, text=None):
        return ProgramModel.count(field, text)

    @staticmethod
    def _validate_program(data, update=False):
        errors = {}
        code_pattern = r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$"


        if not update:
            if not data.get("code"):
                errors["code"] = "Code required"
            else:
                if not re.match(code_pattern, data["code"]):
                    errors["code"] = "Code must contain letters only"
                elif ProgramService.get_by_code(data["code"]):
                    errors["code"] = "Program code already exists"

            if not data.get("name"):
                errors["name"] = "Name required"

            if not data.get("college"):
                errors["college"] = "College required"
            else:
                if not CollegeService.get_by_code(data["college"]):
                    errors["college"] = "Invalid college"

            if "code" in data and not data["code"]:
                errors["code"] = "Code cannot be empty"

        else:
            if "code" in data:
                if not data["code"]:
                    errors["code"] = "Code cannot be empty"
                elif not re.match(code_pattern, data["code"]):
                    errors["code"] = "Code must contain letters only"

        if "name" in data and not data["name"]:
            errors["name"] = "Name cannot be empty"

        if "college" in data:
            if not data["college"]:
                errors["college"] = "College cannot be empty"
            else:
                if not CollegeService.get_by_code(data["college"]):
                    errors["college"] = "Invalid college"

        if errors:
            raise ValidationError(errors)

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

        code = (data.get("code") or "").strip()
        name = (data.get("name") or "").strip()
        college = (data.get("college") or "").strip()

        code_pattern = r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$"

        # Code validation
        if not code:
            errors["code"] = "Code required"

        elif not re.fullmatch(code_pattern, code):
            errors["code"] = "Code must contain letters only"

        else:
            existing = ProgramService.get_by_code(code)

            if not update:
                if existing:
                    errors["code"] = "Program code already exists"

            else:
                original_code = data.get("original_code")

                if existing and code != original_code:
                    errors["code"] = "Program code already exists"

        # Name validation
        if not name:
            errors["name"] = "Name required"

        # College validation
        if not college:
            errors["college"] = "College required"

        elif not CollegeService.get_by_code(college):
            errors["college"] = "Invalid college"

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def get_program_codes():
        return ProgramModel.get_program_codes()

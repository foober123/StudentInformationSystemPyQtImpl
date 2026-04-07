class ValidationError(Exception):
    def __init__(self, errors):
        """
        errors can be:
        - string: general error
        - dict: field-specific errors
        """
        if isinstance(errors, str):
            self.errors = {"_general": errors}
        else:
            self.errors = errors

        super().__init__(self.errors)

    def get_errors(self):
        return self.errors

    def __str__(self):
        return "\n".join(self.errors.values())

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
from errors.validation_error import ValidationError

class BaseForm(QDialog):
    def __init__(self, data=None, title_add="Add", title_edit="Edit"):
        super().__init__()

        self.data = data or {}
        self.is_edit = data is not None

        self.setWindowTitle(title_edit if self.is_edit else title_add)

        self.layout = QVBoxLayout()

        self.setup_fields()

        self.btn_submit = QPushButton(
            "Update" if self.is_edit else "Add"
        )
        self.layout.addWidget(self.btn_submit)

        self.setLayout(self.layout)

        if self.is_edit:
            self.load_data()

        self.btn_submit.clicked.connect(self.handle_submit)

    # ---------- CORE ----------
    def handle_submit(self):
        data = self.get_data()

        try:
            self.submit_data(data)
            self.accept()

        except Exception as e:
            self.show_errors(e)

    # ---------- UI ERROR HANDLING ----------
    def show_errors(self, error):
        QMessageBox.warning(self, "Error", str(error))

    # ---------- HOOKS ----------
    def setup_fields(self):
        pass

    def load_data(self):
        pass

    def get_data(self):
        raise NotImplementedError

    def submit_data(self, data):
        """Child must call service here"""
        raise NotImplementedError

    def show_errors(self, error):

        # clear previous styles
        for field in self.get_field_map().values():
            field.setStyleSheet("")

        if isinstance(error, ValidationError):
            errors = error.get_errors()

            messages = []

            for key, message in errors.items():
                messages.append(message)

                field = self.get_field_map().get(key)
                if field:
                    field.setStyleSheet("border: 1px solid red;")

            QMessageBox.warning(self, "Validation Error", "\n".join(messages))
        else:
            QMessageBox.warning(self, "Error", str(error))


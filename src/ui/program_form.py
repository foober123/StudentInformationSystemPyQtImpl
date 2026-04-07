from PyQt5.QtWidgets import QLabel, QLineEdit
from ui.base_form import BaseForm
from service.programService import ProgramService

class ProgramForm(BaseForm):
    def submit_data(self, data):
        if self.is_edit:
            ProgramService.update(data)
        else:
            ProgramService.create(data)


    def __init__(self, data=None):
        super().__init__(
            data,
            title_add="Add Program",
            title_edit="Edit Program"
        )

    def setup_fields(self):
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.college_code_input = QLineEdit()

        self.layout.addWidget(QLabel("Code"))
        self.layout.addWidget(self.code_input)

        self.layout.addWidget(QLabel("Name"))
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(QLabel("College Code"))
        self.layout.addWidget(self.college_code_input)

    def load_data(self):
        self.code_input.setText(self.data["code"])
        self.name_input.setText(self.data["name"])
        self.college_code_input.setText(self.data["college"] or "")

        self.code_input.setDisabled(True)

    def get_data(self):
        return {
            "code": self.code_input.text().strip(),
            "name": self.name_input.text().strip(),
            "college": self.college_code_input.text().strip() or None
        }

    def get_field_map(self):
        return {
            "code": self.code_input,
            "name": self.name_input,
            "college": self.college_code_input,
        }

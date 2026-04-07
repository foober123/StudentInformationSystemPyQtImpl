from PyQt5.QtWidgets import QLabel, QLineEdit
from ui.base_form import BaseForm
from service.collegeService import CollegeService

class CollegeForm(BaseForm):
    def submit_data(self, data):
        if self.is_edit:
            CollegeService.update(data)
        else:
            CollegeService.create(data)



    def __init__(self, data=None):
        super().__init__(
            data,
            title_add="Add College",
            title_edit="Edit College"
        )

    def setup_fields(self):
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()

        self.layout.addWidget(QLabel("Code"))
        self.layout.addWidget(self.code_input)
        self.layout.addWidget(QLabel("Name"))
        self.layout.addWidget(self.name_input)

    def load_data(self):
        self.code_input.setText(self.data["code"])
        self.name_input.setText(self.data["name"])

        self.code_input.setDisabled(True)

    def get_data(self):
        return {
            "code": self.code_input.text().strip(),
            "name": self.name_input.text().strip()
        }

    def get_field_map(self):
        return {
            "code": self.code_input,
            "name": self.name_input,
        }

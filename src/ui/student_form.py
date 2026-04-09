from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from ui.base_form import BaseForm
from service.student_service import StudentService


class StudentForm(BaseForm):
    def __init__(self, data=None):
        super().__init__(
            data,
            title_add="Add Student",
            title_edit="Edit Student"
        )

    def setup_fields(self):
        self.id_input = QLineEdit()
        self.firstname_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.course_input = QLineEdit()

        self.year_input = QComboBox()
        self.year_input.addItems(["1", "2", "3", "4", "5"])

        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Male", "Female", "Other"])

        self.layout.addWidget(QLabel("ID"))
        self.layout.addWidget(self.id_input)

        self.layout.addWidget(QLabel("First Name"))
        self.layout.addWidget(self.firstname_input)

        self.layout.addWidget(QLabel("Last Name"))
        self.layout.addWidget(self.lastname_input)

        self.layout.addWidget(QLabel("Program"))
        self.layout.addWidget(self.course_input)

        self.layout.addWidget(QLabel("Year (1-5)"))
        self.layout.addWidget(self.year_input)

        self.layout.addWidget(QLabel("Gender"))
        self.layout.addWidget(self.gender_input)

    def load_data(self):
        self.id_input.setText(self.data["id"])
        self.firstname_input.setText(self.data["firstname"])
        self.lastname_input.setText(self.data["lastname"])
        self.course_input.setText(self.data["course"] or "")

        self.year_input.setCurrentText(str(self.data["year"] or ""))

        self.gender_input.setCurrentText(self.data["gender"] or "")

        self.id_input.setDisabled(True)

    def get_data(self):
        year_text = self.year_input.currentText()

        return {
            "id": self.id_input.text().strip(),
            "firstname": self.firstname_input.text().strip(),
            "lastname": self.lastname_input.text().strip(),
            "course": self.course_input.text().strip() or None,

            "year": int(year_text) if year_text.isdigit() else None,

            "gender": self.gender_input.currentText() or None
        }

    def submit_data(self, data):
        if self.is_edit:
            StudentService.update_student(data)
        else:
            StudentService.create_student(data)

    def get_field_map(self):
        return {
            "id": self.id_input,
            "firstname": self.firstname_input,
            "lastname": self.lastname_input,
            "course": self.course_input,
            "year": self.year_input,
            "gender": self.gender_input,
        }

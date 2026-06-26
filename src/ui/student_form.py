from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from ui.base_form import BaseForm
from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter
from service.student_service import StudentService
from service.program_service import ProgramService

class StudentForm(BaseForm):
    def __init__(self, data=None):
        self.original_id = data["id"] if data else None
        super().__init__(
            data,
            title_add="Add Student",
            title_edit="Edit Student"
        )

    def setup_fields(self):
        self.id_input = QLineEdit()
        self.firstname_input = QLineEdit()
        self.lastname_input = QLineEdit()
        
        self.course_input = QComboBox()

        self.load_programs()

        self.course_input.setEditable(True)
        self.course_input.setInsertPolicy(QComboBox.NoInsert)
        self.course_input.lineEdit().setPlaceholderText("Search program...")

        completer = QCompleter(self.course_input.model(), self.course_input)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.course_input.setCompleter(completer)


        self.course_input.setMaxVisibleItems(12)

        self.course_input.setStyleSheet("""
        QComboBox QAbstractItemView {
            max-height: 240px;
            outline: 0px;
        }
        QComboBox {
            combobox-popup: 0;
        }
        """)


        self.year_input = QComboBox()
        self.year_input.addItems(["1", "2", "3", "4", "5"])

        self.gender_input = QComboBox()
        self.gender_input.addItems(["— Select Gender —", "Male", "Female", "Other"])
        item = self.gender_input.model().item(0)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

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
        self.course_input.setCurrentText(self.data["course"] or "")

        self.year_input.setCurrentText(str(self.data["year"] or ""))

        self.gender_input.setCurrentText(self.data["gender"] or "")

        #self.id_input.setDisabled(True)

    def get_data(self):
        year_text = self.year_input.currentText()

        gender = (
            None
            if self.gender_input.currentIndex() == 0
            else self.gender_input.currentText()
        )


        return {
            "original_id": self.original_id,
            "id": self.id_input.text().strip(),
            "firstname": self.firstname_input.text().strip(),
            "lastname": self.lastname_input.text().strip(),
            "course": self.course_input.currentText() or None,

            "year": int(year_text) if year_text.isdigit() else None,

            "gender": gender
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

    def load_programs(self):
        self.course_input.clear()
        self.course_input.addItem("— Select Program —", None)

        item = self.course_input.model().item(0)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

        for code in ProgramService.get_program_codes():
            self.course_input.addItem(code)

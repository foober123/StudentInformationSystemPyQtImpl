from PyQt5.QtWidgets import QLabel, QLineEdit, QCompleter, QComboBox
from PyQt5.QtCore import Qt
from ui.base_form import BaseForm
from service.program_service import ProgramService
from service.college_service import CollegeService

class ProgramForm(BaseForm):
    def submit_data(self, data):
        if self.is_edit:
            ProgramService.update(data)
        else:
            ProgramService.create(data)


    def __init__(self, data=None):
        self.original_code = data["code"] if data else None

        super().__init__(
            data,
            title_add="Add Program",
            title_edit="Edit Program"
        )

    def setup_fields(self):
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.college_code_input = QComboBox()


        self.load_colleges()

        self.college_code_input.setEditable(True)
        self.college_code_input.setInsertPolicy(QComboBox.NoInsert)
        self.college_code_input.lineEdit().setPlaceholderText("Search program...")

        completer = QCompleter(self.college_code_input.model(), self.college_code_input)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.college_code_input.setCompleter(completer)


        self.college_code_input.setMaxVisibleItems(12)

        self.college_code_input.setStyleSheet("""
        QComboBox QAbstractItemView {
            max-height: 240px;
            outline: 0px;
        }
        QComboBox {
            combobox-popup: 0;
        }
        """)


        self.layout.addWidget(QLabel("Code"))
        self.layout.addWidget(self.code_input)

        self.layout.addWidget(QLabel("Name"))
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(QLabel("College Code"))
        self.layout.addWidget(self.college_code_input)

    def load_data(self):
        self.code_input.setText(self.data["code"])
        self.name_input.setText(self.data["name"])

        college = self.data["college"]

        if college:
            index = self.college_code_input.findText(college, Qt.MatchFixedString)
            if index >= 0:
                self.college_code_input.setCurrentIndex(index)

    def get_data(self):
        college = self.college_code_input.currentText().strip()

        if not college or college == "— Select College —":
            college = None

        return {
            "original_code": self.original_code,
            "code": self.code_input.text().strip(),
            "name": self.name_input.text().strip(),
            "college": college,
        }


    def get_field_map(self):
        return {
            "code": self.code_input,
            "name": self.name_input,
            "college": self.college_code_input,
        }

    def load_colleges(self):
        self.college_code_input.clear()
        self.college_code_input.addItem("— Select College —", None)

        item = self.college_code_input.model().item(0)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

        for code in CollegeService.get_college_codes():
            self.college_code_input.addItem(code)

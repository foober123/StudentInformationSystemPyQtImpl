from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
import qtawesome as qta
from core.signals import signals

from ui.studentTable import StudentTable
from ui.programTable import ProgramTable
from ui.collegeTable import CollegeTable


class Dashboard(QWidget):
    def get_current_page(self):
        return self.stack.currentWidget()


    def handle_add(self):
        page = self.get_current_page()
        if hasattr(page, "add_item"):
            page.add_item()


    def handle_edit(self):
        page = self.get_current_page()
        if hasattr(page, "edit_item"):
            page.edit_item()


    def handle_delete(self):
        page = self.get_current_page()
        if hasattr(page, "delete_item"):
            page.delete_item()

    def handle_data_change(self, entity):
        self.student_page.page = 0
        self.program_page.page = 0
        self.college_page.page = 0

        if entity == "college":
            self.college_page.apply_search()
            self.program_page.apply_search()
            self.student_page.apply_search()

        elif entity == "program":
            self.program_page.apply_search()
            self.student_page.apply_search()

        elif entity == "student":
            self.student_page.apply_search()

    def setup_signals(self):
        signals.data_changed.connect(self.handle_data_change)

    def __init__(self):
        super().__init__()


        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        self.btn_add.setIcon(qta.icon('fa5s.plus'))
        self.btn_edit.setIcon(qta.icon('fa5s.edit'))
        self.btn_delete.setIcon(qta.icon('fa5s.trash'))

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_delete)

        self.btn_add.clicked.connect(self.handle_add)
        self.btn_edit.clicked.connect(self.handle_edit)
        self.btn_delete.clicked.connect(self.handle_delete)
        # Buttons
        self.btn_students = QPushButton("Students")
        self.btn_programs = QPushButton("Programs")
        self.btn_colleges = QPushButton("Colleges")

        button_layout.addWidget(self.btn_students)
        button_layout.addWidget(self.btn_programs)
        button_layout.addWidget(self.btn_colleges)

        self.stack = QStackedWidget()

        self.student_page = StudentTable()
        self.program_page = ProgramTable()
        self.college_page = CollegeTable()

        self.stack.addWidget(self.student_page)   
        self.stack.addWidget(self.program_page)   
        self.stack.addWidget(self.college_page) 

        self.btn_students.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_programs.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_colleges.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)
        self.setup_signals()

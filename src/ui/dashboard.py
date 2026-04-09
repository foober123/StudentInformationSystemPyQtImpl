from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget
)
import qtawesome as qta

from core.signals import signals
from ui.student_table import StudentTable
from ui.program_table import ProgramTable
from ui.college_table import CollegeTable


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- MAIN LAYOUT ----------
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ---------- TOP ACTION BAR ----------
        action_layout = QHBoxLayout()

        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        self.btn_add.setIcon(qta.icon('fa5s.plus'))
        self.btn_edit.setIcon(qta.icon('fa5s.edit'))
        self.btn_delete.setIcon(qta.icon('fa5s.trash'))

        action_layout.addWidget(self.btn_add)
        action_layout.addWidget(self.btn_edit)
        action_layout.addWidget(self.btn_delete)

        action_layout.addStretch()  # push navigation buttons to the right

        # ---------- PAGE SWITCH BUTTONS ----------
        self.btn_students = QPushButton("Students")
        self.btn_programs = QPushButton("Programs")
        self.btn_colleges = QPushButton("Colleges")

        action_layout.addWidget(self.btn_students)
        action_layout.addWidget(self.btn_programs)
        action_layout.addWidget(self.btn_colleges)

        # ---------- STACK ----------
        self.stack = QStackedWidget()

        self.student_page = StudentTable()
        self.program_page = ProgramTable()
        self.college_page = CollegeTable()

        self.stack.addWidget(self.student_page)
        self.stack.addWidget(self.program_page)
        self.stack.addWidget(self.college_page)

        # ---------- SIGNAL CONNECTIONS ----------
        self.btn_add.clicked.connect(self.handle_add)
        self.btn_edit.clicked.connect(self.handle_edit)
        self.btn_delete.clicked.connect(self.handle_delete)

        self.btn_students.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_programs.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_colleges.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        signals.data_changed.connect(self.handle_data_change)

        # ---------- FINAL ASSEMBLY ----------
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    # ---------- HELPERS ----------
    def get_current_page(self):
        return self.stack.currentWidget()

    # ---------- CRUD HANDLERS ----------
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

    # ---------- DATA SYNC ----------
    def handle_data_change(self, entity):
        # reset pagination
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

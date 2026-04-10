from ui.base_table import BaseTable
from service.student_service import StudentService
from ui.student_form import StudentForm
from PyQt5.QtWidgets import QMessageBox

class StudentTable(BaseTable):
    def add_item(self):
        dialog = StudentForm()

        if dialog.exec_():
            self.load_data()

    def edit_item(self):
        student_id = self.get_selected_id()

        if not student_id:
            QMessageBox.warning(self, "Error", "Select a student first")
            return

        student = StudentService.get_student_by_id(student_id)

        dialog = StudentForm(student)

        if dialog.exec_():
            self.load_data()

    def delete_item(self):
        code = self.get_selected_id()

        if not code:
            QMessageBox.warning(self, "Error", "Select a student first")
            return

        reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Delete Student '{code}'?",
                QMessageBox.Yes | QMessageBox.No
                )

        if reply != QMessageBox.Yes:
            return

        try:
            success = StudentService.remove(code)

            if not success:
                QMessageBox.warning(self, "Error", "Delete failed")
                return

            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def get_column_map(self):
        return {
            0: "s.id",
            1: "s.firstname",
            2: "s.lastname",
            3: "p.name",
            4: "c.name",
            5: "s.year",
            6: "s.gender",
        }

    def __init__(self):
        super().__init__(page_size=10)

        self.setup_search_fields()

    def setup_search_fields(self):
        self.search_field_box.addItem("ID", "s.id")
        self.search_field_box.addItem("First Name", "s.firstname")
        self.search_field_box.addItem("Last Name", "s.lastname")
        self.search_field_box.addItem("Program", "p.name")
        self.search_field_box.addItem("College", "c.name")
        self.search_field_box.addItem("Year", "s.year")
        self.search_field_box.addItem("Gender", "s.gender")

    def get_query(self, limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return StudentService.get_students(limit, offset, field, text, sort, sort_order)

    def get_total_count(self, field=None, text=None):
        return StudentService.count_students(field, text)

    def setup_headers(self):
        self.model.setHeaderData(0, 1, "ID")
        self.model.setHeaderData(1, 1, "First Name")
        self.model.setHeaderData(2,1, "Last Name")
        self.model.setHeaderData(3,1, "Program")
        self.model.setHeaderData(4,1, "College")
        self.model.setHeaderData(5,1, "Year")
        self.model.setHeaderData(6,1, "Gender")

    def get_detail_fields(self):
        return [
            ("ID", 0),
            ("First Name", 1),
            ("Last Name", 2),
            ("Program", 3),
            ("College", 4),
            ("Year", 5),
            ("Gender", 6),
        ]


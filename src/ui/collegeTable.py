from ui.base_table import BaseTable
from service.collegeService import CollegeService
from PyQt5.QtWidgets import QMessageBox
from ui.college_form import CollegeForm

class CollegeTable(BaseTable):
    def add_item(self):
        dialog = CollegeForm()

        if dialog.exec_():
            self.load_data()

    def edit_item(self):
        code = self.get_selected_id()

        if not code:
            QMessageBox.warning(self, "Error", "Select a program first")
            return

        college = CollegeService.get_by_code(code)

        dialog = CollegeForm(college)

        if dialog.exec_():
            self.load_data()

    def delete_item(self):
        code = self.get_selected_id()

        if not code:
            QMessageBox.warning(self, "Error", "Select a college first")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete college '{code}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            success = CollegeService.remove(code)

            if not success:
                QMessageBox.warning(self, "Error", "Delete failed")
                return

            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def __init__(self):
        super().__init__(page_size=10)

        self.setup_search_fields()

    def setup_search_fields(self):
        self.search_field_box.addItem("Code", "code")
        self.search_field_box.addItem("Name", "name")

    def get_query(self, limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return CollegeService.get(limit, offset, field, text, sort, sort_order)

    def get_total_count(self, field=None, text=None):
        return CollegeService.count(field, text)

    def get_column_map(self):
        return {
        0: "code",
        1: "name"
        }


    def setup_headers(self):
        self.model.setHeaderData(0, 1, "Code")
        self.model.setHeaderData(1, 1, "Name")

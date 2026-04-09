from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QSizePolicy
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QHeaderView, QMessageBox
from ui.base_table import BaseTable
from service.program_service import ProgramService
from ui.program_form import ProgramForm
from errors.validation_error import ValidationError

class ProgramTable(BaseTable):
    def add_item(self):
        dialog = ProgramForm()

        if dialog.exec_():
            self.load_data()

    def edit_item(self):
        code = self.get_selected_id()

        if not code:
            QMessageBox.warning(self, "Error", "Select a program first")
            return

        program = ProgramService.get_by_code(code)

        dialog = ProgramForm(program)

        if dialog.exec_():
            self.load_data()


    def delete_item(self):
        code = self.get_selected_id()

        if not code:
            QMessageBox.warning(self, "Error", "Select a program first")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete program '{code}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            success = ProgramService.remove(code)

            if not success:
                QMessageBox.warning(self, "Error", "Delete failed")
                return

            self.load_data()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def get_column_map(self):
        return {
            0: "p.code",
            1: "p.name",
            2: "c.code",
        }

    def __init__(self):
        super().__init__(page_size=10)

        self.setup_search_fields()

    def setup_search_fields(self):
        self.search_field_box.addItem("Code", "p.code")
        self.search_field_box.addItem("Name", "p.name")
        self.search_field_box.addItem("College", "c.code")

    def get_query(self, limit, offset, field=None, text=None, sort=None, sort_order="ASC"):
        return ProgramService.get(limit, offset, field, text, sort, sort_order)

    def get_total_count(self, field=None, text=None):
        return ProgramService.count(field, text)

    def setup_headers(self):
        self.model.setHeaderData(0, 1, "Program Code")
        self.model.setHeaderData(1, 1, "Name")
        self.model.setHeaderData(2,1, "College Code")



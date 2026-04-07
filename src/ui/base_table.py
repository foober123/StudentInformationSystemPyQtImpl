from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableView,
    QPushButton, QHBoxLayout, QLabel,
    QSizePolicy, QLineEdit, QComboBox
)
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QHeaderView


class BaseTable(QWidget):
    def __init__(self, page_size=10):
        super().__init__()

        self.page = 0
        self.page_size = page_size

        self.search_text = ""
        self.search_field = None

        self.layout = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.table = QTableView()
        self.pagination_layout = QHBoxLayout()

        self.model = QSqlQueryModel()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")

        self.search_field_box = QComboBox()

        self.btn_search = QPushButton("Search")
        self.btn_clear = QPushButton("Clear")

        self.top_bar.addWidget(self.search_field_box)
        self.top_bar.addWidget(self.search_input)
        self.top_bar.addWidget(self.btn_search)
        self.top_bar.addWidget(self.btn_clear)

        self.btn_prev = QPushButton("Previous")
        self.btn_next = QPushButton("Next")
        self.page_label = QLabel()

        self.pagination_layout.addWidget(self.btn_prev)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.btn_next)

        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.table, stretch=1)
        self.layout.addLayout(self.pagination_layout)
        self.setLayout(self.layout)

        self.sort_column = None
        self.sort_order = "ASC"
        self.table.setSortingEnabled(False) 

        header = self.table.horizontalHeader()
        header.sectionClicked.connect(self.handle_sort)

        # Signals
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_search.clicked.connect(self.apply_search)
        self.btn_clear.clicked.connect(self.clear_search)

        self.load_data()

    def get_query(self, limit, offset, search_field=None, search_text=None, sort_column=None, sort_order="ASC"):
        raise NotImplementedError

    def get_total_count(self, search_field=None, search_text=None):
        raise NotImplementedError

    def setup_headers(self):
        pass

    def setup_search_fields(self):
        """Child defines searchable fields"""
        pass

    # ---------- CORE ----------
    def load_data(self):
        total = self.get_total_count(self.search_field, self.search_text)
        max_page = (total - 1) // self.page_size if total else 0

        if self.page > max_page:
            self.page = max_page

        offset = self.page * self.page_size

        sql, values = self.get_query(
            self.page_size,
            offset,
            self.search_field,
            self.search_text,
            self.sort_column,
            self.sort_order
        )

        final_sql = sql
        for v in values:
            if isinstance(v, str):
                v = v.replace("'", "''")  # escape quotes
                final_sql = final_sql.replace("?", f"'{v}'", 1)
            else:
                final_sql = final_sql.replace("?", str(v), 1)

        self.model = QSqlQueryModel()
        self.model.setQuery(final_sql)   # ✅ PASS STRING, NOT QSqlQuery
        self.table.setModel(self.model)

        self.setup_headers()
        self.update_page_label()


    def apply_search(self):
        text = self.search_input.text().strip()

        self.search_text = text if text else None
        self.search_field = self.search_field_box.currentData() if text else None
        self.page = 0
        self.load_data()

    def clear_search(self):
        self.search_input.clear()
        self.search_text = ""
        self.search_field = None
        self.page = 0
        self.load_data()

    def next_page(self):
        total = self.get_total_count(self.search_field, self.search_text)
        max_page = (total - 1) // self.page_size

        if self.page < max_page:
            self.page += 1
            self.load_data()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_data()

    def update_page_label(self):
        total = self.get_total_count(self.search_field, self.search_text)
        max_page = (total - 1) // self.page_size + 1 if total else 1

        self.page_label.setText(f"Page {self.page + 1} of {max_page}")

        self.btn_prev.setEnabled(self.page > 0)
        self.btn_next.setEnabled(self.page < max_page - 1)

    def get_selected_id(self):
        index = self.table.currentIndex()
        if not index.isValid():
            return None
        return self.model.data(self.model.index(index.row(), 0))

    def handle_sort(self, column_index):
        column_map = self.get_column_map()

        if column_index not in column_map:
            return

        selected_column = column_map[column_index]

    # Toggle ASC/DESC if same column
        if self.sort_column == selected_column:
            self.sort_order = "DESC" if self.sort_order == "ASC" else "ASC"
        else:
            self.sort_column = selected_column
            self.sort_order = "ASC"

        self.page = 0  # reset to first page
        self.load_data()

    def get_column_map(self):
        """Child must map table column index → SQL column"""
        return {}

from PyQt5.QtWidgets import (
    QGridLayout, QWidget, QVBoxLayout, QTableView,
    QPushButton, QHBoxLayout, QLabel,
    QSizePolicy, QLineEdit, QComboBox
)
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QFormLayout, QGroupBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

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

        self.btn_first = QPushButton("<<")
        self.btn_prev = QPushButton("<")
        self.page_label = QLabel()
        self.btn_next = QPushButton(">")
        self.btn_last = QPushButton(">>")

        # Center the pagination
        pagination_container = QHBoxLayout()
        pagination_container.addStretch()

        pagination_container.addWidget(self.btn_first)
        pagination_container.addWidget(self.btn_prev)
        pagination_container.addWidget(self.page_label)
        pagination_container.addWidget(self.btn_next)
        pagination_container.addWidget(self.btn_last)

        pagination_container.addStretch()


        self.details_group = QGroupBox("Details")
        self.details_layout = QGridLayout() 
        self.details_group.setLayout(self.details_layout)

        self.details_labels = []  # store value labels


        self.details_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.table, stretch=3)



        self.layout.addWidget(self.details_group, stretch=2)


        self.layout.addLayout(pagination_container)



        self.setLayout(self.layout)

        self.sort_column = None
        self.sort_order = "ASC"
        self.table.setSortingEnabled(False) 

        header = self.table.horizontalHeader()
        header.sectionClicked.connect(self.handle_sort)

        # Signals

        self.btn_first.clicked.connect(self.first_page)
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_last.clicked.connect(self.last_page)

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

        query = QSqlQuery()
        query.prepare(sql)

        for value in values:
            query.addBindValue(value)

        if not query.exec():
            print("SQL Error:", query.lastError().text())
            return

        self.model = QSqlQueryModel()
        self.model.setQuery(query)

        if self.model.lastError().isValid():
            print("Model Error:", self.model.lastError().text())

        self.table.setModel(self.model)

        self.setup_details_panel()
        self.table.selectionModel().selectionChanged.connect(self.update_details)


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

    def first_page(self):
        if self.page != 0:
            self.page = 0
            self.load_data()


    def last_page(self):
        total = self.get_total_count(self.search_field, self.search_text)
        max_page = (total - 1) // self.page_size if total else 0

        if self.page != max_page:
            self.page = max_page
            self.load_data()

    def update_page_label(self):
        total = self.get_total_count(self.search_field, self.search_text)
        max_page = (total - 1) // self.page_size + 1 if total else 1

        self.page_label.setText(f"Page {self.page + 1} of {max_page}")

        at_start = self.page == 0
        at_end = self.page >= max_page - 1

        self.btn_first.setEnabled(not at_start)
        self.btn_prev.setEnabled(not at_start)
        self.btn_next.setEnabled(not at_end)
        self.btn_last.setEnabled(not at_end)

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


    def update_details(self):
        index = self.table.currentIndex()

        if not index.isValid():
            for lbl in self.details_labels:
                lbl.setText("-")
            return

        row = index.row()
        fields = self.get_detail_fields()

        for i, (_, col) in enumerate(fields):
            value = self.model.data(self.model.index(row, col))
            self.details_labels[i].setText(str(value))

    def get_detail_fields(self):
        """
        Should return list of tuples:
        [("Label Name", column_index)]
        """
        return []

    def setup_details_panel(self):

        grid = self.details_layout

        # Clear existing items
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        grid.setAlignment(Qt.AlignTop)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)

        self.details_labels = []

        fields = self.get_detail_fields()

        for i, (label_text, _) in enumerate(fields):
            title = QLabel(label_text.upper())
            title.setStyleSheet("""
                font-size: 11px;
                color: gray;
            """)

            value = QLabel("-")
            value.setWordWrap(True)
            value.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
            """)

            self.details_labels.append(value)

            row = i // 2
            col = i % 2

            container = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.addWidget(title)
            layout.addWidget(value)
            container.setLayout(layout)

            container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

            container.setStyleSheet("""
                QWidget {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)

            grid.addWidget(container, row, col)


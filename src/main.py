import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from database.db import connect_db
from ui.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.resize(1280, 800)

        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

def main():
    app = QApplication(sys.argv)

    connect_db()

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

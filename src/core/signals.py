from PyQt5.QtCore import QObject, pyqtSignal

class AppSignals(QObject):
    data_changed = pyqtSignal(str)

signals = AppSignals()

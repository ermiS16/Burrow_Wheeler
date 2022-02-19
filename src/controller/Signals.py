from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    valueChanged = pyqtSignal()

import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Burrow Wheeler")
        self.show()


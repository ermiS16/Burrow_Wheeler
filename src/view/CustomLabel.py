from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel


class CustomLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)
from enum import Enum

from PyQt5.QtWidgets import QMessageBox

class WARNING(Enum):
    NO_INPUT = 'Eingabe muss mindestens 3 Zeichen lang sein'
    NO_INDEX = "Bitte Index eingeben"
    INVALID_INDEX = "Index darf nicht größer als Textlänge sein"
    NO_DIRECTION = "Bitte Richtung auswählen"

class Warning(QMessageBox):
    def __init__(self, arg1):
        super(Warning, self).__init__()
        self.setIcon(QMessageBox.Warning)

    def showWarning(self, msg):
        self.setWindowTitle("Ungültige Eingabe")
        self.setText(msg.value)
        self.show()

from controller.Gui import Gui
from PyQt5.QtWidgets import QApplication
import sys

    #################### APP Entry Point ####################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Gui()
    sys.exit(app.exec())


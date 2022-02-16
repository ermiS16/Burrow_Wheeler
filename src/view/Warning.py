from PyQt5.QtWidgets import QMessageBox


class Warning(QMessageBox):
    def __init__(self, arg1):
        super(Warning, self).__init__()
        self.setIcon(QMessageBox.Warning)

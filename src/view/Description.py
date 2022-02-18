from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout

class Description(QScrollArea):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.Alignment(Qt.AlignLeft | Qt.AlignTop))

        self.label.setWordWrap(True)

        lay.addWidget(self.label)

        self._descriptions = {}

    def setDescription(self, desc):
        self.removeDescription()
        if desc:
            self.label.setText(desc)

    def removeDescription(self):
        self.label.setText("")
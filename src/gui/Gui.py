import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea
from PyQt5.QtGui import QFont, QColor, QTextFormat
from PyQt5.QtCore import Qt, QSize, QRect


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.input_text = ""
        self.input_delta = 0
        self.showDeltaInput = True
        self.initUI()

    def initUI(self):
        screen_resolution = self.screen().geometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        print (str(screen_width) + ", " + str(screen_height))
        window_width = round(screen_width * 0.8)
        window_height = round(screen_height * 0.8)

        self.setGeometry(10, 10, window_width, window_height)
        self.setWindowTitle("Burrow Wheeler")
        self.createMenu()
        self.initLayout()
        self.initMainFrameControl()

        self.setCentralWidget(self.mainFrameWidget)
        #        self.testLayout(1)
        #        self.testLayout(2)
        #        self.testLayout(3)
        #        self.addLabel("Input", 0, 15)
        #        self.initButtons()
        #        self.initInputLine()
        self.show()

    def testLayout(self, value):
        label = QLabel("Label " + str(value))
        self.h_container_left_main.addWidget(label)


    def initLayout(self):
        print(str(self.frameGeometry().width()))
        print(str(self.frameGeometry().height()))

        mainFrameControlWidth = round(self.frameGeometry().width())
        mainFrameControlHeight = round(self.frameGeometry().height() / 100)

        print(str(mainFrameControlWidth))
        print(str(mainFrameControlHeight))

        self.mainFrameLayout = QVBoxLayout()
        self.mainFrameControl = QHBoxLayout()
        self.mainFrameControl.setGeometry(QRect(0, 0, mainFrameControlWidth, mainFrameControlHeight))

        self.mainFrameContent = QHBoxLayout()

        self.mainContentLeft = QVBoxLayout()
        self.mainContentLeftControl = QHBoxLayout()
        #        self.initMainFrameControl()
        self.mainContentLeftView = QVBoxLayout()
        self.mainContentLeft.addLayout(self.mainContentLeftControl)
        self.mainContentLeft.addLayout(self.mainContentLeftView)

        self.mainContentRight = QVBoxLayout()
        self.mainContentRightView = QVBoxLayout()
        self.mainContentRight.addLayout(self.mainContentRightView)

        self.mainFrameContent.addLayout(self.mainContentLeft)
        self.mainFrameContent.addLayout(self.mainContentRight)

        self.mainFrameLayout.addLayout(self.mainFrameControl)
        self.mainFrameLayout.addLayout(self.mainFrameContent)
        self.mainFrameWidget.setLayout(self.mainFrameLayout)


    def initMainFrameControl(self):
        self.mainFrameControl.addStretch()
        self.mainFrameControlTextInput = QLineEdit()
        self.mainFrameControlTextInput.setPlaceholderText("Wikipedia!")
        labelTextInput = QLabel("Eingabetext: ")
        labelTextInput.setStyleSheet("border: 1px solid black;")

        self.mainFrameControlDeltaInput = QLineEdit()
        self.mainFrameControlDeltaInput.setPlaceholderText("Delta")
        self.toggleShowDeltaInput()
        # self.mainFrameControlDeltaInput.setDisabled(True)
        labelDeltaInput = QLabel("Delta: ")
        labelDeltaInput.setStyleSheet("border: 1px solid black;")

        self.mainFrameControlSubmit = QPushButton("Transformiere")
        self.mainFrameControlSubmit.clicked.connect(self.startTransform)
        self.mainFrameControlDirection = QComboBox()
        self.mainFrameControlDirection.addItems(['Vorwärts', 'Rückwärts'])
        self.mainFrameControlDirection.currentTextChanged.connect(self.initDirection)

        self.mainFrameControl.addWidget(labelTextInput)
        self.mainFrameControl.addWidget(self.mainFrameControlTextInput)
        self.mainFrameControl.addWidget(labelDeltaInput)
        self.mainFrameControl.addWidget(self.mainFrameControlDeltaInput)

        self.mainFrameControl.addWidget(self.mainFrameControlSubmit)
        self.mainFrameControl.addWidget(self.mainFrameControlDirection)
        self.mainFrameControl.addStretch()


    def initDirection(self):
        if(self.mainFrameControlDirection.currentText() == "Vorwärts"):
            self.toggleShowDeltaInput()
            self.initForward()

        if(self.mainFrameControlDirection.currentText() == "Rückwärts"):
            self.toggleShowDeltaInput()
            self.initBackwards()


    def toggleShowDeltaInput(self):
        if(self.mainFrameControlDeltaInput.isEnabled()):
            self.mainFrameControlDeltaInput.setDisabled(True)
            self.mainFrameControlDeltaInput.setToolTip("Nur bei Rückwärtstransformation verfügbar")
        else:
            self.mainFrameControlDeltaInput.setDisabled(False)
            self.mainFrameControlDeltaInput.setToolTip("")


    def startTransform(self):
        direction = self.mainFrameControlDirection.currentText()
        self.input_text = self.mainFrameControlTextInput.text()
        self.input_delta = self.mainFrameControlDeltasInput.text()

        if(direction == 'Vorwärts'):
            pass
        if(direction == 'Rückwärts'):
            pass


    def initForward(self):
        print("Vorwärts")


    def initBackwards(self):
        print("Rückwärts")


    def createMenu(self):
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)


    def addLabel(self, value, x, y):
        print("X: " + str(x) + " | Y: " + str(y) + " | " + str(value))
        label = QLabel(self)
        label.setText(value)
        label.move(x, y)
        label.setFont(QFont("Arial", 20))


    def getInput(self):
        input_text = self.input.text()



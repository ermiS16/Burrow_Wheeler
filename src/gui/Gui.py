import sys
import time
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea, QSizePolicy, QCheckBox, QGridLayout, QFormLayout
from PyQt5.QtGui import QFont, QColor, QTextFormat, QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.input_text = ""
        self.input_text_length = 0
        self.input_delta = 0
        self.rotation_step = 0
        self.showDeltaInput = True
        self.forwardInitialized = False
        self.backwardInitialized = False
        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']
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
        # self.initForward()

        self.setCentralWidget(self.mainFrameWidget)
        #        self.testLayout(1)
        #        self.testLayout(2)
        #        self.testLayout(3)
        #        self.addLabel("Input", 0, 15)
        #        self.initButtons()
        #        self.initInputLine()
        self.show()


    def addContentRow(self):
        char_list = []
        for i in range(self.input_text_length):
            label = QLabel(str(i))
            char_list.append(label)
            self.mainContentLeftViewGrid.addWidget(label, self.rotation_step, i)




    def initLayout(self):
        print(str(self.frameGeometry().width()))
        print(str(self.frameGeometry().height()))

        mainFrameControlWidth = round(self.frameGeometry().width())
        mainFrameControlHeight = round(self.frameGeometry().height() / 100)

        print(str(mainFrameControlWidth))
        print(str(mainFrameControlHeight))

        self.mainFrameLayout = QVBoxLayout()
        self.mainFrameControl = QHBoxLayout()
        self.mainFrameControl.setAlignment(Qt.AlignTop)
        #self.mainFrameControl.setGeometry(QRect(0, 0, mainFrameControlWidth, mainFrameControlHeight))

        self.mainFrameContent = QHBoxLayout()
        #self.mainFrameContent.setAlignment(Qt.AlignTop)

        self.mainContentLeft = QVBoxLayout()
        self.mainContentLeft.setAlignment(Qt.AlignTop)
        self.mainContentLeftControl = QHBoxLayout()
        #        self.initMainFrameControl()
        self.mainContentLeftView = QVBoxLayout()
        self.mainContentLeft.addLayout(self.mainContentLeftControl)
        self.mainContentLeft.addLayout(self.mainContentLeftView)
        self.mainContentLeft.addStretch()

        self.mainContentRight = QVBoxLayout()
        self.mainContentRightView = QVBoxLayout()
        self.mainContentRight.addLayout(self.mainContentRightView)
        self.mainContentRight.addStretch()

        self.mainFrameContent.addLayout(self.mainContentLeft)
        self.mainFrameContent.addLayout(self.mainContentRight)

        self.mainFrameLayout.addLayout(self.mainFrameControl)
        self.mainFrameLayout.addLayout(self.mainFrameContent)
        self.mainFrameWidget.setLayout(self.mainFrameLayout)


    def initMainFrameControl(self):
        self.mainFrameControl.addStretch()
        self.mainFrameControlTextInput = QLineEdit()
        self.mainFrameControlTextInput.setPlaceholderText("Wikipedia!")
        #self.mainFrameControlTextInput.setMaxLength(15)
        input_text_regex = QRegExp(".{2,15}")
        input_text_validator = QRegExpValidator(input_text_regex)
        self.mainFrameControlTextInput.setValidator(input_text_validator)

        labelTextInput = QLabel("Eingabetext: ")
        labelTextInput.setStyleSheet("border: 1px solid black;")

        self.mainFrameControlDeltaInput = QLineEdit()
        self.mainFrameControlDeltaInput.setPlaceholderText("Delta")
        input_delta_regex = QRegExp("\d{1,4}")
        input_delta_validator = QRegExpValidator(input_delta_regex)
        self.mainFrameControlDeltaInput.setValidator(input_delta_validator)
        #self.toggleShowDeltaInput()
        # self.mainFrameControlDeltaInput.setDisabled(True)
        labelDeltaInput = QLabel("Delta: ")
        labelDeltaInput.setStyleSheet("border: 1px solid black;")

        self.mainFrameControlSubmit = QPushButton("Transformiere")
        self.mainFrameControlSubmit.clicked.connect(self.startTransform)


        self.mainFrameControlDirection = QComboBox()
        self.mainFrameControlDirection.addItems(self.directions)
        self.mainFrameControlDirection.currentTextChanged.connect(self.initDirection)


        #self.mainFrameControl.setAlignment(Qt.AlignTop)
        self.mainFrameControl.addWidget(labelTextInput)
        self.mainFrameControl.addWidget(self.mainFrameControlTextInput)
        self.mainFrameControl.addWidget(labelDeltaInput)
        self.mainFrameControl.addWidget(self.mainFrameControlDeltaInput)

        self.mainFrameControl.addWidget(self.mainFrameControlSubmit)
        self.mainFrameControl.addWidget(self.mainFrameControlDirection)
        self.mainFrameControl.addStretch()
        #print(str(self.mainFrameControl.sizeHint()))
        #self.mainFrameControl.setStretchFactor(self, 1)


    def initDirection(self):
        direction = self.mainFrameControlDirection.currentText()
        if(direction == self.directions[0]):
            print(str(direction))
            pass

        if(direction == self.directions[1]):
            self.toggleShowDeltaInput()
            self.initForward()

        if(direction == self.directions[2]):
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
        self.input_text_length = len(self.input_text)
        self.input_delta = self.mainFrameControlDeltaInput.text()

        print(self.input_text)
        print(self.input_delta)

        if(len(self.input_text) == 0):
            pass

        if(direction == 'Vorwärts'):
            text = "Transformation Vorwärts: \n\n"
            text = text + "Der Text wird als erstes rotiert."
            self.description.setText(text)
            self.addContentRow()


        if(direction == 'Rückwärts'):
            if (len(self.input_delta) == 0 or not self.input_delta.isnumeric()):
                pass

        print("Control Test")

    def initForward(self):
        if(self.forwardInitialized):
            pass

        if(not self.forwardInitialized):
            print("Init Forward")
            step_label = QLabel("1.) Rotation")
            step_label.setStyleSheet("border: 1px solid black;")
            self.button_next = QPushButton("Next")
            self.button_next.setStyleSheet("border: 1px solid black;")
            self.button_next.clicked.connect(self.nextStep)
            self.button_prev = QPushButton("Prev")
            self.button_prev.setStyleSheet("border: 1px solid black;")
            self.button_prev.clicked.connect(self.prevStep)
            auto_label = QLabel("Auto")
            auto_label.setStyleSheet("border: 1px solid black;")
            #auto_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.auto_checkbox = QCheckBox()
            self.auto_checkbox.setChecked(False)
            self.auto_checkbox.stateChanged.connect(self.toggleAutorun)


            #self.mainContentLeftControl.setAlignment(Qt.AlignTop)
            self.mainContentLeftControl.addWidget(step_label)
            self.mainContentLeftControl.addWidget(self.button_next)
            self.mainContentLeftControl.addWidget(self.button_prev)
            self.mainContentLeftControl.addWidget(self.auto_checkbox)
            self.mainContentLeftControl.addWidget(auto_label)

            self.mainContentLeftViewGrid = QGridLayout()
            self.mainContentLeftView.addLayout(self.mainContentLeftViewGrid)

            self.mainContentRightViewEncoded = QHBoxLayout()
            encoded_label = QLabel("Encoded: ")
            encoded_label.setStyleSheet("border: 1px solid black;")
            self.encoded_value = QLabel("")
            self.encoded_value.setStyleSheet("border: 1px solid black;")
            #self.encoded_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.mainContentRightViewEncoded.addWidget(encoded_label)
            self.mainContentRightViewEncoded.addWidget(self.encoded_value)

            self.mainContentRightViewIndex = QHBoxLayout()
            index_label = QLabel("Index: ")
            index_label.setStyleSheet("border: 1px solid black;")
            self.index_value = QLabel("")
            self.index_value.setStyleSheet("border: 1px solid black;")
            self.mainContentRightViewIndex.addWidget(index_label)
            self.mainContentRightViewIndex.addWidget(self.index_value)

            self.mainContentRightViewDescription = QVBoxLayout()
            description_label = QLabel("Beschreibung")
            description_label.setStyleSheet("border: 1px solid black;")
            self.mainContentRightViewDescription.addWidget(description_label)
            self.description = QLabel("")
            self.description.setStyleSheet("border: 1px solid black;")
            #self.description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.mainContentRightViewDescription.addWidget(self.description)

            #self.mainContentRightView.setAlignment(Qt.AlignTop)
            self.mainContentRightView.addLayout(self.mainContentRightViewEncoded)
            self.mainContentRightView.addLayout(self.mainContentRightViewIndex)
            self.mainContentRightView.addLayout(self.mainContentRightViewDescription)
            self.forwardInitialized = True


    def initBackwards(self):
        print("Init Backward")
        if(self.forwardInitialized):
            self.clearForward()
        self.forwardInitialized = False
        #self.clearLayout(self.mainContentRightView)


    def clearForward(self):
        print("Clear Content Right")
        self.clearLayout(self.mainContentRightViewEncoded)
        self.clearLayout(self.mainContentRightViewIndex)
        self.clearLayout(self.mainContentRightViewDescription)
        self.clearLayout(self.mainContentLeftControl)

    def clearLayout(self, layout):
        print("Clear Layout")
        if layout.count() > 0:
            while layout.count():
                print("Count: " + str(layout.count()))
                item = layout.itemAt(0)
                widget = item.widget()
                if widget is not None:
                    print("Widget")
                    widget.setParent(None)

        print(str(layout.count()))

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


    def nextStep(self):
        print("Next Step")
        self.addContentRow()
        self.rotation_step = self.rotation_step + 1
        pass

    def prevStep(self):
        print("Prev Step")
        pass


    def toggleAutorun(self):
        if(self.auto_checkbox.isChecked()):
            self.button_next.setDisabled(True)
            self.button_prev.setDisabled(True)
            print("Autorun On")
            self.autorun()
        if(self.auto_checkbox.isChecked()):
            self.button_next.setDisabled(False)
            self.button_prev.setDisabled(False)
            print("Autorun Off")


    def autorun(self):
        print("Autorun")
        #for i in range(10):
        #    print("Step " + str(i))
        #    time.sleep(2)

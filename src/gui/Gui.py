import sys
import time
from enum import Enum
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea, QSizePolicy, QCheckBox, QGridLayout, QFormLayout, \
    QStackedLayout
from PyQt5.QtGui import QFont, QColor, QTextFormat, QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp


class STATE(Enum):
    INIT = 0
    INIT_FORWARD = 1
    INIT_BACKWARD = 2
    F_ROTATION = 3
    F_SORT = 4


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.input_text = ""
        self.input_text_length = 0
        self.input_delta = 0
        self.rotation_step = 0
        self.forwardInitialized = False
        self.backwardInitialized = False
        self.state = STATE.INIT
        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']
        self.initUI()
        self.initDirections()

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
        self.show()


    def addContentRow(self):
        if self.state == STATE.F_ROTATION:
            char_list = []
            for i in range(self.input_text_length):
                label = QLabel(str(self.input_text[i]))
                char_list.append(label)
                self.mainContentLeftViewGrid.addWidget(label, self.rotation_step, i)
        else:
            pass


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

        self.mainFrameContentStack = QStackedLayout()


        self.mainFrameLayout.addLayout(self.mainFrameControl)
        self.mainFrameLayout.addLayout(self.mainFrameContentStack)
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

        self.showDeltaInput(False)
        labelDeltaInput = QLabel("Delta: ")
        labelDeltaInput.setStyleSheet("border: 1px solid black;")

        self.mainFrameControlSubmit = QPushButton("Transformiere")
        self.mainFrameControlSubmit.clicked.connect(self.startTransform)


        self.mainFrameControlDirection = QComboBox()
        self.mainFrameControlDirection.addItems(self.directions)
        self.mainFrameControlDirection.currentTextChanged.connect(self.switchPage)


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


    def switchPage(self):
        currentDirectionIndex = self.mainFrameControlDirection.currentIndex()
        print("Current Dircetion Index: " + str(currentDirectionIndex))
        self.mainFrameContentStack.setCurrentIndex(currentDirectionIndex)
        if(currentDirectionIndex == STATE.INIT_BACKWARD.value):
            self.showDeltaInput(True)
        else:
            self.showDeltaInput(False)


    def initDirections(self):
        self.initStart()
        self.initForward()
        self.initBackwards()


    def initStart(self):
        self.page_start = QWidget()
        self.s_mainFrameContent = QHBoxLayout()

        self.s_mainContentLeft = QVBoxLayout()
        self.s_mainContentLeft.setAlignment(Qt.AlignTop)
        self.s_mainContentLeftControl = QHBoxLayout()
        self.s_mainContentLeftView = QVBoxLayout()
        self.s_mainContentLeft.addLayout(self.s_mainContentLeftControl)
        self.s_mainContentLeft.addLayout(self.s_mainContentLeftView)
        self.s_mainContentLeft.addStretch()

        self.s_mainContentRight = QVBoxLayout()
        self.s_mainContentRightView = QVBoxLayout()
        self.s_mainContentRight.addLayout(self.s_mainContentRightView)
        self.s_mainContentRight.addStretch()

        self.s_mainFrameContent.addLayout(self.s_mainContentLeft)
        self.s_mainFrameContent.addLayout(self.s_mainContentRight)

        self.page_start.setLayout(self.s_mainFrameContent)
        self.mainFrameContentStack.addWidget(self.page_start)

    def initForward(self):
        print("Init Forward")

        self.page_forward = QWidget()
        self.f_mainFrameContent = QHBoxLayout()

        self.f_mainContentLeft = QVBoxLayout()
        self.f_mainContentLeft.setAlignment(Qt.AlignTop)
        self.f_mainContentLeftControl = QHBoxLayout()
        self.f_mainContentLeftView = QVBoxLayout()
        self.f_mainContentLeft.addLayout(self.f_mainContentLeftControl)
        self.f_mainContentLeft.addLayout(self.f_mainContentLeftView)
        self.f_mainContentLeft.addStretch()

        self.f_mainContentRight = QVBoxLayout()
        self.f_mainContentRightView = QVBoxLayout()
        self.f_mainContentRight.addLayout(self.f_mainContentRightView)
        self.f_mainContentRight.addStretch()

        self.f_mainFrameContent.addLayout(self.f_mainContentLeft)
        self.f_mainFrameContent.addLayout(self.f_mainContentRight)

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
        self.f_mainContentLeftControl.addWidget(step_label)
        self.f_mainContentLeftControl.addWidget(self.button_next)
        self.f_mainContentLeftControl.addWidget(self.button_prev)
        self.f_mainContentLeftControl.addWidget(self.auto_checkbox)
        self.f_mainContentLeftControl.addWidget(auto_label)

        self.mainContentLeftViewGrid = QGridLayout()
        self.f_mainContentLeftView.addLayout(self.mainContentLeftViewGrid)

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
        self.f_mainContentRightView.addLayout(self.mainContentRightViewEncoded)
        self.f_mainContentRightView.addLayout(self.mainContentRightViewIndex)
        self.f_mainContentRightView.addLayout(self.mainContentRightViewDescription)
        self.forwardInitialized = True

        self.page_forward.setLayout(self.f_mainFrameContent)
        self.mainFrameContentStack.addWidget(self.page_forward)

    def initBackwards(self):
        print("Init Backward")

        self.page_backward = QWidget()
        self.b_mainFrameContent = QHBoxLayout()

        self.b_mainContentLeft = QVBoxLayout()
        self.b_mainContentLeft.setAlignment(Qt.AlignTop)
        self.b_mainContentLeftControl = QHBoxLayout()
        self.b_mainContentLeftView = QVBoxLayout()
        self.b_mainContentLeft.addLayout(self.b_mainContentLeftControl)
        self.b_mainContentLeft.addLayout(self.b_mainContentLeftView)
        self.b_mainContentLeft.addStretch()

        self.b_mainContentRight = QVBoxLayout()
        self.b_mainContentRightView = QVBoxLayout()
        self.b_mainContentRight.addLayout(self.b_mainContentRightView)
        self.b_mainContentRight.addStretch()

        self.b_mainFrameContent.addLayout(self.b_mainContentLeft)
        self.b_mainFrameContent.addLayout(self.b_mainContentRight)

        self.page_backward.setLayout(self.b_mainFrameContent)
        self.mainFrameContentStack.addWidget(self.page_backward)


    def showDeltaInput(self, val):
        if(val):
            self.mainFrameControlDeltaInput.setDisabled(False)
            self.mainFrameControlDeltaInput.setToolTip("")
        else:
            self.mainFrameControlDeltaInput.setDisabled(True)
            self.mainFrameControlDeltaInput.setToolTip("Nur bei Rückwärtstransformation verfügbar")


    def startTransform(self):
        direction = self.mainFrameControlDirection.currentText()
        self.input_text = self.mainFrameControlTextInput.text()
        self.input_text_length = len(self.input_text)
        self.input_delta = self.mainFrameControlDeltaInput.text()

        print(self.input_text)
        print(self.input_delta)

        if(len(self.input_text) == 0):
            # ToDO: Add user information: User has to choose direction
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


    # def clearForward(self):
    #     print("Clear Content Right")
    #     self.clearLayout(self.mainContentRightViewEncoded)
    #     self.clearLayout(self.mainContentRightViewIndex)
    #     self.clearLayout(self.mainContentRightViewDescription)
    #     self.clearLayout(self.f_mainContentLeftControl)
    #
    # def clearLayout(self, layout):
    #     print("Clear Layout")
    #     if layout.count() > 0:
    #         while layout.count():
    #             print("Count: " + str(layout.count()))
    #             item = layout.itemAt(0)
    #             widget = item.widget()
    #             if widget is not None:
    #                 print("Widget")
    #                 widget.setParent(None)
    #
    #     print(str(layout.count()))

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
        self.rotation_step = self.rotation_step - 1
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

    def setState(self, state):
        self.state = state
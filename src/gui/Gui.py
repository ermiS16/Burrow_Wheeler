import re
import sys
import time
import xml.etree.ElementTree as ET
from data import iText
from enum import Enum
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea, QSizePolicy, QCheckBox, QGridLayout, QFormLayout, \
    QStackedLayout, QLayout
from PyQt5.QtGui import QFont, QColor, QTextFormat, QRegExpValidator, QIntValidator, QCursor
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp


class STATE(Enum):
    INIT = 0
    INIT_FORWARD = 1
    INIT_BACKWARD = 2
    F_ROTATION = 3
    F_SORT = 4
    F_ENCODE = 5
    F_INDEX = 6
    F_END = 7


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.descriptions = {}
        self.input_text = None
        self.text_table = None
        self.encoded = ""
        self.test_list = []
        self.test_count = 0
        self._MAX_STEPS = 0
        self.input_delta = 0
        self.step = 0
        self.f_rotation_step = 0
        self.f_sort_step = 0
        self.f_encode_step = 0
        self.state = STATE.INIT
        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']
        self.loadDescriptions()
        self.initUI()
        self.initDirections()

    def loadDescriptions(self):
        tree = ET.parse("/home/eric/Dokumente/Repositories/hska/Burrow_Wheeler/src/data/Descriptions.xml")
        xml_root = tree.getroot()
        for child in xml_root:
            desc = child.text
            self.descriptions[child.tag] = desc.strip()

    def initUI(self):
        screen_resolution = self.screen().geometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        print (str(screen_width) + ", " + str(screen_height))
        window_width = round(screen_width * 0.5)
        window_height = round(screen_height * 0.5)

        self.setGeometry(10, 10, window_width, window_height)
        self.setWindowTitle("Burrow Wheeler")
        self.createMenu()
        self.initLayout()
        self.initMainFrameControl()

        self.setCentralWidget(self.mainFrameWidget)
        self.show()


    def createMenu(self):
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)


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

        self.mainFrameContentStack = QStackedLayout()


        self.mainFrameLayout.addLayout(self.mainFrameControl)
        self.mainFrameLayout.addLayout(self.mainFrameContentStack)
        self.mainFrameWidget.setLayout(self.mainFrameLayout)


    def initMainFrameControl(self):
        self.mainFrameControl.addStretch()
        self.mainFrameControlTextInput = QLineEdit()
        self.mainFrameControlTextInput.setPlaceholderText("Wikipedia!")
        self.mainFrameControlTextInput.setText("Wikipedia!")
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

        self.mainFrameControl.addWidget(labelTextInput)
        self.mainFrameControl.addWidget(self.mainFrameControlTextInput)
        self.mainFrameControl.addWidget(labelDeltaInput)
        self.mainFrameControl.addWidget(self.mainFrameControlDeltaInput)

        self.mainFrameControl.addWidget(self.mainFrameControlSubmit)
        self.mainFrameControl.addWidget(self.mainFrameControlDirection)
        self.mainFrameControl.addStretch()


    def switchPage(self):
        currentDirectionIndex = self.mainFrameControlDirection.currentIndex()
        print("Current Dircetion Index: " + str(currentDirectionIndex))
        self.mainFrameContentStack.setCurrentIndex(currentDirectionIndex)
        if(currentDirectionIndex == STATE.INIT_BACKWARD.value):
            self.showDeltaInput(True)
        else:
            self.showDeltaInput(False)


    def initDirections(self):
        self.initStartLayout()
        self.initForwardLayout()
        self.initBackwardLayout()


    def initStartLayout(self):
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

    def initForwardLayout(self):
        print("Init Forward")

        self.page_forward = QWidget()
        self.f_mainFrameContent = QHBoxLayout()

        self.f_mainContentLeft = QVBoxLayout()
        self.f_mainContentLeft.setAlignment(Qt.AlignTop)
        self.f_mainContentLeft.setSizeConstraint(QLayout.SetFixedSize)
        self.f_mainContentLeftControl = QHBoxLayout()
        self.f_mainContentLeftView = QVBoxLayout()
        self.f_mainContentLeft.addLayout(self.f_mainContentLeftControl)
        self.f_mainContentLeft.addLayout(self.f_mainContentLeftView)
        self.f_mainContentLeft.addStretch()

        self.f_mainContentRight = QVBoxLayout()
        self.f_mainContentRight.setSizeConstraint(QLayout.SetFixedSize)
        self.f_mainContentRightView = QVBoxLayout()
        self.f_mainContentRight.addLayout(self.f_mainContentRightView)
        self.f_mainContentRight.addStretch()

        self.f_mainFrameContent.addStretch()
        self.f_mainFrameContent.addLayout(self.f_mainContentLeft)
        self.f_mainFrameContent.addStretch()
        self.f_mainFrameContent.addLayout(self.f_mainContentRight)
        self.f_mainFrameContent.addStretch()

        self.step_label = QLabel("1.) Rotation")
        self.step_label.setStyleSheet("border: 1px solid black;")
        self.button_next = QPushButton("Next")
        self.button_next.setStyleSheet("border: 1px solid black;")
        self.button_next.clicked.connect(self.f_nextStep)
        self.button_prev = QPushButton("Prev")
        self.button_prev.setStyleSheet("border: 1px solid black;")
        self.button_prev.clicked.connect(self.f_prevStep)
        auto_label = QLabel("Auto")
        auto_label.setStyleSheet("border: 1px solid black;")
        self.auto_checkbox = QCheckBox()
        self.auto_checkbox.setChecked(False)
        self.auto_checkbox.stateChanged.connect(self.toggleAutorun)

        self.f_mainContentLeftControl.addWidget(self.step_label)
        self.f_mainContentLeftControl.addWidget(self.button_next)
        self.f_mainContentLeftControl.addWidget(self.button_prev)
        self.f_mainContentLeftControl.addWidget(self.auto_checkbox)
        self.f_mainContentLeftControl.addWidget(auto_label)

        self.mainContentLeftViewGridRotation = QGridLayout()
        self.f_mainContentLeftView.addLayout(self.mainContentLeftViewGridRotation)

        self.f_mainContentLeftView.addStretch()

        self.mainContentLeftViewGridSort = QGridLayout()
        self.f_mainContentLeftView.addLayout(self.mainContentLeftViewGridSort)

        self.mainContentRightViewEncoded = QHBoxLayout()
        encoded_label = QLabel("Encoded: ")
        encoded_label.setStyleSheet("border: 1px solid black;")
        self.encoded_value = QLabel("")
        self.encoded_value.setStyleSheet("border: 1px solid black;")
        #self.mainContentRightViewEncoded.addStretch()
        self.mainContentRightViewEncoded.addWidget(encoded_label)
        self.mainContentRightViewEncoded.addWidget(self.encoded_value)
        #self.mainContentRightViewEncoded.addStretch()

        self.mainContentRightViewIndex = QHBoxLayout()
        index_label = QLabel("Index: ")
        index_label.setStyleSheet("border: 1px solid black;")
        self.index_value = QLabel("")
        self.index_value.setStyleSheet("border: 1px solid black;")
        #self.mainContentRightViewIndex.addStretch()
        self.mainContentRightViewIndex.addWidget(index_label)
        self.mainContentRightViewIndex.addWidget(self.index_value)
        #self.mainContentRightViewIndex.addStretch()

        self.mainContentRightViewDescription = QVBoxLayout()
        description_label = QLabel("Beschreibung")
        description_label.setStyleSheet("border: 1px solid black;")

        #self.description_label_wrapper = QHBoxLayout()
        #self.description_label_wrapper.addStretch()
        #self.description_label_wrapper.addWidget(description_label)
        #self.mainContentRightViewDescription.addLayout(self.description_label_wrapper)
        #self.mainContentRightViewDescription.addWidget(description_label)

        self.description = QLabel("")
        self.description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.description.setStyleSheet("border: 1px solid black;")

        #self.descriptionWrapper = QHBoxLayout()
        #self.descriptionWrapper.addStretch()
        #self.descriptionWrapper.addWidget(self.description)
        #self.mainContentRightViewDescription.addLayout(self.descriptionWrapper)
        #self.mainContentRightViewDescription.addLayout(self.description)
        self.mainContentRightViewDescription.addWidget(self.description)

        # self.f_mainContentRightView.setSizeConstraint(QLayout.SetFixedSize)

        self.f_mainContentRightView.addLayout(self.mainContentRightViewEncoded)
        self.f_mainContentRightView.addLayout(self.mainContentRightViewIndex)
        self.f_mainContentRightView.addLayout(self.mainContentRightViewDescription)

        self.page_forward.setLayout(self.f_mainFrameContent)
        self.mainFrameContentStack.addWidget(self.page_forward)

    def initBackwardLayout(self):
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
        input = self.mainFrameControlTextInput.text()
        self.input_delta = self.mainFrameControlDeltaInput.text()
        self._MAX_STEPS = len(input)

        if(len(input) == 0):
            # ToDO: Add user information: User has to choose direction
            pass

        if(direction == 'Vorwärts'):
            self.initForwardTransformation(input)


        if(direction == 'Rückwärts'):
            pass


    def initForwardTransformation(self, input_text):
        self.setState(STATE.F_ROTATION)
        self.step = 0
        self.description.setText(self.descriptions['forward_rotation'])
        self.text_table = iText.TextTable()
        self.text_table.addText(input_text)
        self.f_addGridRotation(self.step, input_text)
        self.step = self.step + 1


    def f_nextStep(self):
        print("Next Step")
        print(self.state)

        if(self.state == STATE.F_ROTATION):
            self.printSteps()

            if(self.step < self._MAX_STEPS):
                old_text = self.text_table.getLastText()
                rotate_text = iText.rotateText(old_text)
                self.text_table.addText(rotate_text)
                self.text_table.printTable()
                self.f_addGridRotation(self.step, rotate_text)
                self.step = self.step + 1

            if(self.step == self._MAX_STEPS):
                self.setState(STATE.F_SORT)
                self.step = 0

        elif(self.state == STATE.F_SORT):
            self.printSteps()
            if self.step == 0:
                self.description.setText(self.descriptions['forward_sort'])

            if (self.step < self._MAX_STEPS):
                self.text_table.sortTable()
                self.markRotatedGrid(self.step)
                sorted_text = self.text_table.getTextAtIndex(self.text_table.getRef(self.step))
                self.f_addGridSort(self.step, sorted_text)
                self.step = self.step + 1

            if self.step == self._MAX_STEPS:
                self.setState(STATE.F_ENCODE)
                self.setColorRotationGrid("gray")
                self.step = 0

        elif(self.state == STATE.F_ENCODE):
            if self.step == 0:
                self.description.setText(self.descriptions['forward_encode'])

            if self.step < self._MAX_STEPS:
                self.setColorSortGrid("gray")
                self.markLastCharSortGrid(self.step)
                self.encoded = self.encoded + iText.getLastChar(self.text_table.getSortedTextAtIndex(self.step))
                self.encoded_value.setText(self.encoded)
                self.encoded_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.encoded_value.setCursor(QCursor(Qt.IBeamCursor))
                self.step = self.step + 1

            if self.step == self._MAX_STEPS:
                self.setState(STATE.F_INDEX)
                self.step = 0

        elif(self.state == STATE.F_INDEX):
            self.description.setText(self.descriptions['forward_index'])
            self.setColorSortGrid("gray")
            input_index = self.text_table.getRef(0)
            self.markSortGrid(input_index)
            self.index_value.setText(str(input_index+1))
            self.index_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.index_value.setCursor(QCursor(Qt.IBeamCursor))


    def markRotatedGrid(self, row):
        for i in range(self._MAX_STEPS):
            if self.text_table.getRef(row) == i:
                color = "black"
            else:
                color = "gray"
            self.setColorAtRotationGridIndex(i, color)


    def setColorRotationGrid(self, color):
        for i in range(self._MAX_STEPS):
            self.setColorAtRotationGridIndex(i, color)

    def markSortGrid(self, row):
        for i in range(self._MAX_STEPS):
            if row == i:
                color = "black"
            else:
                color = "gray"
            self.setColorAtSortGridIndex(i, color, False)

    def markLastCharSortGrid(self, row):
        for i in range(self._MAX_STEPS):
            markLastChar = False

            if i <= row:
                markLastChar = True

            self.setColorAtSortGridIndex(i, "gray", markLastChar)


    def setColorSortGrid(self, color):
        for i in range(self._MAX_STEPS):
            self.setColorAtSortGridIndex(i, color, False)



    def printSteps(self):
        print("Step: " + str(self.step))
        print()

    def f_prevStep(self):
        print("Prev Step")
        self.printSteps()

        if(self.state == STATE.F_INDEX):
            print(self.state)
            self.step = self.step - 1
            self.index_value.setText("")

            if self.step <= 0:
                self.setState(STATE.F_ENCODE)
                self.setColorSortGrid("gray")
                self.step = self._MAX_STEPS
                self.markLastCharSortGrid(self.step-1)
                self.description.setText(self.descriptions['forward_encode'])


        elif(self.state == STATE.F_ENCODE):
            print(self.state)
            self.step = self.step - 1
            self.markLastCharSortGrid(self.step)
            self.encoded = self.encoded[0:-1]
            self.encoded_value.setText(self.encoded)
            if self.step <= 0:
                self.setState(STATE.F_SORT)
                self.setColorSortGrid("black")
                self.step = self._MAX_STEPS
                self.description.setText(self.descriptions['forward_sort'])

        elif(self.state == STATE.F_SORT):
            print(self.state)
            self.step = self.step - 1

            if self.step >= 0:
                self.f_removeGridSort(self.step)
                self.markRotatedGrid(self.step)

            if (self.step <= 0):
                self.state = STATE.F_ROTATION
                self.setColorRotationGrid("black")
                self.step = self._MAX_STEPS
                self.description.setText(self.descriptions['forward_rotation'])


        elif(self.state == STATE.F_ROTATION):
            print(self.state)
            next_step = self.step - 1
            print("Rotation Next Step: " + str(next_step))

            if(next_step > 0):
                self.f_removeGridRotation(next_step)
                self.text_table.removeTextAtIndex(next_step)
                self.text_table.printTable()
                self.step = next_step


    def f_addGridRotation(self, row, text):
        if self.state == STATE.F_ROTATION:
            rotation_index = str(row + 1) + ".)"
            label = QLabel(str(rotation_index))
            self.mainContentLeftViewGridRotation.addWidget(label, row, 0)
            for i in range(len(text)):
                label = QLabel(str(text[i]))
                self.mainContentLeftViewGridRotation.addWidget(label, row, i+1)
        else:
            pass


    def f_addGridSort(self, row, text):
        if self.state == STATE.F_SORT:
            sort_index = str(row + 1) + ".)"
            label = QLabel(str(sort_index))
            self.mainContentLeftViewGridSort.addWidget(label, row, 0)
            for i in range(len(text)):
                label = QLabel(str(text[i]))
                self.mainContentLeftViewGridSort.addWidget(label, row, i+1)
        else:
            pass


    def f_clearGridRotationTable(self):
        if(self.text_table != None):
            for row in range(self.text_table.getTableLength()):
                self.f_removeGridRotation(row)


    def f_removeGridRotation(self, row):
        for i in range(self._MAX_STEPS+1):
            entry = self.mainContentLeftViewGridRotation.itemAtPosition(row, i)
            if(entry != None):
                entry.widget().deleteLater()

    def f_removeGridSort(self, row):
        for i in range(self._MAX_STEPS+1):
            entry = self.mainContentLeftViewGridSort.itemAtPosition(row, i)
            if(entry != None):
                entry.widget().deleteLater()

    def setColorAtRotationGridIndex(self, row, color):
        for i in range(self._MAX_STEPS+1):
            entry = self.mainContentLeftViewGridRotation.itemAtPosition(row, i)
            if entry != None:
                widget = entry.widget()
                styleSheet = r"color: " + str(color) + ";"
                widget.setStyleSheet(styleSheet)


    def setColorAtSortGridIndex(self, row, color, markLastChar):
        max_length = self._MAX_STEPS+1
        entry = None
        for i in range(max_length):
            entry = self.mainContentLeftViewGridSort.itemAtPosition(row, i)
            if entry != None:
                widget = entry.widget()
                styleSheet = r"color: " + str(color) + ";"
                widget.setStyleSheet(styleSheet)
        if markLastChar:
            widget = entry.widget()
            widget.setStyleSheet(r"color: black;")




    def toggleAutorun(self):
        if(self.auto_checkbox.isChecked()):
            #self.button_next.setDisabled(True)
            #self.button_prev.setDisabled(True)
            #print("Autorun On")
            self.autorun()
        if(self.auto_checkbox.isChecked()):
            #self.button_next.setDisabled(False)
            #self.button_prev.setDisabled(False)
            print("Autorun Off")


    def autorun(self):
        print("Autorun")
        #for i in range(10):
        #    print("Step " + str(i))
        #    time.sleep(2)


    def setState(self, state):
        self.state = state
        print("Set State: " + str(state))
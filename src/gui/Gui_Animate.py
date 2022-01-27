import functools
import re
import sys
import time
import xml.etree.ElementTree as ET
from data import iText
from enum import Enum
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea, QSizePolicy, QCheckBox, QGridLayout, QFormLayout, \
    QStackedLayout, QLayout, QSlider
from PyQt5.QtGui import QFont, QColor, QTextFormat, QRegExpValidator, QIntValidator, QCursor, QPalette
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup, QEvent, pyqtProperty, QVariantAnimation, QAbstractAnimation


class STATE(Enum):
    INIT = 0
    INIT_FORWARD = 1
    INIT_BACKWARD = 2
    F_ROTATION = 3
    F_SORT = 4
    F_ENCODE = 5
    F_INDEX_SHOW = 6
    F_INDEX_SELECT = 7
    F_INDEX_FINAL = 8
    F_END = 9

class DESC(Enum):
    forward_rotation = "forward_rotation"
    forward_sort = "forward_sort"
    forward_encode = "forward_encode"
    forward_index = "forward_index"
    forward_end = "forward_end"


class CustomLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)

class Gui_Test(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)

        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']
        self.textTableLast = []

        self.table = []
        self.table_y = []
        self.tableSort = []
        self.tableEncode = []
        self.tableIndex = []
        self.tableFinalIndex = []
        self.resultLabel = {'encode': None, 'index': None}
        self.descriptions = {}
        self.description = None
        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']

        self.tableLast = []
        self.textTable = None
        self.sortedTextTable = []
        self.sortRef = {}
        self.encodeTable = []
        self.step = 0
        self.speedFactor = 1
        self.state = STATE.F_ROTATION
        self.initUI()

    def resetWindow(self):
        childs = self.mainFrameWidget.children()
        print(str(childs))
        for child in childs:
            child.deleteLater()

    def initWindow(self):
        self.screen_resolution = self.screen().geometry()
        self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
        print (str(self.screen_width) + ", " + str(self.screen_height))
        self.window_width = self.screen_width
        #self.window_width = round(self.screen_width * 0.7)
        self.window_height = self.screen_height
        #self.window_height = round(self.screen_height * 0.6)
        self.menu_bar_offset = self.menuBar().geometry().height()


    def initControlPanel(self):
        self.controlPanel = QWidget(self)
        self.control_panel_width = self.window_width
        self.control_panel_height = round(self.window_height * 0.1)
        self.control_panel_y_offset = self.menu_bar_offset + self.control_panel_height

        self.y_offset = 0 + self.menu_bar_offset

        self.y_start = 0 + self.menu_bar_offset
        x_start = round(self.window_width / 50)  # space to left window edge (1920/50 ~ 40)

        self.button_width = 100
        self.button_height = 30
        self.button_margin = round(self.screen_width / 120)
        self.button_margin_bottom = self.button_height + round(self.screen_width / 120)

        self.input_field_label = QLabel(self)
        self.input_field_label.setText("Eingabewort:")
        self.input_field_label.move(x_start, self.y_start)
        self.input_field_label.setParent(self.mainFrameWidget)
        self.input_field_label.show()
        input_field_label_length = self.input_field_label.geometry().width()

        self.input_field = QLineEdit(self)
        self.input_field_width = self.input_field.geometry().width()
        input_field_x_start = input_field_label_length + (self.button_margin*2)
        self.input_field.move(input_field_x_start, self.y_start)
        input_text_regex = QRegExp(".{2,15}")
        input_text_validator = QRegExpValidator(input_text_regex)
        self.input_field.setValidator(input_text_validator)
        self.input_field.setPlaceholderText("Input")
        self.input_field.setText("Wikipedia!")
        self.input_field.setParent(self.mainFrameWidget)
        self.input_field.show()

        self.transform_button_x_start = self.input_field_width + (self.button_width) + (self.button_margin*4)
        self.transform_button = QPushButton(self)
        self.transform_button.setText("Transformiere")
        self.transform_button.move(self.transform_button_x_start, self.y_start)
        self.transform_button.clicked.connect(self.initForward)
        self.transform_button.setParent(self.mainFrameWidget)

        self.next_button = QPushButton(self)
        self.next_button.setText("Next")
        self.next_button.setEnabled(False)
        next_button_x_start = x_start + (self.button_width*3) + (self.button_margin*3)
        self.next_button.move(next_button_x_start, self.y_start)
        self.next_button.clicked.connect(self.nextStep)
        self.next_button.setParent(self.mainFrameWidget)

        self.prev_button = QPushButton(self)
        self.prev_button.setText("Prev")
        self.prev_button.setEnabled(False)
        prev_x_start = x_start + (self.button_width*4) + (self.button_margin*4)
        self.prev_button.move(prev_x_start, self.y_start)
        self.prev_button.clicked.connect(self.stepBack)
        self.prev_button.setParent(self.mainFrameWidget)

        self.reset_button = QPushButton(self)
        self.reset_button.setText("Reset")
        self.reset_button.setEnabled(True)
        reset_x_start = x_start + (self.button_width*5) + (self.button_margin*5)
        self.reset_button.move(reset_x_start, self.y_start)
        self.reset_button.clicked.connect(self.resetWindow)
        self.reset_button.setParent(self.mainFrameWidget)

        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(14)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setValue(7)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        slider_x_start = x_start + (self.button_width*6) + (self.button_margin*6)
        slider_y_start = self.y_offset
        slider_width = round(self.screen_width / (self.screen_width/200))
        self.speed_slider.setGeometry(QRect(slider_x_start, slider_y_start, slider_width, self.speed_slider.geometry().height()+5))
        self.speed_slider.valueChanged.connect(self.updateSpeed)
        self.speed_slider.setParent(self.mainFrameWidget)

        self.mainFrameControlDirection = QComboBox()
        self.mainFrameControlDirection.addItems(self.directions)
        self.mainFrameControlDirection.currentTextChanged.connect(self.switchPage)
        direction_x_start = x_start + (self.button_width*6) + (self.button_margin*6)
        self.mainFrameControlDirection.move(direction_x_start, self.y_start)
        self.mainFrameControlDirection.setParent(self.mainFrameWidget)

        self.setCentralWidget(self.mainFrameWidget)

    def switchPage(self):
        currentDirectionIndex = self.mainFrameControlDirection.currentIndex()
        print("Current Dircetion Index: " + str(currentDirectionIndex))
        self.mainFrameContentStack.setCurrentIndex(currentDirectionIndex)
        if(currentDirectionIndex == STATE.INIT_BACKWARD.value):
            self.showDeltaInput(True)
        else:
            self.showDeltaInput(False)


    def loadDescriptions(self):
        tree = ET.parse("/home/eric/Dokumente/Repositories/hska/Burrow_Wheeler/src/data/Descriptions.xml")
        xml_root = tree.getroot()
        for child in xml_root:
            desc = child.text
            self.descriptions[child.tag] = desc.strip()


    def initContentLayout(self):
        self.margin_window_left = round(self.window_width * 0.025)
        self.margin_window_right = round(self.window_width * 0.025)
        self.margin_window_top = self.control_panel_y_offset
        self.margin_window_bottom = round(self.window_height * 0.05)
        self.margin_between_boxes = self.window_width * 0.025

        self.left_box_x_start = 0 + self.margin_window_left
        self.left_box_x_end = round(self.window_width * 0.3)
        self.left_box_width = self.left_box_x_end - self.left_box_x_start
        self.left_box_y_start = self.margin_window_top
        self.left_box_y_end = self.window_height - self.margin_window_bottom
        self.left_box_height = self.left_box_y_end - self.left_box_y_start
        print("L: " + str(self.left_box_x_start), "R: " + str(self.left_box_x_end), "T: " + str(self.left_box_y_start),
              "B: " + str(self.left_box_y_end), "W: " + str(self.left_box_width), "H: " + str(self.left_box_height))

        self.middle_box_x_start = self.left_box_x_end + self.margin_between_boxes
        self.middle_box_x_end = round(self.window_width * 0.6)
        self.middle_box_width = self.middle_box_x_end - self.middle_box_x_start
        self.middle_box_y_start = self.margin_window_top
        self.middle_box_y_end = self.window_height - self.margin_window_bottom
        self.middle_box_height = self.middle_box_y_end - self.middle_box_y_start
        print("L: " + str(self.middle_box_x_start), "R: " + str(self.middle_box_x_end),
              "T: " + str(self.middle_box_y_start), "B: " + str(self.middle_box_y_end),
              "W: " + str(self.middle_box_width), "H: " + str(self.middle_box_height))

        self.right_box_x_start = self.middle_box_x_end + self.margin_between_boxes
        self.right_box_x_end = round(self.window_width * 0.9)
        self.right_box_x_end_test = self.window_width - self.margin_window_right
        self.right_box_width = self.right_box_x_end - self.right_box_x_start
        self.right_box_y_start = self.margin_window_top
        self.right_box_y_end = self.window_height - self.margin_window_bottom
        self.right_box_height = self.right_box_y_end - self.right_box_y_start
        print("L: " + str(self.right_box_x_start), "R: " + str(self.right_box_x_end),
              "T: " + str(self.right_box_y_start), "B: " + str(self.right_box_y_end),
              "W: " + str(self.right_box_width), "H: " + str(self.right_box_height))




    def initUI(self):
        self.initWindow()
        self.initControlPanel()
        self.initContentLayout()
        self.loadDescriptions()

        self.labelWidth = round(self.screen_width/100)
        self.labelHeight = self.labelWidth
        self.labelMargin = round(self.screen_width / 120)

        self.labelStyle = r"background-color:red; color:white;"
        self.labelStyleCopyInit = "background-color:orange; color.white;"
        self.labelStyleMarked = r"background-color:orange; color:white;"
        self.labelStyleSelected = r"background-color:green; color:white;"
        self.indexStyleMarked = r"backgroud-color:gray; color:black;"
        self.indexStyleSelected = r"backgroud-color:green; color:white;"
        self.labelDefaultStyle = r"background-color: #eff0f1; color:black;"
        self.descriptionStyle = r"border: 1px solid black;"

        self.indexMargin = round(self.screen_width / 50)
        self.tableMargin = round(self.screen_width / 4.5)

        self.indexResultHeight = round(self.screen_width / 150)

        #Position the main window in the center of the screen
        self.main_window_x_start = round(self.screen_width/2) - round(self.window_width/2)
        self.main_window_y_start = round(self.screen_height/2) - round(self.window_height/2)

        self.setGeometry(self.main_window_x_start, self.main_window_y_start, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Test Gui")
        self.createMenu()
        self.show()

    def initForward(self):
        self.next_button.setEnabled(True)
        self.prev_button.setEnabled(True)
        self.resetTable(self.table)
        self.table = []
        self.resetTable(self.tableSort)
        self.tableSort = []
        self.resetResultDirectory()
        self.deleteLabelList(self.tableIndex)
        self.deleteLabelList(self.tableEncode)
        self.tableIndex = []
        self.tableEncode = []
        self.textTable = iText.TextTable()
        self.state = STATE.F_ROTATION
        self.index = None
        self.encode = ""
        row = []
        text = ""
        print("i x_start")
        self.input_text = self.input_field.text()
        self.textTable.addText(self.input_text)
        self._MAX_STEPS = len(self.input_text)

        self.labelWidth = round((self.left_box_width / len(self.input_text)) / 2)
        self.labelLineMargin = round(((self.left_box_height / len(self.input_text)) / 2) * self.labelHeight)
        print("Label Line Margin: ", self.labelLineMargin)

        self.labelHeight = self.labelWidth
        self.labelMargin = round(self.labelWidth * 0.75)
        self.labelLineMargin = (self.labelHeight*2)
        self.labelLineMarginDouble = (self.labelHeight*4)

        desc_start_x = self.right_box_x_start
        desc_width = self.right_box_x_end - desc_start_x
        desc_start_y = self.right_box_y_start
        desc_height = (self.right_box_height * 0.25)


        if self.description != None:
            self.description.deleteLater()

        self.description = QLabel(self)
        self.description.setAlignment(Qt.AlignTop)
        self.description.setWordWrap(True)
        self.displayInfoText(DESC.forward_rotation.value)
        self.description.setGeometry(QRect(desc_start_x, desc_start_y, desc_width, desc_height))
        self.description.setStyleSheet(self.descriptionStyle)
        self.description.setParent(self.mainFrameWidget)
        self.description.show()

        self.resultLabelMargin = self.right_box_height * 0.05


        elemCount = 0
        for ch in self.input_text:
            print(ch)
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(self.labelStyle)
            #label.setStyleSheet("background-color:red; color:white;")
            y_start = self.y_offset + self.labelHeight + self.button_margin_bottom
            y_start = self.left_box_y_start
            label.resize(self.labelWidth, self.labelHeight)
            # label.setGeometry(QRect(0, 0, self.labelWidth, self.labelheight))

            if elemCount == 0:
                #x_start = round(self.window_width/50)  # space to left window edge (1920/50 ~ 40)
                x_start = self.left_box_x_start  # space to left window edge (1920/50 ~ 40)
            else:
                x_start = x_start + self.labelWidth + self.labelMargin

            label.move(x_start, y_start)
            print(str(x_start), str(y_start))
            label.setParent(self.mainFrameWidget)
            label.show()
            #print(label.palette().window().color().name())
            # label.setGeometry(QRect(x_start, y_start, 20, 20))
            self.table_y.append(y_start)
            # print(str(ch), str(x_start), str(label.width()))
            #label.move(x_start, 50)
            row.append(label)
            elemCount = elemCount + 1

        self.step = 0
        self.table.append(row)

    def resetResultDirectory(self):
        if(self.resultLabel.get('encode') != None):
            self.resultLabel.get('encode').deleteLater()
            self.resultLabel['encode'] = None

        if(self.resultLabel.get('index') != None):
            self.resultLabel.get('index').deleteLater()
            self.resultLabel['index'] = None

    def resetTable(self, table):
        if(len(table) > 0):
            for i in range(len(table)):
                self.deleteLabelList(table[i])

    def updateSpeed(self):
        print("New Speed: " + str(self.speed_slider.value()))
        self.speedFactor = ((self.speed_slider.value()/5)**-1)
        print("New Speedfactor: " + str(self.speedFactor))

    def printTable(self, table):
        content = "["
        for label in table:
            content = content + str(label.text()) + ", "

        content = content + "]"
        print(content)

    def nextStep(self):
        if self.step < self._MAX_STEPS and self.state != STATE.F_END:
            self.step = self.step + 1
        self.printStep()
        self.printState()

        if(self.state == STATE.F_ROTATION):
            if self.step == self._MAX_STEPS:
                self.state = STATE.F_SORT
                self.step = 0
                self.displayInfoText(DESC.forward_sort.value)
            else:
                self.rotate()
                #self.setLabelStyle(self.table[self.step], self.labelStyle)
                self.textTable.printTable()

        if(self.state == STATE.F_SORT):
            self.printState()
            if self.step == self._MAX_STEPS:
                self.state = STATE.F_ENCODE
                self.step = 0
                self.displayInfoText(DESC.forward_encode.value)
            else:
                self.textTable.sortTable()
                row_index = self.textTable.getRef(self.step)
                self.selectSortedRow(row_index)

        if(self.state == STATE.F_ENCODE):
            self.printState()

            if self.step == self._MAX_STEPS:
                self.state = STATE.F_INDEX_SHOW
                self.step = 0
                self.displayInfoText(DESC.forward_index.value)
            else:
                self.selectLastChar(self.step)

        if(self.state == STATE.F_INDEX_SHOW):
            self.printState()
            for i in range(self._MAX_STEPS+1):
                if(i == self._MAX_STEPS):
                    self.state = STATE.F_INDEX_SELECT
                    self.step = 0
                else:
                    self.showIndex(i)

        if(self.state == STATE.F_INDEX_SELECT):
            self.printState()

            if(self.textTable.getSortedTextAtIndex(self.step) == self.input_text):
                self.selectIndex(self.step, "next", QColor("red"), QColor("green"))
                self.state = STATE.F_INDEX_FINAL
                self.displayInfoText(DESC.forward_end.value)
            else:
                self.selectIndex(self.step, "next", QColor("red"), QColor("blue"))

        if(self.state == STATE.F_INDEX_FINAL):
            self.printState()
            self.printStep()
            self.showFinalEncodeLabel()
            self.selectFinalIndexLabel(self.step)
            self.state = STATE.F_END

        if(self.state == STATE.F_END):
            self.printState()
            self.printStep()



    def displayInfoText(self, type):
        info = self.descriptions.get(type)
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        info = info.replace("  ", "")
        print(info)
        self.description.setText(info)

    def showFinalEncodeLabel(self):
        self.toggleButtons()
        encodeLabel = self.tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()

        encode = QLabel(self)
        encode.setText("Encode: " + self.encode)
        encode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        encode.setStyleSheet("font-weight: bold; border: 1px solid black")
        encode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        encode.setCursor(QCursor(Qt.IBeamCursor))
        encode.setParent(self.mainFrameWidget)
        encode.show()

        y_end = first_encode_elem_y + self.resultLabelMargin + first_encode_elem_height
        anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(encode, b"geometry")
        #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+50, int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        anim_group.finished.connect(self.toggleButtons)
        anim_group.start()
        self.resultLabel['encode'] = encode

    def selectFinalIndexLabel(self, row):
        self.toggleButtons()

        #encodeLabel = self.tableEncode[0]
        encodeLabel = self.resultLabel.get('encode')
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()
        print(str(first_encode_elem_x), str(first_encode_elem_y), str(first_encode_elem_height))
        anim_group = QSequentialAnimationGroup(self)

        label = self.tableIndex[row]
        label_val = label.text()[0]
        label_x_start = label.geometry().x()
        label_y_start = label.geometry().y()

        print(str(label_x_start), str(label_y_start), str(label.geometry().width()), str(label.geometry().height()))
        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, int(label.geometry().width()*1.3), int(label.geometry().height()*1.3)))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, label.geometry().width(), label.geometry().height()))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        anim_group.start()



        indexLabel = QLabel(self)
        indexLabel.setText("Index: " + str(label_val))
        #indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y+50, 0, 0))
        indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        indexLabel.setStyleSheet("font-weight: bold; border: 1px solid black")
        indexLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        indexLabel.setCursor(QCursor(Qt.IBeamCursor))
        indexLabel.setParent(self.mainFrameWidget)
        indexLabel.show()
        # self.animateLabelText(indexLabel, "", "Index: ", duration=1000)

        y_end = first_encode_elem_y + self.resultLabelMargin + first_encode_elem_height
        anim = QPropertyAnimation(indexLabel, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+100, int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        anim_group.finished.connect(self.toggleButtons)
        anim_group.start()

        #self.tableFinalIndex.append(indexLabel)
        self.resultLabel['index'] = indexLabel



    def selectIndex(self, row, direction, start_color, end_color):
        if direction == 'next':
            previous = row-1
        if direction == 'prev':
            previous = row+1
            print("Prev Select Index Step: " + str(row))


        for i in range(len(self.tableSort)):
            for label in self.tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, start_color, end_color, duration=500)
                elif(i == previous):
                    self.animateBackgroundColor(label, end_color, start_color, duration=500)




    def showIndex(self, row):
        self.toggleButtons()
        table = self.tableSort[row]
        firstLabel = table[0]
        entry_y = firstLabel.geometry().y()
        entry_x = firstLabel.geometry().x()

        indexLabel_x = entry_x - self.indexMargin
        indexLabel = QLabel(self)
        labelText = str(row+1) + ".)"
        indexLabel.setText(labelText)
        indexLabel.setGeometry(QRect(indexLabel_x, entry_y, 0, 0))
        indexLabel.setAlignment(Qt.AlignCenter)
        indexLabel.setParent(self.mainFrameWidget)
        indexLabel.show()

        anim = QPropertyAnimation(indexLabel, b"geometry", self)
#        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
#                               indexLabel.sizeHint().height()))
        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
                               self.labelHeight))
        print(str(indexLabel.geometry().x()), str(indexLabel.geometry().y()), str(indexLabel.sizeHint().width()),
              str(indexLabel.sizeHint().height()))
        speed = int(500*self.speedFactor)
        anim.setDuration(speed)
        anim.finished.connect(self.toggleButtons)
        anim.start()

        self.tableIndex.append(indexLabel)


    def selectLastChar(self, row_index):
        self.toggleButtons()
        table = self.tableSort[row_index]
        lastLabel = table[-1]

        lastChar = QLabel(self)
        lastChar.setAlignment(Qt.AlignCenter)
        #print("Set Text: " + str(lastLabel.text()))
        lastChar.setText(lastLabel.text())
        lastChar.setStyleSheet("background-color:red; color: white;")
        lastChar.resize(self.labelWidth, self.labelHeight)
        lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
        lastChar.setParent(self.mainFrameWidget)
        lastChar.show()
        print(str(lastLabel.geometry().x()), str(lastLabel.geometry().y()))

        tableIndexHalf = round(len(self.tableSort)/2)
        tableEntryHalf = self.tableSort[tableIndexHalf]
        labelHalf = tableEntryHalf[0]

        #labelHalf_y = labelHalf.geometry().y()
        labelHalf_y = round(self.right_box_height / 2)
        if(len(self.tableEncode) == 0):
            lastChar_x_end = self.right_box_x_start
        else:
            prev_last = self.tableEncode[-1]
            lastChar_x_end = self.labelWidth + self.labelMargin + prev_last.geometry().x()

        #lastChar_x_end = (self.right_box_x_start + self.labelMargin) * self.step
        #lastChar_x_end = (self.right_box_x_start + ((self.labelMargin + self.labelWidth) * self.step) + self.labelMargin)
        #lastChar_x_end = lastChar.geometry().x() + 150 + (self.step * (lastChar.geometry().width() + 5))
        print(str(lastChar_x_end), str(labelHalf_y))
        #anim_group = QSequentialAnimationGroup(self)

        anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), int(lastChar.geometry().width()*1.3),
                               int(lastChar.geometry().height()*1.3)))
        speed = int(self.speedFactor * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), self.labelWidth, self.labelHeight))
        speed = int(self.speedFactor * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"pos", self)
        anim.setEndValue(QPoint(lastChar_x_end, labelHalf_y))
        speed = int(350*self.speedFactor)
        anim.setDuration(speed)
        anim.start()

        anim_group.addAnimation(anim)
        anim_group.finished.connect(self.toggleButtons)
        anim_group.start()

        self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=5000)
        self.tableEncode.append(lastChar)
        self.encode = self.encode + lastLabel.text()


    def selectSortedRow(self, row_index):
        self.toggleButtons()
        table = self.table[row_index]
        copyTable = []
        anim_group = QSequentialAnimationGroup(self)

        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet("background-color:red; color:white;")
            labelCopy.resize(self.labelWidth, self.labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.setParent(self.mainFrameWidget)
            labelCopy.show()
            copyTable.append(labelCopy)

        y_table = self.table[self.step]
        y_start = y_table[0].geometry().y()
        # y_start = y_label.geometry().y()
        first = 1
        for label in copyTable:
            if first:
                x_start = self.middle_box_x_start
                first = 0
            else:
                x_start = x_start + self.labelWidth + self.labelMargin

            # x_start = label.geometry().x()
            # y_start = label.geometry().y()
            # x_end = x_start + self.tableMargin
            x_end = x_start + self.labelMargin
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(300*self.speedFactor)
            anim.setDuration(speed)
            anim_group.addAnimation(anim)

        anim_group.finished.connect(self.toggleButtons)
        anim_group.start()

        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)

        self.tableSort.append(copyTable)

    def rotate(self):
        copyTable = []
        self.toggleButtons()
        anim_group = QSequentialAnimationGroup(self)

        table = self.table[-1]
        for label in table:
            labelCopy = QLabel(self)
            labelCopy = CustomLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet(self.labelStyleCopyInit)
            labelCopy.resize(self.labelWidth, self.labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.setParent(self.mainFrameWidget)
            #print(labelCopy.palette().window().color().name())
            labelCopy.show()
            copyTable.append(labelCopy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copyTable:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            print("y start: " + str(y_start), "y end: " + str(y_end))
            self.table_y.append(y_end)
            # print(str(x_start), str(y_start))
            anim = QPropertyAnimation(label, b"pos")
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.setEndValue(QPoint(x_start, y_end))
            speed = int(300*self.speedFactor)
            anim.setDuration(speed)
            par_anim_group.addAnimation(anim)

        par_anim_group.start()
        print(str(par_anim_group.state()))
        last_label = copyTable[-1]
        first_pos = copyTable[0].pos()

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+100))
        anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+self.labelLineMarginDouble))
        speed = int(200*self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        for i in range(len(copyTable)-2, -1, -1):
            label = copyTable[i]
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            # y_end = y_start + 50
            x_end = copyTable[i+1].geometry().x()
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_end))
            speed = int(150*self.speedFactor)
            anim.setDuration(speed)
            anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+100))
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self.labelLineMarginDouble))
        speed = int(400*self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+50))
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self.labelLineMargin))
        speed = int(400 * self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        anim_group.finished.connect(self.toggleButtons)
        anim_group.start()

        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)

        self.tableLast = copyTable.copy()
        tableRotated = self.rotateTable(copyTable)
        self.table.append(tableRotated)

        text_rotate = iText.rotateText(self.textTable.getLastText())
        self.textTable.addText(text_rotate)

    def animateBackgroundColor(self, widget, start_color, end_color, duration=1000):
        duration = int(duration*self.speedFactor)
        anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def setLabelBackground(self, widget, color):
        widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))

    def animateLabelText(self, widget, start_text, end_text, duration=1000):
        duration = int(duration*self.speedFactor)
        anim = QVariantAnimation(widget, duration=duration, startValue=start_text, endValue=end_text, loopCount=1)
        anim.valueChanged.connect(functools.partial(self.setLabelText, widget))
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def setLabelText(self, widget, text):
        widget.setText(text)

    def setLabelStyle(self, table, style):
        for label in table:
            label.setStyleSheet(style)

    def stepBack(self):

        if self.state == STATE.F_ROTATION:
            self.printStep()

            if self.step > 0:
                tableLast = self.table[-1]
                self.deleteLabelList(self.table[-1])
                del self.table[-1]
                self.textTable.removeLastText()

            next_step = self.step - 1
            if next_step < 0:
                pass
            else:
                self.step = self.step - 1

        elif self.state == STATE.F_SORT:
            self.step = self.step - 1
            if self.step >= 0:
                self.deleteLabelList(self.tableSort[-1])
                del self.tableSort[-1]

            if self.step < 0:
                self.deleteLabelList(self.tableSort[-1])
                del self.tableSort[-1]
                self.state = STATE.F_ROTATION
                self.step = self._MAX_STEPS - 1
                self.displayInfoText(DESC.forward_rotation.value)

        elif self.state == STATE.F_ENCODE:
            self.step = self.step - 1
            if self.step >= 0:
                self.deleteLastLabel(self.tableEncode)
                self.encode = self.encode[0::-1]

            if self.step < 0:
                self.deleteLastLabel(self.tableEncode)
                self.state = STATE.F_SORT
                self.step = self._MAX_STEPS - 1
                self.displayInfoText(DESC.forward_sort.value)

        elif self.state == STATE.F_INDEX_SHOW:
            for i in range(self._MAX_STEPS):
                self.step = self.step - 1
                print(str(i))
                if self.step >= 0:
                    self.deleteLastLabel(self.tableIndex)

                if self.step < 0:
                    self.deleteLastLabel(self.tableIndex)
                    self.state = STATE.F_ENCODE
                    self.step = self._MAX_STEPS - 1
                    self.displayInfoText(DESC.forward_encode.value)

        elif self.state == STATE.F_INDEX_SELECT:
            self.step = self.step - 1
            if self.step >= 0:
                self.selectIndex(self.step, "prev", QColor("red"), QColor("blue"))

            if self.step < 0:
                self.selectIndex(self.step, "prev", QColor("red"), QColor("blue"))
                self.state = STATE.F_INDEX_SHOW
                self.step = self._MAX_STEPS - 1

        elif self.state == STATE.F_END:
            self.step = self.step - 1
            self.selectIndex(self.step, "prev", QColor("red"), QColor("blue"))
            self.state = STATE.F_INDEX_SELECT
            self.deleteResultLabel()
            self.displayInfoText(DESC.forward_index.value)


    def toggleButtons(self):
        self.toggleButton(self.next_button)
        self.toggleButton(self.prev_button)
        self.toggleButton(self.transform_button)

    def toggleButton(self, button):
        if button.isEnabled():
            button.setEnabled(False)
        else:
            button.setEnabled(True)


    def deleteResultLabel(self):
        self.resultLabel['encode'].deleteLater()
        del self.resultLabel['encode']
        self.resultLabel['index'].deleteLater()
        del self.resultLabel['index']

    def deleteLastLabel(self, table):
        table[-1].deleteLater()
        del table[-1]

    def deleteLabelList(self, list):
        for label in list:
            label.deleteLater()

    def printLabelTable(self, table):
        content = "["
        for label in table:
            content = content + str(label.text()) + ", "

        content = content[0::-2]
        content = content + "]"
        print(content)

    def rotateTable(self, table):
        last = table[-1]

        for i in range(len(table)-1, 0, -1):
            table[i] = table[i-1]

        table[0] = last
        return table

    def rotateTableBack(self, table):
        first = table[0]

        for i in range(0, len(table)-1, 1):
            table[i] = table[i+1]

        table[-1] = first
        # self.printTable(table)

    def createMenu(self):
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)



        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)

    def printState(self):
        print("State: " + str(self.state))

    def printStep(self):
        print("Step: " + str(self.step))


    def switchAlgo(self):
        pass

app = QApplication(sys.argv)
window = Gui_Test()
sys.exit(app.exec())

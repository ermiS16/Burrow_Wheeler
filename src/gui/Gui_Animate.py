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
        self.resultLabel = {'encode':None, 'index':None}

        self.index = None
        self.encode = ""

        self.tableLast = []
        self.textTable = iText.TextTable()
        self.sortedTextTable = []
        self.sortRef = {}
        self.encodeTable = []
        self.step = 0
        self.speedFactor = 1
        self.state = STATE.F_ROTATION
        self.initUI()


    def initUI(self):


        self.screen_resolution = self.screen().geometry()
        self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
        print (str(self.screen_width) + ", " + str(self.screen_height))
        self.window_width = round(self.screen_width * 0.7)
        self.window_height = round(self.screen_height * 0.6)

        self.labelWidth = round(self.screen_width/100)
        self.labelheight = self.labelWidth
        self.labelMargin = round(self.screen_width / 120)

        self.labelStyle = r"background-color:red; color:white;"
        self.labelStyleCopyInit = "background-color:orange; color.white;"
        self.labelStyleMarked = r"background-color:orange; color:white;"
        self.labelStyleSelected = r"background-color:green; color:white;"
        self.indexStyleMarked = r"backgroud-color:gray; color:black;"
        self.indexStyleSelected = r"backgroud-color:green; color:white;"
        self.labelDefaultStyle = r"background-color: #eff0f1; color:black;"

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

        self.menu_bar_offset = self.menuBar().geometry().height()
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
        next_button_x_start = x_start + (self.button_width*3) + (self.button_margin*3)
        self.next_button.move(next_button_x_start, self.y_start)
        self.next_button.clicked.connect(self.nextStep)
        self.next_button.setParent(self.mainFrameWidget)

        self.prev_button = QPushButton(self)
        self.prev_button.setText("Prev")
        prev_x_start = x_start + (self.button_width*4) + (self.button_margin*4)
        self.prev_button.move(prev_x_start, self.y_start)
        self.prev_button.clicked.connect(self.stepBack)
        self.prev_button.setParent(self.mainFrameWidget)

        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(14)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setValue(7)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        slider_x_start = x_start + (self.button_width*5) + (self.button_margin*5)
        slider_y_start = self.y_offset
        slider_width = round(self.screen_width / (self.screen_width/200))
        self.speed_slider.setGeometry(QRect(slider_x_start, slider_y_start, slider_width, self.speed_slider.geometry().height()+5))
        self.speed_slider.valueChanged.connect(self.updateSpeed)
        self.speed_slider.setParent(self.mainFrameWidget)


        button_height = self.next_button.geometry().height()

        # row = []
        # text = ""
        # print("i x_start")
        # self.input_text = "Wikipedia!"
        # self.textTable.addText(self.input_text)
        # self._MAX_STEPS = len(self.input_text)
        # elemCount = 0
        # for ch in self.input_text:
        #     label = QLabel(self)
        #     label.setAlignment(Qt.AlignCenter)
        #     label.setText(str(ch))
        #     text = text + str(ch)
        #     label.setStyleSheet(self.labelStyle)
        #     #label.setStyleSheet("background-color:red; color:white;")
        #     y_start = y_offset + self.labelheight + self.button_margin_bottom
        #     label.resize(self.labelWidth, self.labelheight)
        #     # label.setGeometry(QRect(0, 0, self.labelWidth, self.labelheight))
        #
        #     if elemCount == 0:
        #         x_start = round(self.window_width/50)  # space to left window edge (1920/50 ~ 40)
        #     else:
        #         x_start = x_start + self.labelWidth + self.labelMargin
        #
        #     label.move(x_start, y_start)
        #     label.setParent(self.mainFrameWidget)
        #     #print(label.palette().window().color().name())
        #     # label.setGeometry(QRect(x_start, y_start, 20, 20))
        #     self.table_y.append(y_start)
        #     # print(str(ch), str(x_start), str(label.width()))
        #     #label.move(x_start, 50)
        #     row.append(label)
        #     elemCount = elemCount + 1
        #
        # self.table.append(row)


        self.setCentralWidget(self.mainFrameWidget)
        self.show()

    def initForward(self):
        print(str(len(self.table)))
        print(self.table)
        if(len(self.table) > 0):
            for i in range(len(self.table)):
                print(str(i))
                #print(self.table[i])
                self.deleteLabelList(self.table[i])

            for entry in self.table:
                del entry

            self.table = []

        row = []
        text = ""
        print("i x_start")
        self.input_text = self.input_field.text()
        self.textTable.addText(self.input_text)
        self._MAX_STEPS = len(self.input_text)
        elemCount = 0
        for ch in self.input_text:
            print(ch)
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(self.labelStyle)
            #label.setStyleSheet("background-color:red; color:white;")
            y_start = self.y_offset + self.labelheight + self.button_margin_bottom
            label.resize(self.labelWidth, self.labelheight)
            # label.setGeometry(QRect(0, 0, self.labelWidth, self.labelheight))

            if elemCount == 0:
                x_start = round(self.window_width/50)  # space to left window edge (1920/50 ~ 40)
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

        self.table.append(row)


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
            else:
                self.rotate()
                #self.setLabelStyle(self.table[self.step], self.labelStyle)
                self.textTable.printTable()

        if(self.state == STATE.F_SORT):
            self.printState()
            if self.step == self._MAX_STEPS:
                self.state = STATE.F_ENCODE
                self.step = 0
            else:
                self.textTable.sortTable()
                row_index = self.textTable.getRef(self.step)
                self.selectSortedRow(row_index)

        if(self.state == STATE.F_ENCODE):
            self.printState()

            if self.step == self._MAX_STEPS:
                self.state = STATE.F_INDEX_SHOW
                self.step = 0
            else:
                self.selectLastChar(self.step)

        if(self.state == STATE.F_INDEX_SHOW):
            self.printState()

            if(self.step == self._MAX_STEPS):
                self.state = STATE.F_INDEX_SELECT
                self.step = 0
            else:
                self.showIndex(self.step)

        if(self.state == STATE.F_INDEX_SELECT):
            self.printState()

            if(self.textTable.getSortedTextAtIndex(self.step) == self.input_text):
                self.selectIndex(self.step, "next", QColor("red"), QColor("green"))
                self.state = STATE.F_INDEX_FINAL
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

    def showFinalEncodeLabel(self):

        encodeLabel = self.tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()

        encode = QLabel(self)
        encode.setText("Encode: " + self.encode)
        encode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y+25, 0, 0))
        encode.setStyleSheet("font-weight: bold; border: 1px solid black")
        encode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        encode.setCursor(QCursor(Qt.IBeamCursor))
        encode.setParent(self.mainFrameWidget)
        encode.show()

        anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(encode, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+50, int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        anim_group.start()
        self.resultLabel['encode'] = encode


    def selectFinalIndexLabel(self, row):
        encodeLabel = self.tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()

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
        indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y+50, 0, 0))
        indexLabel.setStyleSheet("font-weight: bold; border: 1px solid black")
        indexLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        indexLabel.setCursor(QCursor(Qt.IBeamCursor))
        indexLabel.setParent(self.mainFrameWidget)
        indexLabel.show()
        # self.animateLabelText(indexLabel, "", "Index: ", duration=1000)

        anim = QPropertyAnimation(indexLabel, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+100, int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        speed = int(self.speedFactor*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
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
        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
                               indexLabel.sizeHint().height()))
        print(str(indexLabel.geometry().x()), str(indexLabel.geometry().y()), str(indexLabel.sizeHint().width()),
              str(indexLabel.sizeHint().height()))
        speed = int(500*self.speedFactor)
        anim.setDuration(speed)
        anim.start()

        self.tableIndex.append(indexLabel)


    def selectLastChar(self, row_index):
        table = self.tableSort[row_index]
        lastLabel = table[-1]

        lastChar = QLabel(self)
        lastChar.setAlignment(Qt.AlignCenter)
        #print("Set Text: " + str(lastLabel.text()))
        lastChar.setText(lastLabel.text())
        lastChar.setStyleSheet("background-color:red; color: white;")
        lastChar.resize(self.labelWidth, self.labelheight)
        lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
        lastChar.setParent(self.mainFrameWidget)
        lastChar.show()
        print(str(lastLabel.geometry().x()), str(lastLabel.geometry().y()))

        tableIndexHalf = round(len(self.tableSort)/2)
        tableEntryHalf = self.tableSort[tableIndexHalf]
        labelHalf = tableEntryHalf[0]

        labelHalf_y = labelHalf.geometry().y()
        lastChar_x_end = lastChar.geometry().x() + 150 + (self.step * (lastChar.geometry().width() + 5))
        print(str(lastChar_x_end), str(labelHalf_y))
        #anim_group = QSequentialAnimationGroup(self)

        anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), (lastChar.geometry().width()*1.3), (lastChar.geometry().height()*1.3)))
        speed = int(self.speedFactor * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), self.labelWidth, self.labelheight))
        speed = int(self.speedFactor * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"pos", self)
        anim.setEndValue(QPoint(lastChar_x_end, labelHalf_y))
        speed = int(350*self.speedFactor)
        anim.setDuration(speed)
        anim.start()

        anim_group.addAnimation(anim)
        anim_group.start()

        self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=5000)
        self.tableEncode.append(lastChar)
        self.encode = self.encode + lastLabel.text()


    def selectSortedRow(self, row_index):
        table = self.table[row_index]
        copyTable = []
        anim_group = QSequentialAnimationGroup(self)

        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet("background-color:red; color:white;")
            labelCopy.resize(self.labelWidth, self.labelheight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.setParent(self.mainFrameWidget)
            labelCopy.show()
            copyTable.append(labelCopy)

        y_table = self.table[self.step]
        y_start = y_table[0].geometry().y()
        # y_start = y_label.geometry().y()

        for label in copyTable:
            x_start = label.geometry().x()
            # y_start = label.geometry().y()
            x_end = x_start + self.tableMargin
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(300*self.speedFactor)
            anim.setDuration(speed)
            anim_group.addAnimation(anim)

        anim_group.start()

        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)

        self.tableSort.append(copyTable)

    def rotate(self):
        copyTable = []
        anim_group = QSequentialAnimationGroup(self)

        table = self.table[-1]
        for label in table:
            labelCopy = QLabel(self)
            labelCopy = CustomLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet(self.labelStyleCopyInit)
            labelCopy.resize(self.labelWidth, self.labelheight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.setParent(self.mainFrameWidget)
            #print(labelCopy.palette().window().color().name())
            labelCopy.show()
            copyTable.append(labelCopy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copyTable:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + 50
            self.table_y.append(y_end)
            # print(str(x_start), str(y_start))
            anim = QPropertyAnimation(label, b"pos")
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.setEndValue(QPoint(x_start, y_end))
            speed = int(300*self.speedFactor)
            anim.setDuration(speed)
            par_anim_group.addAnimation(anim)

        par_anim_group.start()

        last_label = copyTable[-1]
        first_pos = copyTable[0].pos()

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+100))
        speed = int(200*self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        for i in range(len(copyTable)-2, -1, -1):
            label = copyTable[i]
            y_start = label.geometry().y()
            y_end = y_start + 50
            x_end = copyTable[i+1].geometry().x()
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_end))
            speed = int(150*self.speedFactor)
            anim.setDuration(speed)
            anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+100))
        speed = int(400*self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+50))
        speed = int(400 * self.speedFactor)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
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

        elif self.state == STATE.F_ENCODE:
            self.step = self.step - 1
            if self.step >= 0:
                self.deleteLastLabel(self.tableEncode)
                self.encode = self.encode[0::-1]

            if self.step < 0:
                self.deleteLastLabel(self.tableEncode)
                self.state = STATE.F_SORT
                self.step = self._MAX_STEPS - 1

        elif self.state == STATE.F_INDEX_SHOW:
            self.step = self.step - 1
            if self.step >= 0:
                self.deleteLastLabel(self.tableIndex)

            if self.step < 0:
                self.deleteLastLabel(self.tableIndex)
                self.state = STATE.F_ENCODE
                self.step = self._MAX_STEPS - 1

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

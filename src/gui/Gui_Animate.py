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
    F_END = 8


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

        self.index = None

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
        self.window_width = round(self.screen_width * 0.6)
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

        self.indexMargin = round(self.screen_width / 50)
        self.tableMargin = round(self.screen_width / 4.5)

        #Position the main window in the center of the screen
        self.main_window_x_start = round(self.screen_width/2) - round(self.window_width/2)
        self.main_window_y_start = round(self.screen_height/2) - round(self.window_height/2)

        self.setGeometry(self.main_window_x_start, self.main_window_y_start, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Test Gui")
        self.createMenu()

        self.menu_bar_offset = self.menuBar().geometry().height()
        y_offset = 0 + self.menu_bar_offset

        y_start = 0 + self.menu_bar_offset
        x_start = round(self.window_width / 50)  # space to left window edge (1920/50 ~ 40)

        self.button_width = 100
        self.button_height = 30
        self.button_margin = round(self.screen_width / 120)
        self.button_margin_bottom = self.button_height + round(self.screen_width / 120)

        self.next_button = QPushButton(self)
        self.next_button.setText("Next")
        self.next_button.move(x_start, y_start)
        self.next_button.clicked.connect(self.nextStep)
        self.next_button.setParent(self.mainFrameWidget)

        self.prev_button = QPushButton(self)
        self.prev_button.setText("Prev")
        prev_x_start = x_start + self.button_width + self.button_margin
        self.prev_button.move(prev_x_start, y_start)
        self.prev_button.clicked.connect(self.stepBack)
        self.prev_button.setParent(self.mainFrameWidget)

        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(14)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setValue(7)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        slider_x_start = x_start + (self.button_width*2) + (self.button_margin*2)
        slider_y_start = y_offset
        slider_width = round(self.screen_width / (self.screen_width/200))
        self.speed_slider.setGeometry(QRect(slider_x_start, slider_y_start, slider_width, self.speed_slider.geometry().height()+5))
        self.speed_slider.valueChanged.connect(self.updateSpeed)
        self.speed_slider.setParent(self.mainFrameWidget)


        button_height = self.next_button.geometry().height()

        row = []
        text = ""
        print("i x_start")
        self.input_text = "Wikipedia!"
        self.textTable.addText(self.input_text)
        self._MAX_STEPS = len(self.input_text)
        elemCount = 0
        for ch in self.input_text:
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(self.labelStyle)
            #label.setStyleSheet("background-color:red; color:white;")
            y_start = y_offset + self.labelheight + self.button_margin_bottom
            label.resize(self.labelWidth, self.labelheight)
            # label.setGeometry(QRect(0, 0, self.labelWidth, self.labelheight))

            if elemCount == 0:
                x_start = round(self.window_width/50)  # space to left window edge (1920/50 ~ 40)
            else:
                x_start = x_start + self.labelWidth + self.labelMargin

            label.move(x_start, y_start)
            label.setParent(self.mainFrameWidget)
            #print(label.palette().window().color().name())
            # label.setGeometry(QRect(x_start, y_start, 20, 20))
            self.table_y.append(y_start)
            # print(str(ch), str(x_start), str(label.width()))
            #label.move(x_start, 50)
            row.append(label)
            elemCount = elemCount + 1

        self.table.append(row)


        self.setCentralWidget(self.mainFrameWidget)
        self.show()


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
        if self.step < self._MAX_STEPS:
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
                self.state = STATE.F_END

            elif not self.index == None:
                self.state = STATE.F_END

            else:
                self.selectIndex(self.step)

        if(self.state == STATE.F_END):
            pass

    def selectIndexFinal(self, row):
        pass

    def selectIndex(self, row):

        for i in range(len(self.tableSort)):
            for label in self.tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, QColor("red"), QColor("blue"), duration=100)
                else:
                    #self.setLabelStyle(label, self.labelStyle)
                    self.animateBackgroundColor(label, QColor("red"), QColor("red"), duration=100)



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
        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(), indexLabel.sizeHint().height()))
        speed = int(500*self.speedFactor)
        anim.setDuration(speed)
        anim.start()


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
        speed = int(1500*self.speedFactor)
        anim.setDuration(speed)
        anim.start()

        anim_group.addAnimation(anim)
        anim_group.start()

        self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=5000)

        self.tableEncode.append(lastChar)


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
        #     anim = QPropertyAnimation(label, b"color")
        #     anim.setEndValue(QColor(255, 0, 0))
        #     anim.setDuration(50)
        #     anim_group.addAnimation(anim)


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

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
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup


class STATE(Enum):
    INIT = 0
    INIT_FORWARD = 1
    INIT_BACKWARD = 2
    F_ROTATION = 3
    F_SORT = 4
    F_ENCODE = 5
    F_INDEX = 6
    F_END = 7

class Gui_Test(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.directions = ['Richtung Auswählen', 'Vorwärts', 'Rückwärts']
        self.textTable = []
        self.textTableLast = []

        self.table = []
        self.tableLast = []
        self.sortRef = {}
        self.step = 0
        self.speedFactor = 0.3
        self.state = STATE.F_ROTATION
        self.initUI()


    def initUI(self):
        self.screen_resolution = self.screen().geometry()
        self.screen_width, self.screen_height = self.screen_resolution.width(), self.screen_resolution.height()
        print (str(self.screen_width) + ", " + str(self.screen_height))
        self.window_width = round(self.screen_width * 0.6)
        self.window_height = round(self.screen_height * 0.5)

        self.setGeometry(10, 10, self.window_width, self.window_height)
        self.setWindowTitle("Test Gui")
        self.createMenu()
        self.menu_bar_offset = self.menuBar().geometry().height()
        x_start = 0
        y_offset = 0 + self.menu_bar_offset

        self.next_button = QPushButton(self)
        self.next_button.setText("Next")
        self.next_button.move(x_start, y_offset)
        self.next_button.clicked.connect(self.nextStep)


        prev_button = QPushButton(self)
        prev_button.setText("Prev")
        prev_x_start = self.next_button.geometry().width() + 5
        prev_button.move(prev_x_start, y_offset)
        prev_button.clicked.connect(self.stepBack)

        print_button = QPushButton(self)
        print_button.setText("Print")
        print_y_start = y_offset
        print_x_start = (self.next_button.geometry().width()*2) + 10
        print_button.move(print_x_start, y_offset)
        print_button.clicked.connect(self.printTable)

        button_margin_bottom = self.next_button.geometry().height() + 5
        button_height = self.next_button.geometry().height()

        row = []
        text = ""
        print("i x_start")
        input = "Wikipedia!"
        self._MAX_STEPS = len(input)
        elemCount = 0
        for ch in input:
            label = QLabel(self)
            label.setText(str(ch))
            text = text + str(ch)
            self.textTable.append(text)
            label.setStyleSheet("background-color:red; color:white;")
            y_start = y_offset + label.geometry().height() + button_margin_bottom
            label.setGeometry(QRect(0, 0, 20, 20))

            if elemCount == 0:
                x_start = 0
            else:
                x_start = x_start + label.geometry().width() + 5

            label.setGeometry(QRect(x_start, y_start, 20, 20))
            # print(str(ch), str(x_start), str(label.width()))
            #label.move(x_start, 50)
            row.append(label)
            elemCount = elemCount + 1

        self.table.append(row)
        self.show()

    def printTable(self, table):
        content = "["
        for label in table:
            content = content + str(label.text()) + ", "

        content = content + "]"
        print(content)

    def nextStep(self):
        self.step = self.step + 1
        self.printStep()
        self.printState()

        if(self.state == STATE.F_ROTATION):
            if self.step == self._MAX_STEPS:
                self.state = STATE.F_SORT
                self.step = 0
            else:
                self.rotate()

        if(self.state == STATE.F_SORT):
            self.printState()

    def printState(self):
        print("State: " + str(self.state))

    def printStep(self):
        print("Step: " + str(self.step))

    def rotate(self):

        copyTable = []
        anim_group = QSequentialAnimationGroup(self)

        table = self.table[-1]
        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet("background-color:red; color:white;")
            labelCopy.resize(label.geometry().width(), label.geometry().height())
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.show()
            copyTable.append(labelCopy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copyTable:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + 50
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

        self.tableLast = copyTable.copy()
        tableRotated = self.rotateTable(copyTable)
        self.table.append(tableRotated)


    def stepBack(self):
        self.step = self.step - 1
        if self.state == STATE.F_ROTATION:
            if self.step >= 0:
                tableLast = self.table[-1]

                for label in tableLast:
                    print(label.text())
                    label.deleteLater()

                del self.table[-1]

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
        height = self.menuBar().geometry().height()
        print("Menu Bar Height: " + str(height))

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)


app = QApplication(sys.argv)
window = Gui_Test()
sys.exit(app.exec())

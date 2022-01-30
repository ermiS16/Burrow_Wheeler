import functools
import re
import sys
import time
import xml.etree.ElementTree as ET
from data.iText import TextTable
from data import iText
from data.Description import DESC, Description
from gui.Speed import Speed
from gui import Utils
import styles.Style as sty
from styles.Style import Style
from gui.CustomLabel import CustomLabel

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


class Forward(QWidget):
    def __init__(self, arg1, input):
        super().__init__(arg1)
        self._speedFactor = Speed()
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._utils_table = Utils.Table()
        self._utils_btn = Utils.Button()
        self._utils_label = Utils.Label()
        self._table = []
        self._tableSort = []
        self._tableIndex = []
        self._tableEncode = []
        self._resultLabel = {}
        self._textTable = TextTable()
        self._description = None
        #print(input)
        self._input_text = input
        self._encode = ""
        self._index = None
        self._anim = 0
        #self.update()

    def updateSpeed(self, factor):
        self._speedFactor.update(factor)

    def setStart(self, x, y):
        self._x = x
        self._y = y
        self.setGeometry(x, y, self.geometry().width(), self.geometry().height())
        #self.update()

    def setInput(self, input):
        self._input_text = input

    def setWidth(self, width):
        self.setGeometry(self.geometry().x(), self.geometry().y(), width, self.geometry().height())
        self._width = width
        #self.update()

    def setHeight(self, height):
        self.setGeometry(self.geometry().x(), self.geometry().y(), self.geometry().width(), height)
        self._height = height

    def update(self):
        self.initLayout()
        self.initForward()

    def sortTextTable(self):
        self._textTable.sortTable()

    def getTextTableRef(self, index):
        return self._textTable.getRef(index)

    def getSortedTextAtIndex(self, index):
        return self._textTable.getSortedTextAtIndex(index)

    def removeLastText(self):
        self._textTable.removeLastText()

    def getInpuText(self):
        return self._input_text

    def getTable(self):
        return self._table

    def appendTable(self, elem):
        self._table.append(elem)

    def appendSortedTable(self, elem):
        self._tableSort.append(elem)

    def appendIndexTable(self, elem):
        self._tableIndex.append(elem)

    def appendEncodeTable(self, elem):
        self._tableEncode.append(elem)

    def getSortedTable(self):
        return self._tableSort

    def getEncodeTable(self):
        return self._tableEncode

    def getEncode(self):
        return self._encode

    def setEncode(self, encode):
        self._encode = encode

    def getIndexTable(self):
        return self._tableIndex

    def getIndex(self):
        return self._index

    def setIndex(self, index):
        self._index = index

    def getResultLabel(self):
        return self._resultLabel

    def getAnim(self):
        return self._anim

    def setAnim(self):
        print("Animation State: " + str(self.anim_group.state()))
        self._anim = self.anim_group.state()

    def reset(self):
        self._utils_table.resetTable(self._table)
        self._utils_table.resetTable(self._tableSort)
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'encode')
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'index')
        self._utils_table.deleteLabelList(self._tableIndex)
        self._utils_table.deleteLabelList(self._tableEncode)
        del self._textTable

    def initLayout(self):
        self._margin_window_left = round(self._width * 0.025)
        self._margin_window_right = round(self._width * 0.025)
        self._margin_window_top = self._y
        self._margin_window_bottom = round(self._width * 0.05)
        self._margin_between_boxes = self._width * 0.025

        self._left_box_x_start = 0 + self._margin_window_left
        self._left_box_x_end = round(self._width * 0.3)
        self._left_box_width = self._left_box_x_end - self._left_box_x_start
        self._left_box_y_start = self._margin_window_top
        self._left_box_y_end = self._height - self._margin_window_bottom
        self._left_box_height = self._left_box_y_end - self._left_box_y_start
        #print("L: " + str(self._left_box_x_start), "R: " + str(self._left_box_x_end), "T: " + str(self._left_box_y_start),
        #      "B: " + str(self._left_box_y_end), "W: " + str(self._left_box_width), "H: " + str(self._left_box_height))

        self._middle_box_x_start = self._left_box_x_end + self._margin_between_boxes
        self._middle_box_x_end = round(self._width * 0.6)
        self._middle_box_width = self._middle_box_x_end - self._middle_box_x_start
        self._middle_box_y_start = self._margin_window_top
        self._middle_box_y_end = self._height - self._margin_window_bottom
        self._middle_box_height = self._middle_box_y_end - self._middle_box_y_start
        #print("L: " + str(self._middle_box_x_start), "R: " + str(self._middle_box_x_end),
        #      "T: " + str(self._middle_box_y_start), "B: " + str(self._middle_box_y_end),
        #      "W: " + str(self._middle_box_width), "H: " + str(self._middle_box_height))

        self._right_box_x_start = self._middle_box_x_end + self._margin_between_boxes
        self._right_box_x_end = round(self._width * 0.9)
        self._right_box_width = self._right_box_x_end - self._right_box_x_start
        self._right_box_y_start = self._margin_window_top
        self._right_box_y_end = self._height - self._margin_window_bottom
        self._right_box_height = self._right_box_y_end - self._right_box_y_start
        #print("L: " + str(self._right_box_x_start), "R: " + str(self._right_box_x_end),
        #      "T: " + str(self._right_box_y_start), "B: " + str(self._right_box_y_end),
        #      "W: " + str(self._right_box_width), "H: " + str(self._right_box_height))


    def initForward(self):
        # if len(self._table) > 0:
        #     self._utils_table.resetTable(self._table)
        # if len(self._tableSort) > 0:
        #     self._utils_table.resetTable(self._tableSort)
        # if 'ecnode' in self._resultLabel:
        #     self._utils_table.deleteDirectoryEntry(self._resultLabel, 'encode')
        # if 'index' in self._resultLabel:
        #     self._utils_table.deleteDirectoryEntry(self._resultLabel, 'index')
        # if len(self._tableIndex) > 0:
        #     self._utils_table.deleteLabelList(self._tableIndex)
        # if len(self._tableEncode) > 0:
        #     self._utils_table.deleteLabelList(self._tableEncode)
        self.reset()
        self._table = []
        self._tableSort = []
        self._tableIndex = []
        self._tableEncode = []
        self._textTable = TextTable()

        self._index = None
        self._encode = ""
        row = []
        text = ""
        print(self._input_text)
        self._textTable.addText(self._input_text)

        self._labelWidth = round((self._left_box_width / len(self._input_text)) / 2)

        self._labelHeight = self._labelWidth
        self._labelMargin = round(self._labelWidth * 0.75)
        self._labelLineMargin = (self._labelHeight * 2)
        self._labelLineMarginDouble = (self._labelHeight * 4)

        desc_start_x = self._right_box_x_start
        desc_width = self._right_box_x_end - desc_start_x
        desc_start_y = self._right_box_y_start
        desc_height = (self._right_box_height * 0.25)

        if self._description != None:
            self._description.deleteLater()

        self._description = Description(self)
        self._description.setAlignment(Qt.AlignTop)
        self._description.setWordWrap(True)
        self._description.setDescription(DESC.forward_rotation)
        self._description.setGeometry(QRect(desc_start_x, desc_start_y, desc_width, desc_height))
        self._description.setStyleSheet(sty.getStyle(Style.descriptionStyle))
        #self._description.setParent(self)

        self._resultLabelMargin = self._right_box_height * 0.05

        self._labelWidth = round(self._width/100)
        self._labelHeight = self._labelWidth
        self._labelMargin = round(self._width / 120)


        self._indexMargin = round(self._width / 50)
        self._tableMargin = round(self._width / 4.5)

        self._indexResultHeight = round(self._width / 150)

        self._labelLineMargin = (self._labelHeight * 2)
        self._labelLineMarginDouble = (self._labelHeight * 4)

        elemCount = 0
        for ch in self._input_text:
            #print(ch)
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(sty.getStyle(Style.labelStyle))
            y_start = self._left_box_y_start
            #print(y_start)
            label.resize(self._labelWidth, self._labelHeight)

            if elemCount == 0:
                x_start = self._left_box_x_start
            else:
                x_start = x_start + self._labelWidth + self._labelMargin

            #print(str(x_start), str(y_start))
            label.move(x_start, y_start)
            #label.show()
            row.append(label)
            elemCount = elemCount + 1

        #self.appendTable(row)
        self._table.append(row)

    def setDescription(self, info):
        self._description.setDescription(info)

    def showFinalEncodeLabel(self):
        #self.utils_btn.toggleButtons(self.controlBtnList)
        #self.toggleButtons()
        encodeLabel = self._tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()

        encode = QLabel(self)
        encode.setText("Encode: " + self._encode)
        encode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        encode.setStyleSheet("font-weight: bold; border: 1px solid black")
        encode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        encode.setCursor(QCursor(Qt.IBeamCursor))
        #encode.setParent(self.mainFrameWidget)
        encode.show()

        y_end = first_encode_elem_y + self._resultLabelMargin + first_encode_elem_height
        anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(encode, b"geometry")
        #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+50, int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        #anim_group.finished.connect(self.toggleButtons)
        #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        anim_group.start()
        self._resultLabel['encode'] = encode

    def selectFinalIndexLabel(self, row):
        #self.toggleButtons()
        #self.utils_btn.toggleButtons(self.controlBtnList)
        #encodeLabel = self.tableEncode[0]
        encodeLabel = self._resultLabel.get('encode')
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()
        #print(str(first_encode_elem_x), str(first_encode_elem_y), str(first_encode_elem_height))
        anim_group = QSequentialAnimationGroup(self)

        label = self._tableIndex[row]
        label_val = label.text()[0]
        label_x_start = label.geometry().x()
        label_y_start = label.geometry().y()

        #print(str(label_x_start), str(label_y_start), str(label.geometry().width()), str(label.geometry().height()))
        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, int(label.geometry().width()*1.3), int(label.geometry().height()*1.3)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, label.geometry().width(), label.geometry().height()))
        speed = int(self._speedFactor.getFactor()*500)
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
        #indexLabel.setParent(self.mainFrameWidget)
        indexLabel.show()
        # self.animateLabelText(indexLabel, "", "Index: ", duration=1000)

        y_end = first_encode_elem_y + self._resultLabelMargin + first_encode_elem_height
        anim = QPropertyAnimation(indexLabel, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+100, int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        anim_group.addAnimation(anim)
        #anim_group.finished.connect(self.toggleButtons)
        #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        anim_group.start()

        #self.tableFinalIndex.append(indexLabel)
        self._resultLabel['index'] = indexLabel



    def selectIndex(self, row, direction, start_color, end_color):
        if direction == 'next':
            previous = row-1
        if direction == 'prev':
            previous = row+1
            #print("Prev Select Index Step: " + str(row))


        for i in range(len(self._tableSort)):
            for label in self._tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, start_color, end_color, duration=500)
                elif(i == previous):
                    self.animateBackgroundColor(label, end_color, start_color, duration=500)




    def showIndex(self, row):
        #self.toggleButtons()
        #self.utils_btn.toggleButtons(self.controlBtnList)

        table = self._tableSort[row]
        firstLabel = table[0]
        entry_y = firstLabel.geometry().y()
        entry_x = firstLabel.geometry().x()

        indexLabel_x = entry_x - self._indexMargin
        indexLabel = QLabel(self)
        labelText = str(row+1) + ".)"
        indexLabel.setText(labelText)
        indexLabel.setGeometry(QRect(indexLabel_x, entry_y, 0, 0))
        indexLabel.setAlignment(Qt.AlignCenter)
        #indexLabel.setParent(self.mainFrameWidget)
        indexLabel.show()

        anim = QPropertyAnimation(indexLabel, b"geometry", self)
        #        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
        #                               indexLabel.sizeHint().height()))
        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
                               self._labelHeight))
        #print(str(indexLabel.geometry().x()), str(indexLabel.geometry().y()), str(indexLabel.sizeHint().width()),
        #      str(indexLabel.sizeHint().height()))
        speed = int(500*self._speedFactor.getFactor())
        anim.setDuration(speed)
        #anim.finished.connect(self.toggleButtons)
        #anim.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        anim.start()

        self.appendIndexTable(indexLabel)
        #self.tableIndex.append(indexLabel)


    def selectLastChar(self, row_index):
        #self.toggleButtons()
        #self.utils_btn.toggleButtons(self.controlBtnList)

        table = self._tableSort[row_index]
        lastLabel = table[-1]

        lastChar = QLabel(self)
        lastChar.setAlignment(Qt.AlignCenter)
        #print("Set Text: " + str(lastLabel.text()))
        lastChar.setText(lastLabel.text())
        lastChar.setStyleSheet("background-color:red; color: white;")
        lastChar.resize(self._labelWidth, self._labelHeight)
        lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
        #lastChar.setParent(self.mainFrameWidget)
        lastChar.show()
        #print(str(lastLabel.geometry().x()), str(lastLabel.geometry().y()))

        tableIndexHalf = round(len(self._tableSort)/2)
        tableEntryHalf = self._tableSort[tableIndexHalf]
        labelHalf = tableEntryHalf[0]

        #labelHalf_y = labelHalf.geometry().y()
        labelHalf_y = round(self._right_box_height / 2)
        if(len(self._tableEncode) == 0):
            lastChar_x_end = self._right_box_x_start
        else:
            prev_last = self._tableEncode[-1]
            lastChar_x_end = self._labelWidth + self._labelMargin + prev_last.geometry().x()

        #lastChar_x_end = (self.right_box_x_start + self.labelMargin) * self.step
        #lastChar_x_end = (self.right_box_x_start + ((self.labelMargin + self.labelWidth) * self.step) + self.labelMargin)
        #lastChar_x_end = lastChar.geometry().x() + 150 + (self.step * (lastChar.geometry().width() + 5))
        #print(str(lastChar_x_end), str(labelHalf_y))
        #anim_group = QSequentialAnimationGroup(self)

        anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), int(lastChar.geometry().width()*1.3),
                               int(lastChar.geometry().height()*1.3)))
        speed = int(self._speedFactor.getFactor() * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), self._labelWidth, self._labelHeight))
        speed = int(self._speedFactor.getFactor() * 50)
        anim.setDuration(speed)

        anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"pos", self)
        anim.setEndValue(QPoint(lastChar_x_end, labelHalf_y))
        speed = int(350*self._speedFactor.getFactor())
        anim.setDuration(speed)
        anim.start()

        anim_group.addAnimation(anim)
        #anim_group.finished.connect(self.toggleButtons)
        #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        anim_group.start()

        self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=5000)
        self.appendEncodeTable(lastChar)
        #self.tableEncode.append(lastChar)
        self.setEncode((self._encode + lastLabel.text()))
        #self._encode = self._encode + lastLabel.text()


    def selectSortedRow(self, row_index, step):
        #self.toggleButtons()
        #self.utils_btn.toggleButtons(self.controlBtnList)

        table = self._table[row_index]
        copyTable = []
        anim_group = QSequentialAnimationGroup(self)

        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet("background-color:red; color:white;")
            labelCopy.resize(self._labelWidth, self._labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            #labelCopy.setParent(self.mainFrameWidget)
            labelCopy.show()
            copyTable.append(labelCopy)

        y_table = self._table[step]
        y_start = y_table[0].geometry().y()
        # y_start = y_label.geometry().y()
        first = 1
        for label in copyTable:
            if first:
                x_start = self._middle_box_x_start
                first = 0
            else:
                x_start = x_start + self._labelWidth + self._labelMargin

            # x_start = label.geometry().x()
            # y_start = label.geometry().y()
            # x_end = x_start + self.tableMargin
            x_end = x_start + self._labelMargin
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(300*self._speedFactor.getFactor())
            anim.setDuration(speed)
            anim_group.addAnimation(anim)

        #anim_group.finished.connect(self.toggleButtons)
        #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        anim_group.start()

        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)

        self.appendSortedTable(copyTable)
        #self._tableSort.append(copyTable)

    def rotate(self):
        #self.toggleButtons()
        #self.toggleControlPanelBtn()
        #self.utils_btn.toggleButtons(self.controlBtnList)

        copyTable = []
        self.anim_group = QSequentialAnimationGroup(self)

        table = self._table[-1]
        #print(table)
        for label in table:
            labelCopy = QLabel(self)
            labelCopy = CustomLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            #labelCopy.setStyleSheet(self.labelStyleCopyInit)
            labelCopy.setStyleSheet(sty.getStyle(Style.labelStyleCopyInit))
            labelCopy.resize(self._labelWidth, self._labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            #labelCopy.setParent(self.mainFrameWidget)
            #print(labelCopy.palette().window().color().name())
            labelCopy.show()
            copyTable.append(labelCopy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copyTable:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            #print("y start: " + str(y_start), "y end: " + str(y_end))
            # print(str(x_start), str(y_start))
            anim = QPropertyAnimation(label, b"pos")
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.setEndValue(QPoint(x_start, y_end))
            speed = int(300*self._speedFactor.getFactor())
            anim.setDuration(speed)
            par_anim_group.addAnimation(anim)

        par_anim_group.start()
        #print(str(par_anim_group.state()))
        last_label = copyTable[-1]
        first_pos = copyTable[0].pos()

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+100))
        anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+self._labelLineMarginDouble))
        speed = int(200*self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        for i in range(len(copyTable)-2, -1, -1):
            label = copyTable[i]
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            # y_end = y_start + 50
            x_end = copyTable[i+1].geometry().x()
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_end))
            speed = int(150*self._speedFactor.getFactor())
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+100))
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self._labelLineMarginDouble))
        speed = int(400*self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+50))
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self._labelLineMargin))
        speed = int(400 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        #anim_group.finished.connect(self.toggleButtons)
        #print(self.controlBtnList)
        #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
        #anim_group.finished.connect(self.utils_btn.toggle)
        self.anim_group.stateChanged.connect(self.setAnim)
        self.anim_group.finished.connect(self.setAnim)
        self.anim_group.finished.signal

        self.anim_group.start()

        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)

        self._tableLast = copyTable.copy()
        #tableRotated = self.rotateTable(copyTable)
        tableRotated = self._utils_table.rotateTable(copyTable)
        self._table.append(tableRotated)
        #self.appendTable(tableRotated)

        text_rotate = iText.rotateText(self._textTable.getLastText())
        self._textTable.addText(text_rotate)

    def animateBackgroundColor(self, widget, start_color, end_color, duration=1000):
        duration = int(duration*self._speedFactor.getFactor())
        anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def setLabelBackground(self, widget, color):
        widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))

    def animateLabelText(self, widget, start_text, end_text, duration=1000):
        duration = int(duration*self._speedFactor.getFactor())
        anim = QVariantAnimation(widget, duration=duration, startValue=start_text, endValue=end_text, loopCount=1)
        anim.valueChanged.connect(functools.partial(self.setLabelText, widget))
        anim.start(QAbstractAnimation.DeleteWhenStopped)

    def setLabelText(self, widget, text):
        widget.setText(text)

    def setLabelStyle(self, table, style):
        for label in table:
            label.setStyleSheet(style)

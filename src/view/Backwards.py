import functools
import re

import PyQt5
from PyQt5.QtCore import Qt, QRect, QVariantAnimation, QSequentialAnimationGroup, QPropertyAnimation, QPoint
from data.Description import Description, DESC

from gui.CustomLabel import CustomLabel
from gui.Speed import Speed
from data.iText import Text
from gui.Utils import Table as util_t


from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QColor, QCursor

import styles.Style as sty
from styles.Style import Style


class Backwards(QWidget):
    def __init__(self, arg1, encode_text, index):
        super().__init__(arg1)

        self._width = 0
        self._height = 0
        self._x = 0
        self._y = 0

        self._encode = encode_text
        self._index = index
        self._table = []
        self._tableIndex = []
        self._tableSort = []
        self._tableIndexSort = []
        self._tableIndexSortCurrent = []
        self._tableDecode = []
        self._resultLabel = {}

        self._input_desc_label = {}

        self._description = None
        self._result_text = ""

        self._speedFactor = Speed()
        self._anim = 0
        self._animGroup = 0

        self.initLayout()
        self.initBackwards()


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

    def setGeo(self, rect):
        self.setGeometry(rect)
        self._x = rect.x()
        self._y = rect.y()
        self._width = rect.width()
        self._height = rect.height()
        self.update()

    def setEncode(self, encode):
        self._encode = encode

    def setIndex(self, index):
        self._index = index

    def update(self):
        self.initLayout()
        self.initBackwards()

    def sortText(self):
        self._text.sortText()

    def getTextTableRef(self, index):
        return self._text.getRef(index)

    def setResultLabel(self, key, val):
        print(key, val)
        self._resultLabel[key] = val

    def getResultLabel(self):
        return self._resultLabel

    def getAnimGroup(self):
        return self._animGroup

    def getAnim(self):
        return self._anim

    def setAnimGroupState(self):
        print("Animation Group State: " + str(self.anim_group.state()))
        self._animGroup = self.anim_group.state()

    def setAnimState(self):
        print("Animation State: " + str(self.anim.state()))
        self._anim = self.anim.state()


    def _reset(self):
        util_t.deleteLabelList(self, self._table)
        util_t.deleteLabelList(self, self._tableIndex)
        util_t.deleteLabelList(self, self._tableSort)
        util_t.deleteLabelList(self, self._tableIndexSort)
        util_t.deleteLabelList(self, self._tableIndexSortCurrent)
        util_t.deleteLabelList(self, self._tableDecode)
        util_t.deleteDirectoryEntry(self, self._input_desc_label, 'encode')
        util_t.deleteDirectoryEntry(self, self._input_desc_label, 'index')
        util_t.deleteDirectoryEntry(self, self._resultLabel, 'decode')

    def setDescription(self, info):
        self._description.setDescription(info)

    def updateSpeed(self, factor):
        self._speedFactor.update(factor)

    def initBackwards(self):
        self._reset()
        self._result_text = ""
        self._table = []
        self._tableIndex = []
        self._tableSort = []
        self._tableIndexSort = []
        self._input_desc_label = {}
        self._tableDecode = []

        self._labelWidth = round(self._width/100)

        self._labelHeight = self._labelWidth
        self._labelMargin = round(self._labelWidth * 0.75)
        self._labelLineMargin = (self._labelHeight * 2)
        self._labelLineMarginDouble = (self._labelHeight * 4)

        self._elem_margin_x = self._width * 0.005
        self._elem_margin_y = self._height * 0.04

        desc_start_x = self._right_box_x_start
        desc_width = self._right_box_x_end - desc_start_x
        desc_start_y = self._right_box_y_start
        desc_height = (self._right_box_height * 0.25)

        if self._description != None:
            self._description.deleteLater()

        self._description = Description(self)
        self._description.setAlignment(Qt.AlignTop)
        self._description.setWordWrap(True)
        #self._description.setDescription(DESC.forward_rotation)
        self._description.setGeometry(QRect(desc_start_x, desc_start_y, desc_width, desc_height))
        self._description.setStyleSheet(sty.getStyle(Style.descriptionStyle))

        x_start = self._left_box_x_start
        y_start = self._left_box_y_start

        encode_label = QLabel(self)
        encode_label.setText("Encodiertes Wort:")
        encode_label.move(x_start, y_start)
        encode_label_width = encode_label.geometry().width()
        self._input_desc_label['encode'] = encode_label

        index_label_desc = QLabel(self)
        index_label_desc.setText("Index:")
        y_start = y_start + self._labelLineMargin
        index_label_desc.move(x_start, y_start)
        self._input_desc_label['index'] = index_label_desc

        elem_count = 0
        for ch in self._encode:
            ch_label = QLabel(self)
            ch_label.setAlignment(Qt.AlignCenter)
            ch_label.setText(str(ch))
            ch_label.setStyleSheet(sty.getStyle(Style.labelStyle))
            ch_label.resize(self._labelWidth, self._labelHeight)
            if elem_count == 0:
                x_start = x_start + encode_label_width + (self._elem_margin_x*2)
            else:
                x_start = x_start + self._labelWidth + self._elem_margin_x
            y_start = self._left_box_y_start
            ch_label.move(x_start, y_start)
            self._table.append(ch_label)

            index_label = QLabel(self)
            index_label.setAlignment(Qt.AlignCenter)
            index_label.setText(str(elem_count+1))
            index_label.setStyleSheet(sty.getStyle(Style.labelDefaultStyle))
            index_label.resize(self._labelWidth, self._labelHeight)

            y_start = y_start + self._labelLineMargin
            index_label.move(x_start, y_start)

            self._tableIndex.append(index_label)

            elem_count = elem_count + 1

    def selectSort(self, index):
        print("Sort")
        label = self._table[index]
        index_label = self._tableIndex[index]
        #print(str(label.text()), str(index_label.text()))

        label_copy = QLabel(self)
        label_copy.setAlignment(Qt.AlignCenter)
        label_copy.setText(str(label.text()))
        label_copy.setStyleSheet(label.styleSheet())
        label_copy.resize(self._labelWidth, self._labelHeight)
        label_copy.move(label.geometry().x(), label.geometry().y())
        label_copy.show()

        self.setLabelTextColor(label_copy, QColor("red"))

        index_label_copy = QLabel(self)
        index_label_copy.setAlignment(Qt.AlignCenter)
        index_label_copy.setText(str(index_label.text()))
        index_label_copy.setStyleSheet(index_label.styleSheet())
        index_label_copy.resize(self._labelWidth, self._labelHeight)
        index_label_copy.move(index_label.geometry().x(), index_label.geometry().y())
        index_label_copy.show()

        current_index_label = QLabel(self)
        current_index_label.setAlignment(Qt.AlignCenter)
        current_index_label.setText(str("(" + str((len(self._tableIndexSortCurrent)+1)) + ")"))
        current_index_label.setStyleSheet(index_label.styleSheet())
        current_index_label.resize(self._labelWidth, self._labelHeight)
        current_index_label.show()


        self.anim_group = QSequentialAnimationGroup(self)
        #print(index)
        if len(self._tableSort) == 0:
            x_start = self._middle_box_x_start
            x_end = x_start + self._labelWidth + self._elem_margin_x
        else:
            x_start = self._tableSort[-1].geometry().x()
            x_end = x_start + self._labelWidth + self._elem_margin_x

        y_start = label.geometry().y()

        current_index_label.move(x_end, (label_copy.geometry().y() - self._labelLineMargin))

        anim = QPropertyAnimation(label_copy, b"geometry")
        anim.setEndValue(QRect(label_copy.geometry().x(), label_copy.geometry().y(), int(label_copy.geometry().width()*1.3), int(label_copy.geometry().height()*1.3)))
        speed = int(500 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_copy, b"geometry")
        anim.setEndValue(QRect(label_copy.geometry().x(), label_copy.geometry().y(), label_copy.geometry().width(), label_copy.geometry().height()))
        speed = int(500 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_copy, b"pos")
        anim.setEndValue(QPoint(x_end, y_start))
        speed = int(500 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        # x_start = index_label.geometry().x()
        # x_end = x_start + self._middle_box_x_start
        y_start = index_label.geometry().y()

        anim = QPropertyAnimation(index_label_copy, b"pos")
        anim.setEndValue(QPoint(x_end, y_start))
        speed = int(500 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.start()

        speed = 500
        self.animateBackgroundColor(label_copy, QColor("orange"), QColor("red"), duration=speed)

        self._tableSort.append(label_copy)
        self._tableIndexSort.append(index_label_copy)
        self._tableIndexSortCurrent.append(current_index_label)

    def selectSortedChar(self, index):
        label = self._tableSort[index]
        print(index, label.text())
        label_selected = QLabel(self)
        label_selected.setAlignment(Qt.AlignCenter)
        label_selected.setText(label.text())
        label_selected.setStyleSheet("background-color:red; color: white;")
        label_selected.resize(self._labelWidth, self._labelHeight)
        label_selected.move(label.geometry().x(), label.geometry().y())
        label_selected.show()

        y_start = round(self._right_box_height / 2)
        if(len(self._tableDecode) == 0):
            x_start = self._right_box_x_start
        else:
            prev_last = self._tableDecode[-1]
            x_start = prev_last.geometry().x() + self._labelWidth + self._elem_margin_x

        self.anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(label_selected, b"geometry", self)
        anim.setEndValue(QRect(label_selected.geometry().x(), label_selected.geometry().y(), int(label_selected.geometry().width()*1.3),
                               int(label_selected.geometry().height()*1.3)))
        speed = int(self._speedFactor.getFactor() * 250)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_selected, b"geometry", self)
        anim.setEndValue(QRect(label_selected.geometry().x(), label_selected.geometry().y(), self._labelWidth, self._labelHeight))
        speed = int(self._speedFactor.getFactor() * 250)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_selected, b"pos", self)
        anim.setEndValue(QPoint(x_start, y_start))
        speed = int(350*self._speedFactor.getFactor())
        anim.setDuration(speed)
        anim.start()

        self.anim_group.addAnimation(anim)
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()

        speed = 500
        self.animateBackgroundColor(label_selected, QColor("orange"), QColor("red"), duration=speed)
        self._tableDecode.append(label_selected)

    def showFinalDecodeLabel(self, decoded):
        encodeLabel = self._tableDecode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()

        decode = QLabel(self)
        decode.setText("Decodiert: " + decoded)
        decode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        decode.setStyleSheet("font-weight: bold; border: 1px solid black")
        decode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        decode.setCursor(QCursor(Qt.IBeamCursor))
        decode.show()

        y_end = first_encode_elem_y + self._elem_margin_y + first_encode_elem_height
        self.anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(decode, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(decode.sizeHint().width()*2), int(decode.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(lambda: self.setResultLabel('encode', decode))
        self.anim_group.start()

        self._resultLabel['decode'] = decode

    def animateBackgroundColor(self, widget, start_color, end_color, duration=1000):
        duration = int(duration*self._speedFactor.getFactor())
        self.anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        self.anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        self.anim.stateChanged.connect(self.setAnimState)
        self.anim.finished.connect(self.setAnimState)
        self.anim.start()



    def setLabelBackground(self, widget, color):
        widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))

    def setLabelTextColor(self, widget, color):
        style = widget.styleSheet()
        new = re.sub(r'; *color: \.', "", style)
        print(new)
        #widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))


    def removeResultLabel(self):
        util_t.deleteDirectoryEntry(self, self._resultLabel, 'decode')

    def removeLastDecodeLabel(self):
        util_t.deleteLastLabel(self, self._tableDecode)

    def removeLastSortLabel(self):
        util_t.deleteLastLabel(self, self._tableSort)
        util_t.deleteLastLabel(self, self._tableIndexSort)
        util_t.deleteLastLabel(self, self._tableIndexSortCurrent)


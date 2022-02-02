import functools

import PyQt5
from PyQt5.QtCore import Qt, QRect, QVariantAnimation
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
        self._text = Text(encode_text)
        self._table = []
        self._tableIndex = []
        self._tableSort = []

        self._input_desc_label = {}

        self._description = None
        self._result_text = ""

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
        util_t.deleteDirectoryEntry(self, self._input_desc_label, 'encode')
        util_t.deleteDirectoryEntry(self, self._input_desc_label, 'index')
        del self._text

    def setDescription(self, info):
        self._description.setDescription(info)

    def initBackwards(self):
        self._reset()
        self._result_text = ""
        self._text = Text(self._encode)
        self._table = []
        self._tableIndex = []
        self._tableSort = []
        self._input_desc_label = {}

        self._labelWidth = round(self._width/100)

        self._labelHeight = self._labelWidth
        self._labelMargin = round(self._labelWidth * 0.75)
        self._labelLineMargin = (self._labelHeight * 2)
        self._labelLineMarginDouble = (self._labelHeight * 4)

        self._elem_margin_x = self._width * 0.005

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
        print(str(label.text()))



    def animateBackgroundColor(self, widget, start_color, end_color, duration=1000, setAnim=False):
        duration = int(duration*self._speedFactor.getFactor())
        self.anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        self.anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        self.anim.stateChanged.connect(self.setAnimState)
        self.anim.finished.connect(self.setAnimState)
        self.anim.start()

    def setLabelBackground(self, widget, color):
        widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))

import functools

from PyQt5.QtCore import QVariantAnimation, QRect
from PyQt5.QtWidgets import QWidget
from controller.Speed import Speed
from view.Description import Description
from view.ColorSettings import Setting
import styles.Style as sty
from styles.Style import STYLE

class Content(QWidget):

    def __init__(self, arg1):
        super(Content, self).__init__()
        self._result_label = {}
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._speed_factor = 1
        self._color_setting = None
        self._description = None
        self._table_dict = {}
        self._info_label = {}
        self._anim_counter = 0

    def setDescription(self, info):
        self._description.setDescription(info)

    def updateSpeed(self, factor):
        self._speed_factor = factor

    def getSpeedFactor(self):
        return self._speed_factor

    def setColorSetting(self, setting):
        self._color_setting = setting

    def setLabelStyle(self, list):
        style = self._color_setting.get(Setting.label_style.value)
        for label in list:
            self.setStyle(label, style)

    def setStyle(self, label, style):
        label.setStyleSheet(style)

    def setGeo(self, rect):
        self.setGeometry(rect)
        self._x = rect.x()
        self._y = rect.y()
        self._width = rect.width()
        self._height = rect.height()
        self.update()

    def update(self):
        self.initLayout()
        self.initContent()

    def animCounterIncrease(self):
        self._anim_counter = self._anim_counter + 1

    def animCounterDecrease(self):
        self._anim_counter = self._anim_counter - 1

    def getAnimCounter(self):
        return self._anim_counter

    def addTable(self, key, list):
        print("Key: " + str(key), list)
        self._table_dict[key] = list

    def appendTable(self, table_name, entry):
        list = self._table_dict.get(table_name)
        table = list[0]
        table.append(entry)

    def getTable(self, table_name):
        list = self._table_dict.get(table_name)
        return list[0]

    def rotateTable(self, table):
        last = table[-1]
        for i in range(len(table) - 1, 0, -1):
            table[i] = table[i - 1]

        table[0] = last
        return table

    def getTableEntry(self, table_name, index):
        list = self._table_dict.get(table_name)
        return list[0][index]

    def getLastTableEntry(self, table_name):
        list = self._table_dict.get(table_name)
        return list[0][-1]

    def getTableLength(self, table_name):
        list = self._table_dict.get(table_name)
        return len(list[0])

    def getLabelGeometry(self, table_name, index):
        label = self.getTableEntry(table_name, index)
        return label.geometry()

    def deleteTable(self, table_name, index):
        list = self._table_dict.get(table_name)
        table = list[0]
        self.deleteLabelList(table[index])
        del table[index]

    def deleteLabel(self, table_name, index):
        list = self._table_dict.get(table_name)
        table = list[0]
        if len(table) > 0:
            table[index].deleteLater()
            del table[index]

    def deleteLastLabel(self, table_name):
        table = self.getTable(table_name)
        if len(table) > 0:
            table[-1].deleteLater()
            del table[-1]

    def deleteLabelList(self, list):
        for label in list:
            label.deleteLater()
            del label

    def resetTable(self, table):
        if(len(table) > 0):
            for i in range(len(table)):
                self.deleteLabelList(table[i])

            for list in table:
                del list

    def reset(self):
        self.deleteDict(self._info_label)
        self.deleteDict(self._result_label)
        for entry in self._table_dict:
            list = self._table_dict[entry]
            if list[1] == "label":
                self.deleteLabelList(list[0])
            if list[1] == "table":
                self.resetTable(list[0])
            list[1] = []

    def deleteDict(self, dict):
        entries = list(dict.keys())
        for entry in entries:
            self.deleteDirectoryEntry(dict, str(entry))

    def deleteDirectoryEntry(self, dir, key):
        if key in dir:
            dir[key].deleteLater()
            del dir[key]

    def setInfoLabel(self, key, val):
        print("Set Info: " + str(key))
        self._info_label[key] = val

    def infoLabelExists(self, label_name):
        return label_name in self._info_label

    def setResultLabel(self, key, val):
        self._result_label[key] = val

    def deleteResultLabel(self):
        self.deleteDict(self._result_label)

    def deleteInfoLabel(self):
        self.deleteDict(self._info_label)

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

        self._label_width = round(self._width / 100)

        self._label_height = self._label_width
        self._label_margin = round(self._label_width * 0.75)
        self._label_line_margin = (self._label_height * 2)
        self._label_line_margin_double = (self._label_height * 4)
        self._result_label_margin = self._right_box_height * 0.05

        self._elem_margin_x = self._width * 0.005
        self._elem_margin_y = self._height * 0.04

        self._index_margin = self._width * 0.03

    def initContent(self):
        pass

    def initDescription(self):
        if self._description != None:
            self._description.deleteLater()

        desc_start_x = self._right_box_x_start
        desc_width = self._right_box_x_end - desc_start_x
        desc_start_y = self._right_box_y_start
        desc_height = (self._right_box_height * 0.25)

        self._description = Description(self)
        self._description.setDescription("")
        self._description.setGeometry(QRect(desc_start_x, desc_start_y, desc_width, desc_height))
        self._description.setStyleSheet(sty.getStyle(STYLE.descriptionStyle))


    def animateLabelColor(self, widget, start_color, end_color, start_color_text, end_color_text, duration=1000):
        duration = int(duration * self.getSpeedFactor())

        self.anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        self.anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        self.anim.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim.start()

        self.anim2 = QVariantAnimation(widget, duration=duration, startValue=start_color_text, endValue=end_color_text, loopCount=1)
        self.anim2.valueChanged.connect(functools.partial(self.setLabelText, widget))
        self.anim2.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim2.start()


    def setLabelBackground(self, widget, color):
        text = widget.styleSheet().split(";")[1]
        background = r"background-color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)

    def setLabelText(self, widget, color):
        background = widget.styleSheet().split(";")[0]
        text = r"color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)

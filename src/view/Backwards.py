from enum import Enum

from PyQt5.QtCore import Qt, QRect, QSequentialAnimationGroup, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QCursor

import styles.Style as sty
from styles.Style import STYLE
from view.ColorSettings import Setting
from view.Content import Content

class TableName(Enum):
    table = "table"
    tableSort = "tableSort"
    tableIndex = "tableIndex"
    tableIndexSort = "tableIndexSort"
    tableIndexSortReal = "tableIndexSortReal"
    tableDecode = "tableDecode"

class Backwards(Content):
    def __init__(self, arg1, encode_text, index):
        super(Backwards, self).__init__(self)

        self._encode = encode_text
        self._index = index

        self.addTable(TableName.table.value, [[], "label"])
        self.addTable(TableName.tableSort.value, [[], "label"])
        self.addTable(TableName.tableIndex.value, [[], "label"])
        self.addTable(TableName.tableIndexSort.value, [[], "label"])
        self.addTable(TableName.tableIndexSortReal.value, [[], "label"])
        self.addTable(TableName.tableDecode.value, [[], "label"])


    def removeLastDecodeLabel(self):
        self.deleteLastLabel(TableName.tableDecode.value)

    def removeLastSortLabel(self):
        self.deleteLastLabel(TableName.tableSort.value)
        self.deleteLastLabel(TableName.tableIndexSort.value)
        self.deleteLastLabel(TableName.tableIndexSortReal.value)

    def updateSelectFoundColor(self, index):
        entry = self.getTableEntry(TableName.tableIndexSortReal.value, index)
        style = self._color_setting.get(Setting.label_select_found_style.value)
        self.setStyle(entry, style)

    def updateSelectColor(self, index):
        print("Index: " + str(index))
        entry = self.getTableEntry(TableName.tableIndexSortReal.value, index)
        style = self._color_setting.get(Setting.label_select_style.value)
        self.setStyle(entry, style)

    def updateLabelColor(self):
        self.setLabelStyle(self.getTable(TableName.table.value))
        self.setLabelStyle(self.getTable(TableName.tableSort.value))
        self.setLabelStyle(self.getTable(TableName.tableDecode.value))


    def initContent(self):
        self.reset()
        self.initDescription()

        x_start = self._left_box_x_start
        y_start = self._left_box_y_start

        encode_label_info = QLabel(self)
        encode_label_info.setText("Kodiertes Wort:")
        encode_label_info.setStyleSheet(sty.getStyle(STYLE.infoLabelStyle))
        encode_label_info.move(x_start, y_start)
        encode_label_width = encode_label_info.geometry().width()
        self.setInfoLabel('encode_info', encode_label_info)

        index_label_info = QLabel(self)
        index_label_info.setText("Index:")
        index_label_info.setStyleSheet(sty.getStyle(STYLE.infoLabelStyle))
        y_start = y_start + self._label_line_margin
        index_label_info.move(x_start, y_start)
        self.setInfoLabel('index_info', index_label_info)

        info_label = QLabel(self)
        info_label.setText("Dekodiertes Wort")
        info_label.setStyleSheet(sty.getStyle(STYLE.infoLabelStyle))
        x_start = self._right_box_x_start
        y_start = round(self._right_box_height / 2) - self._elem_margin_y
        print(x_start, y_start)
        info_label.move(x_start, y_start)
        self.setInfoLabel('decoded_info', info_label)

        x_start = self._left_box_x_start
        elem_count = 0
        for ch in self._encode:
            ch_label = QLabel(self)
            ch_label.setAlignment(Qt.AlignCenter)
            ch_label.setText(str(ch))
            ch_label.setStyleSheet(self._color_setting.get(Setting.label_style.value))
            ch_label.resize(self._label_width, self._label_height)
            if elem_count == 0:
                x_start = x_start + encode_label_width + (self._elem_margin_x*2)
            else:
                x_start = x_start + self._label_width + self._elem_margin_x
            y_start = self._left_box_y_start
            ch_label.move(x_start, y_start)

            self.appendTable(TableName.table.value, ch_label)

            index_label = QLabel(self)
            index_label.setAlignment(Qt.AlignCenter)
            index_label.setText(str(elem_count+1))
            index_label.resize(self._label_width, self._label_height)

            y_start = y_start + self._label_line_margin
            index_label.move(x_start, y_start)

            self.appendTable(TableName.tableIndex.value, index_label)
            elem_count = elem_count + 1

    def selectSort(self, index):
        label = self.getTableEntry(TableName.table.value, index)
        index_label = self.getTableEntry(TableName.tableIndex.value, index)


        label_copy = QLabel(self)
        label_copy.setAlignment(Qt.AlignCenter)
        label_copy.setText(str(label.text()))
        label_copy.setStyleSheet(self._color_setting.get(Setting.label_style.value))
        label_copy.resize(self._label_width, self._label_height)
        label_copy.move(label.geometry().x(), label.geometry().y())
        label_copy.show()

        index_label_copy = QLabel(self)
        index_label_copy.setAlignment(Qt.AlignCenter)
        index_label_copy.setText(str(index_label.text()))
        index_label_copy.resize(self._label_width, self._label_height)
        index_label_copy.move(index_label.geometry().x(), index_label.geometry().y())
        index_label_copy.show()

        table_index_sort_real_length = self.getTableLength(TableName.tableIndexSortReal.value)
        real_index_label = QLabel(self)
        real_index_label.setAlignment(Qt.AlignCenter)
        real_index_label.setText(str("(" + str(table_index_sort_real_length+1) + ")"))
        real_index_label.resize(self._label_width, self._label_height)
        real_index_label.show()


        self.anim_group = QSequentialAnimationGroup(self)
        table_sort_length = self.getTableLength(TableName.tableSort.value)
        if table_sort_length == 0:
            x_start = self._middle_box_x_start
            x_end = x_start + self._label_width + self._elem_margin_x
        else:
            x_start = self.getLabelGeometry(TableName.tableSort.value, -1).x()
            x_end = x_start + self._label_width + self._elem_margin_x

        y_start = label.geometry().y()
        y_end = label_copy.geometry().y() - self._label_line_margin
        real_index_label.move(x_end, y_end)

        anim = QPropertyAnimation(label_copy, b"geometry")
        anim.setEndValue(QRect(label_copy.geometry().x(), label_copy.geometry().y(), int(label_copy.geometry().width()*1.3), int(label_copy.geometry().height()*1.3)))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_copy, b"geometry")
        anim.setEndValue(QRect(label_copy.geometry().x(), label_copy.geometry().y(), label_copy.geometry().width(), label_copy.geometry().height()))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_copy, b"pos")
        anim.setEndValue(QPoint(x_end, y_start))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        y_start = index_label.geometry().y()

        anim = QPropertyAnimation(index_label_copy, b"pos")
        anim.setEndValue(QPoint(x_end, y_start))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = 500
        start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
        start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
        end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
        end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
        self.animateLabelColor(label_copy, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)

        self.appendTable(TableName.tableSort.value, label_copy)
        self.appendTable(TableName.tableIndexSort.value, index_label_copy)
        self.appendTable(TableName.tableIndexSortReal.value, real_index_label)


    def selectSortedChar(self, index):
        label = self.getTableEntry(TableName.tableSort.value, index)
        label_selected = QLabel(self)
        label_selected.setAlignment(Qt.AlignCenter)
        label_selected.setText(label.text())
        label_selected.setStyleSheet(self._color_setting.get(Setting.label_style.value))
        label_selected.resize(self._label_width, self._label_height)
        label_selected.move(label.geometry().x(), label.geometry().y())
        label_selected.show()

        y_start = round(self._right_box_height / 2)
        table_decode_length = self.getTableLength(TableName.tableDecode.value)
        if(table_decode_length == 0):
            x_start = self._right_box_x_start
        else:
            prev_last = self.getTableEntry(TableName.tableDecode.value, -1)
            x_start = prev_last.geometry().x() + self._label_width + self._elem_margin_x

        self.anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(label_selected, b"geometry", self)
        anim.setEndValue(QRect(label_selected.geometry().x(), label_selected.geometry().y(), int(label_selected.geometry().width()*1.3),
                               int(label_selected.geometry().height()*1.3)))
        speed = int(self.getSpeedFactor()*250)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_selected, b"geometry", self)
        anim.setEndValue(QRect(label_selected.geometry().x(), label_selected.geometry().y(), self._label_width, self._label_height))
        speed = int(self.getSpeedFactor()*250)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label_selected, b"pos", self)
        anim.setEndValue(QPoint(x_start, y_start))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        anim.start()

        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(500)
        start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
        start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
        end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
        end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
        self.animateLabelColor(label_selected, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)
        self.appendTable(TableName.tableDecode.value, label_selected)

    def selectNextSortedIndex(self, index, prev_index, direction):
        speed = 500
        print(index, prev_index)
        if direction == 'next':
            if index != None:
                label = self.getTableEntry(TableName.tableIndexSortReal.value, index)
                start_color = QColor(self._color_setting.get(Setting.label_default_background.value))
                end_color = QColor(self._color_setting.get(Setting.label_select_background.value))
                start_color_text = QColor(self._color_setting.get(Setting.label_default_text.value))
                end_color_text = QColor(self._color_setting.get(Setting.label_select_text.value))
                self.animateLabelColor(label, start_color, end_color, start_color_text, end_color_text, duration=speed)
                label.setStyleSheet(self._color_setting.get(Setting.label_select_style.value))

            if prev_index != None:
                label = self.getTableEntry(TableName.tableIndexSortReal.value, prev_index)
                start_color = QColor(self._color_setting.get(Setting.label_select_background.value))
                end_color = QColor(self._color_setting.get(Setting.label_select_found_background.value))
                start_color_text = QColor(self._color_setting.get(Setting.label_select_text.value))
                end_color_text = QColor(self._color_setting.get(Setting.label_select_found_text.value))
                self.animateLabelColor(label, start_color, end_color, start_color_text, end_color_text, duration=speed)
                label.setStyleSheet(self._color_setting.get(Setting.label_select_style.value))

        if direction == 'prev':
            if index != None:
                label = self.getTableEntry(TableName.tableIndexSortReal.value, index)
                start_color = QColor(self._color_setting.get(Setting.label_select_found_background.value))
                end_color = QColor(self._color_setting.get(Setting.label_select_background.value))
                start_color_text = QColor(self._color_setting.get(Setting.label_select_found_text.value))
                end_color_text = QColor(self._color_setting.get(Setting.label_select_text.value))
                self.animateLabelColor(label, start_color, end_color, start_color_text, end_color_text, duration=speed)
                label.setStyleSheet(self._color_setting.get(Setting.label_select_style.value))

            if prev_index != None:
                label = self.getTableEntry(TableName.tableIndexSortReal.value, prev_index)
                start_color = QColor(self._color_setting.get(Setting.label_select_background.value))
                end_color = QColor(self._color_setting.get(Setting.label_default_background.value))
                start_color_text = QColor(self._color_setting.get(Setting.label_select_text.value))
                end_color_text = QColor(self._color_setting.get(Setting.label_default_text.value))
                self.animateLabelColor(label, start_color, end_color, start_color_text, end_color_text, duration=speed)
                label.setStyleSheet(self._color_setting.get(Setting.label_select_style.value))

    def showFinalDecodeLabel(self, decoded):
        encode_label = self.getTableEntry(TableName.tableDecode.value, 0)
        first_encode_elem_y = encode_label.geometry().y()
        first_encode_elem_x = encode_label.geometry().x()
        first_encode_elem_height = encode_label.geometry().height()

        decode = QLabel(self)
        decode.setText("Dekodiert: " + decoded)
        decode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        decode.setStyleSheet(sty.getStyle(STYLE.resultLabelStyle))
        decode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        decode.setCursor(QCursor(Qt.IBeamCursor))
        decode.show()

        y_end = first_encode_elem_y + self._elem_margin_y + first_encode_elem_height
        self.anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(decode, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(decode.sizeHint().width()*2), int(decode.sizeHint().height()*2)))

        speed = int(self.getSpeedFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.finished.connect(lambda: self.setResultLabel('encode', decode))
        self.animCounterIncrease()
        self.anim_group.start()

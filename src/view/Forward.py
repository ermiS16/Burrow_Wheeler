from enum import Enum

from view.Content import Content
from model.Description import DESC
import styles.Style as sty
from styles.Style import Style
from view.ColorSettings import Setting
from view.CustomLabel import CustomLabel

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup

class TableName(Enum):
    table = "table"
    tableSort = "tableSort"
    tableIndex = "tableIndex"
    tableEncode = "tableEncode"
    tableSortIndex = "tableSortIndex"

class Forward(Content):
    def __init__(self, arg1, input):
        super(Forward, self).__init__(self)

        self.addTable(TableName.table.value, [[], "table"])
        self.addTable(TableName.tableSort.value, [[], "table"])
        self.addTable(TableName.tableIndex.value, [[], "label"])
        self.addTable(TableName.tableEncode.value, [[], "label"])
        self.addTable(TableName.tableSortIndex.value, [[], "table"])

        self._input_text = input


    def updateSelectColor(self, step):
        self.selectIndex(step, 'update', found=False)

    def updateSelectFoundColor(self, step):
        self.selectIndex(step, 'update', found=True)

    def updateLabelColor(self, ignore=None):
        table = self.getTable(TableName.table.value)
        for list in table:
            self.setLabelStyle(list)

        table_sort = self.getTable(TableName.tableSort.value)
        table_sort_length = self.getTableLength(TableName.tableSort.value)
        for i in range(table_sort_length):
            if i == ignore:
                pass
            else:
                self.setLabelStyle(table_sort[i])

        table_encode = self.getTable(TableName.tableEncode.value)
        self.setLabelStyle(table_encode)

    def deleteLastTable(self):
        self.deleteTable(TableName.table.value, -1)

    def deleteLastTableSorted(self):
        self.deleteTable(TableName.tableSort.value, -1)

    def deleteLastEncodeLabel(self):
        self.deleteLabel(TableName.tableEncode.value, -1)

    def deleteIndexTable(self):
        self.deleteLabel(TableName.tableIndex.value, -1)

    def initContent(self):
        self.reset()
        row = []
        text = ""
        self.initDescription(DESC.forward_rotation)

        info_label = QLabel(self)
        info_label.setText("Rotationen")
        info_label.setStyleSheet(sty.getStyle(Style.infoLabelStyle))
        x_start = self._left_box_x_start
        y_start = self._left_box_y_start - self._elem_margin_y
        print(x_start, y_start)
        info_label.move(x_start, y_start)
        self.setInfoLabel('rotation', info_label)

        info_label = QLabel(self)
        info_label.setText("Sortierte Rotationen")
        info_label.setStyleSheet(sty.getStyle(Style.infoLabelStyle))
        x_start = self._middle_box_x_start
        y_start = self._middle_box_y_start - self._elem_margin_y
        print(x_start, y_start)
        info_label.move(x_start, y_start)
        self.setInfoLabel('sorted_rotation', info_label)

        info_label = QLabel(self)
        info_label.setText("Kodiertes Wort")
        info_label.setStyleSheet(sty.getStyle(Style.infoLabelStyle))
        x_start = self._right_box_x_start
        #y_start = self._middle_box_y_start - self._elem_margin_y
        y_start = round(self._right_box_height / 2) - self._elem_margin_y
        print(x_start, y_start)
        info_label.move(x_start, y_start)
        self.setInfoLabel('encoded_input', info_label)

        elem_count = 0
        for ch in self._input_text:
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(self._color_setting.get(Setting.label_style.value))
            y_start = self._left_box_y_start
            label.resize(self._label_width, self._label_height)

            if elem_count == 0:
                x_start = self._left_box_x_start
            else:
                x_start = x_start + self._label_width + self._elem_margin_x

            label.move(x_start, y_start)
            row.append(label)
            elem_count = elem_count + 1

        self.appendTable(TableName.table.value, row)


    def showFinalEncodeLabel(self, encode_text):
        encode_label = self.getTableEntry(TableName.tableEncode.value, 0)
        first_encode_elem_y = encode_label.geometry().y()
        first_encode_elem_x = encode_label.geometry().x()
        first_encode_elem_height = encode_label.geometry().height()

        encode = QLabel(self)
        encode.setText("Kodiert: " + encode_text)
        encode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        encode.setStyleSheet(sty.getStyle(Style.resultLabelStyle))
        encode.setTextInteractionFlags(Qt.TextSelectableByMouse)
        encode.setCursor(QCursor(Qt.IBeamCursor))
        encode.show()

        y_end = first_encode_elem_y + self._elem_margin_y + first_encode_elem_height
        self.anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(encode, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))

        speed = int(self.getSpeedFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.finished.connect(lambda: self.setResultLabel('encode', encode))
        self.animCounterIncrease()
        self.anim_group.start()

    def selectFinalIndexLabel(self, row):
        encode_label = self.getTableEntry(TableName.tableEncode.value, 0)
        first_encode_elem_y = encode_label.geometry().y()
        first_encode_elem_x = encode_label.geometry().x()
        first_encode_elem_height = encode_label.geometry().height()
        self.anim_group = QSequentialAnimationGroup(self)

        label = self.getTableEntry(TableName.tableIndex.value, row)
        label_val = label.text()[0]
        label_x_start = label.geometry().x()
        label_y_start = label.geometry().y()

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, int(label.geometry().width()*1.3), int(label.geometry().height()*1.3)))
        speed = int(self.getSpeedFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, label.geometry().width(), label.geometry().height()))
        speed = int(self.getSpeedFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.animCounterIncrease()
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.start()

        index_label = QLabel(self)
        index_label.setText("Index: " + str(label_val))
        index_label.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        index_label.setStyleSheet(sty.getStyle(Style.resultLabelStyle))
        index_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        index_label.setCursor(QCursor(Qt.IBeamCursor))
        index_label.show()

        y_end = first_encode_elem_y + (self._elem_margin_y*2) + (first_encode_elem_height*2)
        anim = QPropertyAnimation(index_label, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(index_label.sizeHint().width()*2), int(index_label.sizeHint().height()*2)))

        speed = int(self.getSpeedFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.finished.connect(lambda: self.setResultLabel('index', index_label))
        self.animCounterIncrease()
        self.anim_group.start()


    def selectIndex(self, row, direction, found=False):
        if direction == 'next':
            previous = row-1
        if direction == 'prev':
            previous = row+1
        if direction == 'update':
            previous = -1

        if found:
            start_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_select_found_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_select_found_text.value))
        else:
            start_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_select_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_select_text.value))

        tableSort = self.getTable(TableName.tableSort.value)
        for i in range(len(tableSort)):
            for label in tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=500)
                elif(i == previous):
                    self.animateBackgroundColor(label, end_color_background, start_color_background, end_color_text, start_color_text, duration=500)

    def showIndex(self, row):

        table = self.getTableEntry(TableName.tableSort.value, row)
        first_label = table[0]
        entry_y = first_label.geometry().y()
        entry_x = first_label.geometry().x()

        index_label_x = entry_x - self._index_margin
        index_label = QLabel(self)
        label_text = str(row+1) + ".)"
        index_label.setText(label_text)
        index_label.setGeometry(QRect(index_label_x, entry_y, 0, 0))
        index_label.setAlignment(Qt.AlignCenter)
        index_label.show()
        self.anim = QPropertyAnimation(index_label, b"geometry", self)
        self.anim.setEndValue(QRect(index_label.geometry().x(), index_label.geometry().y(), index_label.sizeHint().width(),
                                    self._label_height))

        speed = int(self.getSpeedFactor()*500)
        self.anim.setDuration(speed)
        self.anim.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim.start()

        self.appendTable(TableName.tableIndex.value, index_label)


    def selectLastChar(self, row_index):

        table_sort = self.getTableEntry(TableName.tableSort.value, row_index)
        last_label = table_sort[-1]

        last_char = QLabel(self)
        last_char.setAlignment(Qt.AlignCenter)
        last_char.setText(last_label.text())
        last_char.setStyleSheet(self._color_setting.get(Setting.label_animation_style.value))
        last_char.resize(self._label_width, self._label_height)
        last_char.move(last_label.geometry().x(), last_label.geometry().y())
        last_char.show()

        table_encode_length = self.getTableLength(TableName.tableEncode.value)
        y_start = round(self._right_box_height / 2)
        if(table_encode_length == 0):
            x_start = self._right_box_x_start
        else:
            prev_last = self.getTableEntry(TableName.tableEncode.value, -1)
            x_start = prev_last.geometry().x() + self._label_width + self._elem_margin_x

        self.anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(last_char, b"geometry", self)
        anim.setEndValue(QRect(last_char.geometry().x(), last_char.geometry().y(), int(last_char.geometry().width()*1.3),
                               int(last_char.geometry().height()*1.3)))
        speed = int(self.getSpeedFactor()*50)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_char, b"geometry", self)
        anim.setEndValue(QRect(last_char.geometry().x(), last_char.geometry().y(), self._label_width, self._label_height))
        speed = int(self.getSpeedFactor()*50)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_char, b"pos", self)
        anim.setEndValue(QPoint(x_start, y_start))
        speed = int(self.getSpeedFactor()*350)
        anim.setDuration(speed)
        anim.start()

        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(350*self._speedFactor.getFactor())
        start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
        start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
        end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
        end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
        self.animateBackgroundColor(last_char, start_color_background, end_color_background, start_color_text,
                                    end_color_text, duration=speed)

        self.appendTable(TableName.tableEncode.value, last_char)


    def selectSortedRow(self, row_index, step):
        table = self.getTableEntry(TableName.table.value, row_index)
        copy_table = []
        self.anim_group = QSequentialAnimationGroup(self)

        for label in table:
            label_copy = QLabel(self)
            label_copy.setAlignment(Qt.AlignCenter)
            label_copy.setText(str(label.text()))
            label_copy.setStyleSheet(self._color_setting.get(Setting.label_animation_style.value))
            label_copy.resize(self._label_width, self._label_height)
            label_copy.move(label.geometry().x(), label.geometry().y())
            label_copy.show()
            copy_table.append(label_copy)

        y_table = self.getTableEntry(TableName.table.value, step)
        y_start = y_table[0].geometry().y()
        first = True
        for label in copy_table:
            if first:
                x_start = self._middle_box_x_start
                x_end = x_start
                first = False
            else:
                x_start = x_start + self._label_width + self._elem_margin_x
                x_end = x_start #+ self._elem_margin_x

            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(self.getSpeedFactor()*200)
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(200*len(copy_table)*self._speedFactor.getFactor())
        for label in copy_table:
            start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)

        self.appendTable(TableName.tableSort.value, copy_table)

    def rotate(self):
        copy_table = []
        self.anim_group = QSequentialAnimationGroup(self)
        print(self._color_setting)
        table = self.getLastTableEntry(TableName.table.value)

        for label in table:
            label_copy = CustomLabel(self)
            label_copy.setAlignment(Qt.AlignCenter)
            label_copy.setText(str(label.text()))
            style = self._color_setting.get(Setting.label_animation_style.value)
            label_copy.setStyleSheet(style)
            label_copy.resize(self._label_width, self._label_height)
            label_copy.move(label.geometry().x(), label.geometry().y())
            label_copy.show()
            copy_table.append(label_copy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copy_table:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            anim = QPropertyAnimation(label, b"pos")
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.setEndValue(QPoint(x_start, y_end))
            speed = int(self.getSpeedFactor()*300)
            anim.setDuration(speed)
            par_anim_group.addAnimation(anim)

        par_anim_group.start()
        last_label = copy_table[-1]
        first_pos = copy_table[0].pos()

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y() + self._label_line_margin_double))
        speed = int(self.getSpeedFactor()*200)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        for i in range(len(copy_table)-2, -1, -1):
            label = copy_table[i]
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            x_end = copy_table[i+1].geometry().x()
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_end))
            speed = int(self.getSpeedFactor()*150)
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y() + self._label_line_margin_double))
        speed = int(self.getSpeedFactor()*400)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y() + self._label_line_margin))
        speed = int(self.getSpeedFactor()*400)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(400)
        for label in copy_table:
            start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)

        table_rotated = self._utils_table.rotateTable(copy_table)
        self.appendTable(TableName.table.value, table_rotated)


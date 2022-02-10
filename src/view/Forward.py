import functools

from model.Description import DESC, Description
from controller.Speed import Speed
from controller import Utils
import styles.Style as sty
from styles.Style import Style
from view.ColorSettings import Setting, ColorType
from view.CustomLabel import CustomLabel
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup, QVariantAnimation


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
        self._description = None
        self._input_text = input
        self._color_setting = None
        self._anim = 0
        self._anim_count = 0
        self._animGroup = 0
        self._animCounter = 0

    def updateSpeed(self, factor):
        self._speedFactor.update(factor)

    def setColorSetting(self, setting):
        self._color_setting = setting

    def updateSelectColor(self, step):
        self.selectIndex(step, 'update', found=False)

    def updateSelectFoundColor(self, step):
        self.selectIndex(step, 'update', found=True)

    def updateLabelColor(self):
        for list in self._table:
            self.setLabelStyle(list)

        for list in self._tableSort:
            self.setLabelStyle(list)

        self.setLabelStyle(self._tableEncode)

    def setLabelStyle(self, list):
        style = self._color_setting.get(Setting.label_style.value)
        for label in list:
            self.setStyle(label, style)


    def setStyle(self, label, style):
        label.setStyleSheet(style)

    def setStart(self, x, y):
        self._x = x
        self._y = y
        self.setGeometry(x, y, self.geometry().width(), self.geometry().height())

    def setInput(self, input):
        self._input_text = input

    def setWidth(self, width):
        self.setGeometry(self.geometry().x(), self.geometry().y(), width, self.geometry().height())
        self._width = width

    def setHeight(self, height):
        self.setGeometry(self.geometry().x(), self.geometry().y(), self.geometry().width(), height)
        self._height = height

    def update(self):
        self.initLayout()
        self.initForward()

    def deleteLastTable(self):
        self._utils_table.deleteLabelList(self._table[-1])
        del self._table[-1]

    def deleteLastTableSorted(self):
        self._utils_table.deleteLabelList(self._tableSort[-1])
        del self._tableSort[-1]

    def deleteLastEncodeLabel(self):
        self._utils_table.deleteLastLabel(self._tableEncode)


    def deleteIndexTable(self):
        self._utils_table.deleteLastLabel(self._tableIndex)

    def setResultLabel(self, key, val):
        self._resultLabel[key] = val

    def deleteResultLabel(self):
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'encode')
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'index')

    def animCounterIncrease(self):
        self._animCounter = self._animCounter + 1
        print("Increase: " + str(self._animCounter))

    def animCounterDecrease(self):
        self._animCounter = self._animCounter - 1
        print("Decrease: " + str(self._animCounter))

    def getAnimCounter(self):
        return self._animCounter

    def reset(self):
        self._utils_table.resetTable(self._table)
        self._utils_table.resetTable(self._tableSort)
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'encode')
        self._utils_table.deleteDirectoryEntry(self._resultLabel, 'index')
        self._utils_table.deleteLabelList(self._tableIndex)
        self._utils_table.deleteLabelList(self._tableEncode)

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
        self.reset()
        self._table = []
        self._tableIndex = []
        self._tableSort = []
        self._tableSortIndex = []

        row = []
        text = ""

        self._labelWidth = round(self._width/100)

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

        self._resultLabelMargin = self._right_box_height * 0.05

        self._elem_margin_x = self._width * 0.005
        self._elem_margin_y = self._height * 0.04

        #self._indexMargin = round(self._width / 50)
        self._indexMargin = self._width * 0.03


        elemCount = 0
        for ch in self._input_text:
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(self._color_setting.get(Setting.label_style.value))
            y_start = self._left_box_y_start
            label.resize(self._labelWidth, self._labelHeight)

            if elemCount == 0:
                x_start = self._left_box_x_start
            else:
                x_start = x_start + self._labelWidth + self._elem_margin_x

            label.move(x_start, y_start)
            row.append(label)
            elemCount = elemCount + 1


        self._table.append(row)

    def setDescription(self, info):
        self._description.setDescription(info)

    def showFinalEncodeLabel(self, encode_text):
        encodeLabel = self._tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()

        encode = QLabel(self)
        encode.setText("Encode: " + encode_text)
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
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.finished.connect(lambda: self.setResultLabel('encode', encode))
        self.animCounterIncrease()
        self.anim_group.start()

    def selectFinalIndexLabel(self, row):
        encodeLabel = self._tableEncode[0]
        first_encode_elem_y = encodeLabel.geometry().y()
        first_encode_elem_x = encodeLabel.geometry().x()
        first_encode_elem_height = encodeLabel.geometry().height()
        self.anim_group = QSequentialAnimationGroup(self)

        label = self._tableIndex[row]
        label_val = label.text()[0]
        label_x_start = label.geometry().x()
        label_y_start = label.geometry().y()

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, int(label.geometry().width()*1.3), int(label.geometry().height()*1.3)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(label, b"geometry")
        anim.setEndValue(QRect(label_x_start, label_y_start, label.geometry().width(), label.geometry().height()))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.animCounterIncrease()
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.start()


        indexLabel = QLabel(self)
        indexLabel.setText("Index: " + str(label_val))
        indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        indexLabel.setStyleSheet(sty.getStyle(Style.resultLabelStyle))
        indexLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        indexLabel.setCursor(QCursor(Qt.IBeamCursor))
        indexLabel.show()

        y_end = first_encode_elem_y + (self._elem_margin_y*2) + (first_encode_elem_height*2)
        anim = QPropertyAnimation(indexLabel, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.anim_group.finished.connect(lambda: self.setResultLabel('index', indexLabel))
        self.animCounterIncrease()
        self.anim_group.start()



    #def selectIndex(self, row, direction, start_color, end_color):
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


        for i in range(len(self._tableSort)):
            for label in self._tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=500)
                elif(i == previous):
                    self.animateBackgroundColor(label, end_color_background, start_color_background, end_color_text, start_color_text, duration=500)

    def showIndex(self, row):

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
        indexLabel.show()
        self.anim = QPropertyAnimation(indexLabel, b"geometry", self)
        self.anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
                                    self._labelHeight))
        speed = int(500*self._speedFactor.getFactor())
        self.anim.setDuration(speed)
        self.anim.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim.start()

        self._tableIndex.append(indexLabel)


    def selectLastChar(self, row_index):

        table = self._tableSort[row_index]
        lastLabel = table[-1]

        lastChar = QLabel(self)
        lastChar.setAlignment(Qt.AlignCenter)
        lastChar.setText(lastLabel.text())
        lastChar.setStyleSheet(self._color_setting.get(Setting.label_animation_style.value))
        lastChar.resize(self._labelWidth, self._labelHeight)
        lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
        lastChar.show()

        y_start = round(self._right_box_height / 2)
        if(len(self._tableEncode) == 0):
            x_start = self._right_box_x_start
        else:
            prev_last = self._tableEncode[-1]
            x_start = prev_last.geometry().x() + self._labelWidth + self._elem_margin_x

        self.anim_group = QSequentialAnimationGroup(self)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), int(lastChar.geometry().width()*1.3),
                               int(lastChar.geometry().height()*1.3)))
        speed = int(self._speedFactor.getFactor() * 50)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"geometry", self)
        anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), self._labelWidth, self._labelHeight))
        speed = int(self._speedFactor.getFactor() * 50)
        anim.setDuration(speed)

        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(lastChar, b"pos", self)
        anim.setEndValue(QPoint(x_start, y_start))
        speed = int(350*self._speedFactor.getFactor())
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
        self.animateBackgroundColor(lastChar, start_color_background, end_color_background, start_color_text,
                                    end_color_text, duration=speed)

        self._tableEncode.append(lastChar)


    def selectSortedRow(self, row_index, step):

        table = self._table[row_index]
        copyTable = []
        self.anim_group = QSequentialAnimationGroup(self)

        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            #labelCopy.setStyleSheet(sty.getStyle(Style.labelStyleInit))
            labelCopy.setStyleSheet(self._color_setting.get(Setting.label_animation_style.value))
            labelCopy.resize(self._labelWidth, self._labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.show()
            copyTable.append(labelCopy)

        y_table = self._table[step]
        y_start = y_table[0].geometry().y()
        first = 1
        for label in copyTable:
            if first:
                x_start = self._middle_box_x_start
                first = 0
            else:
                x_start = x_start + self._labelWidth + self._elem_margin_x

            x_end = x_start + self._elem_margin_x
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(200*self._speedFactor.getFactor())
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(200*len(copyTable)*self._speedFactor.getFactor())
        for label in copyTable:
            start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)

        self._tableSort.append(copyTable)

    def rotate(self):
        copyTable = []
        self.anim_group = QSequentialAnimationGroup(self)
        print(self._color_setting)
        table = self._table[-1]
        for label in table:
            labelCopy = CustomLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            style = self._color_setting.get(Setting.label_animation_style.value)
            print(style)
            labelCopy.setStyleSheet(style)
            #labelCopy.setStyleSheet(sty.getStyle(Style.labelStyleInit))
            labelCopy.resize(self._labelWidth, self._labelHeight)
            labelCopy.move(label.geometry().x(), label.geometry().y())
            labelCopy.show()
            copyTable.append(labelCopy)

        par_anim_group = QParallelAnimationGroup(self)
        for label in copyTable:
            x_start = label.geometry().x()
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            anim = QPropertyAnimation(label, b"pos")
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.setEndValue(QPoint(x_start, y_end))
            speed = int(300*self._speedFactor.getFactor())
            anim.setDuration(speed)
            par_anim_group.addAnimation(anim)

        par_anim_group.start()
        last_label = copyTable[-1]
        first_pos = copyTable[0].pos()

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+self._labelLineMarginDouble))
        speed = int(200*self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        for i in range(len(copyTable)-2, -1, -1):
            label = copyTable[i]
            y_start = label.geometry().y()
            y_end = y_start + (label.geometry().height()*2)
            x_end = copyTable[i+1].geometry().x()
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_end))
            speed = int(150*self._speedFactor.getFactor())
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self._labelLineMarginDouble))
        speed = int(400*self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)

        anim = QPropertyAnimation(last_label, b"pos")
        anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self._labelLineMargin))
        speed = int(400 * self._speedFactor.getFactor())
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.finished.connect(self.animCounterDecrease)
        self.animCounterIncrease()
        self.anim_group.start()

        speed = int(400)
        for label in copyTable:
            start_color_background = QColor(self._color_setting.get(Setting.label_animation_background.value))
            start_color_text = QColor(self._color_setting.get(Setting.label_animation_text.value))
            end_color_background = QColor(self._color_setting.get(Setting.label_background.value))
            end_color_text = QColor(self._color_setting.get(Setting.label_text.value))
            self.animateBackgroundColor(label, start_color_background, end_color_background, start_color_text, end_color_text, duration=speed)

        self._tableLast = copyTable.copy()
        tableRotated = self._utils_table.rotateTable(copyTable)
        self._table.append(tableRotated)


    def animateBackgroundColor(self, widget, start_color, end_color, start_color_text, end_color_text, duration=1000):
        duration = int(duration*self._speedFactor.getFactor())

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
        background = widget.styleSheet().split(";")[0]
        text = widget.styleSheet().split(";")[1]
        background = r"background-color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)

    def setLabelText(self, widget, color):
        background = widget.styleSheet().split(";")[0]
        text = r"color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)


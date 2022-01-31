import functools
from data.iText import TextTable
from data import iText
from data.Description import DESC, Description
from gui.Speed import Speed
from gui import Utils
import styles.Style as sty
from styles.Style import Style
from gui.CustomLabel import CustomLabel
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup, QVariantAnimation, QAbstractAnimation


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
        self._input_text = input
        self._encode = ""
        self._index = None
        self._anim = 0
        self._animGroup = 0
        #self.update()

    def updateSpeed(self, factor):
        self._speedFactor.update(factor)

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
            label = QLabel(self)
            label.setAlignment(Qt.AlignCenter)
            label.setText(str(ch))
            text = text + str(ch)
            label.setStyleSheet(sty.getStyle(Style.labelStyle))
            y_start = self._left_box_y_start
            label.resize(self._labelWidth, self._labelHeight)

            if elemCount == 0:
                x_start = self._left_box_x_start
            else:
                x_start = x_start + self._labelWidth + self._labelMargin

            label.move(x_start, y_start)
            row.append(label)
            elemCount = elemCount + 1

        #self.appendTable(row)
        self._table.append(row)

    def setDescription(self, info):
        self._description.setDescription(info)

    def showFinalEncodeLabel(self):
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
        encode.show()

        y_end = first_encode_elem_y + self._resultLabelMargin + first_encode_elem_height
        self.anim_group = QSequentialAnimationGroup(self)
        anim = QPropertyAnimation(encode, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()
        self._resultLabel['encode'] = encode

    def selectFinalIndexLabel(self, row):
        encodeLabel = self._resultLabel.get('encode')
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
        self.anim_group.start()


        indexLabel = QLabel(self)
        indexLabel.setText("Index: " + str(label_val))
        indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
        indexLabel.setStyleSheet("font-weight: bold; border: 1px solid black")
        indexLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        indexLabel.setCursor(QCursor(Qt.IBeamCursor))
        indexLabel.show()

        y_end = first_encode_elem_y + self._resultLabelMargin + first_encode_elem_height
        anim = QPropertyAnimation(indexLabel, b"geometry")
        anim.setEndValue(QRect(first_encode_elem_x, y_end,
                               int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
        speed = int(self._speedFactor.getFactor()*500)
        anim.setDuration(speed)
        self.anim_group.addAnimation(anim)
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()

        self._resultLabel['index'] = indexLabel



    def selectIndex(self, row, direction, start_color, end_color):
        if direction == 'next':
            previous = row-1
        if direction == 'prev':
            previous = row+1

        for i in range(len(self._tableSort)):
            for label in self._tableSort[i]:
                if(i == row):
                    self.animateBackgroundColor(label, start_color, end_color, duration=500, setAnim=True)
                elif(i == previous):
                    self.animateBackgroundColor(label, end_color, start_color, duration=500, setAnim=True)




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
        self.anim.stateChanged.connect(self.setAnimState)
        self.anim.finished.connect(self.setAnimState)
        self.anim.start()

        self.appendIndexTable(indexLabel)


    def selectLastChar(self, row_index):

        table = self._tableSort[row_index]
        lastLabel = table[-1]

        lastChar = QLabel(self)
        lastChar.setAlignment(Qt.AlignCenter)
        lastChar.setText(lastLabel.text())
        lastChar.setStyleSheet("background-color:red; color: white;")
        lastChar.resize(self._labelWidth, self._labelHeight)
        lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
        lastChar.show()

        tableIndexHalf = round(len(self._tableSort)/2)

        labelHalf_y = round(self._right_box_height / 2)
        if(len(self._tableEncode) == 0):
            lastChar_x_end = self._right_box_x_start
        else:
            prev_last = self._tableEncode[-1]
            lastChar_x_end = self._labelWidth + self._labelMargin + prev_last.geometry().x()

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
        anim.setEndValue(QPoint(lastChar_x_end, labelHalf_y))
        speed = int(350*self._speedFactor.getFactor())
        anim.setDuration(speed)
        anim.start()

        self.anim_group.addAnimation(anim)
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()

        speed = int(350*self._speedFactor.getFactor())
        self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=speed, setAnim=False)
        self.appendEncodeTable(lastChar)
        self.setEncode((self._encode + lastLabel.text()))


    def selectSortedRow(self, row_index, step):

        table = self._table[row_index]
        copyTable = []
        self.anim_group = QSequentialAnimationGroup(self)

        for label in table:
            labelCopy = QLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet("background-color:red; color:white;")
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
                x_start = x_start + self._labelWidth + self._labelMargin

            x_end = x_start + self._labelMargin
            anim = QPropertyAnimation(label, b"pos")
            anim.setEndValue(QPoint(x_end, y_start))
            speed = int(350*self._speedFactor.getFactor())
            anim.setDuration(speed)
            self.anim_group.addAnimation(anim)

        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()

        speed = int(350*len(copyTable)*self._speedFactor.getFactor())
        for label in copyTable:
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=speed, setAnim=False)

        self.appendSortedTable(copyTable)

    def rotate(self):
        copyTable = []
        self.anim_group = QSequentialAnimationGroup(self)
        #self.anim_group = QParallelAnimationGroup(self)

        table = self._table[-1]
        for label in table:
            labelCopy = CustomLabel(self)
            labelCopy.setAlignment(Qt.AlignCenter)
            labelCopy.setText(str(label.text()))
            labelCopy.setStyleSheet(sty.getStyle(Style.labelStyleCopyInit))
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
            # y_end = y_start + 50
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
        self.anim_group.stateChanged.connect(self.setAnimGroupState)
        self.anim_group.finished.connect(self.setAnimGroupState)
        self.anim_group.start()

        speed = int(400*self._speedFactor.getFactor())
        anim_group2 = QSequentialAnimationGroup(self)
        for label in copyTable:
            #anim_group2.addAnimation(self.getAnimateBackgroundColor(label, QColor("orange"), QColor("red"),
            #                                                            duration=speed, setAnim=False))
            self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=speed, setAnim=False)

        #self.anim_group.stateChanged.connect(self.setAnimGroupState)
        #self.anim_group.finished.connect(self.setAnimGroupState)
        #self.anim_group.start()

        self._tableLast = copyTable.copy()
        tableRotated = self._utils_table.rotateTable(copyTable)
        self._table.append(tableRotated)

        text_rotate = iText.rotateText(self._textTable.getLastText())
        self._textTable.addText(text_rotate)



    def getAnimateBackgroundColor(self, widget, start_color, end_color, duration=1000, setAnim=False):
        duration = int(duration*self._speedFactor.getFactor())
        anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        return anim

    def animateBackgroundColor(self, widget, start_color, end_color, duration=1000, setAnim=False):
        duration = int(duration*self._speedFactor.getFactor())
        self.anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
        self.anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
        self.anim.stateChanged.connect(self.setAnimState)
        self.anim.finished.connect(self.setAnimState)

        #self.anim.start(QAbstractAnimation.DeleteWhenStopped)
        self.anim.start()

    def setLabelBackground(self, widget, color):
        widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))

    # def animateLabelText(self, widget, start_text, end_text, duration=1000):
    #     duration = int(duration*self._speedFactor.getFactor())
    #     self.anim = QVariantAnimation(widget, duration=duration, startValue=start_text, endValue=end_text, loopCount=1)
    #     self.anim.valueChanged.connect(functools.partial(self.setLabelText, widget))
    #     #self.anim.stateChanged.connect(self.setAnimState)
    #     #self.anim.finished.connect(self.setAnimState)
    #     #self.anim.start(QAbstractAnimation.DeleteWhenStopped)
    #     self.anim.start()

    def setLabelText(self, widget, text):
        widget.setText(text)

    def setLabelStyle(self, table, style):
        for label in table:
            label.setStyleSheet(style)

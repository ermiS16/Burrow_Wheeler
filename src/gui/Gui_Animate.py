import functools
import sys
import time


from gui import Utils
from data.Description import DESC, Description
from gui.State import STATE, State
from gui.ControlPanel import ControlPanel, ElemKeys, Direction
from gui.Step import Step
from gui.Window import Window
from logic.Forward import Forward as f_logic

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSlot, QObject, QThread, QThreadPool, QRunnable, pyqtSignal

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, func, *args):
        super().__init__()
        self._func = func
        self._args = list[args]

    def run(self):
        self._func
        self.finished.emit()

class Rotate(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, content):
        super().__init__()
        self._content = content

    def run(self):
        print("Thread: " + str(self.thread().currentThread()))
        print(self._content.getAnim())
        self._content.rotate()
        while(self._content.getAnim() != 0):
            pass

        self.finished.emit()

class AnimListener(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, func, *args):
        super().__init__()
        self._func = func
        self._args = list[args]

    def run(self):
        #print(self._func.__name__)
        print("Anim: " + str(self._func.getAnim()))
        while(self._func.getAnim() == 0):
            pass
            #print("Init")
        while(self._func.getAnim() == 2):
            pass
            #print("Running")

        #print("Animation finished")

        self.finished.emit()



class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self.content = None

        self.utils_table = Utils.Table()
        self.utils_btn = Utils.Button()
        self.utils_label = Utils.Label()

        self._step = Step(0, 0)
        self._step.printStep()
        self.speedFactor = 1
        self.state = State(STATE.INIT)
        self.initUI()

    def resetWindow(self):
        childs = self.mainFrameWidget.children()
        print(str(childs))
        for child in childs:
            if child.objectName() != 'ControlPanel':
                child.deleteLater()

    def initWindow(self):
        self.win = Window(self.screen())
        self.window_width = self.win.getWindowWidth()
        self.window_height = self.win.getWindowHeight()
        self.screen_width = self.win.getScreenWidth()
        self.screen_height = self.win.getScreenHeight()
        self.menu_bar_offset = self.menuBar().geometry().height()

        self.main_window_x_start = round(self.screen_width/2) - round(self.window_width/2)
        self.main_window_y_start = round(self.screen_height/2) - round(self.window_height/2)

        self.setGeometry(self.main_window_x_start, self.main_window_y_start, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Burrows-Wheeler Transformation")


    def initUI(self):
        self.createMenu()
        self.initWindow()
        self.controlPanel = ControlPanel(self)
        self.controlPanel.setObjectName('ControlPanel')
        self.controlPanel.setWidth(self.win.getWindowWidth())
        self.controlPanel.setHeight((self.win.getWindowHeight()*0.1))
        self.controlPanel.setX(50)
        self.controlPanel.setY(self.menu_bar_offset)
        self.controlPanel.setParent(self.mainFrameWidget)

        self.controlPanel.connectBtnOnClick(ElemKeys.transform_button, self.transform)
        self.controlPanel.connectBtnOnClick(ElemKeys.reset_button, self.resetWindow)
        self.controlPanel.show()

        self.speed_slider = self.controlPanel.getElem(ElemKeys.speed_slider)

        self.setCentralWidget(self.mainFrameWidget)
        self.show()

    def transform(self):
        direction = self.controlPanel.getDirection()

        print(direction)
        if direction == Direction.forward.value:
            next_btn = self.controlPanel.getElem(ElemKeys.next_button)
            prev_btn = self.controlPanel.getElem(ElemKeys.prev_button)
            next_btn.setEnabled(True)
            prev_btn.setEnabled(True)

            input = self.controlPanel.getInputText()
            self._step.reset()
            self._step.setMax(len(input))
            #print(input)

            if self.content != None:
                for child in self.content.children():
                    child.deleteLater()
                #self.content.deleteLater()
            self.content = f_logic(self, input)
            #self.content.initLayout()

            #self.content.initForward(input)
            #self.content.setInput(input)
            self.updateSpeed(self.content)
            self.content.setWidth(self.win.getWindowWidth())
            self.content.setHeight(self.win.getWindowHeight())
            self.content.setStart(0, self.controlPanel.getHeight())
            self.content.initLayout()
            self.content.initForward()
            self.content.setParent(self.mainFrameWidget)
            self.content.show()
            #self.content.reset()


            self.state.setState(STATE.F_ROTATION)
            self.controlPanel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self.content)
            self.controlPanel.connectBtnOnClick(ElemKeys.next_button, self.f_next_step)
            self.controlPanel.connectBtnOnClick(ElemKeys.prev_button, self.f_prev_step)
            self._step.printStep()


        if direction == Direction.backwards.value:
            pass

        if direction == Direction.choose.value:
            pass

    def updateSpeed(self, content):
        factor = ((self.speed_slider.value() / 5) ** -1)
        content.updateSpeed(factor)

    def toggleControlPanelBtn(self):
        print("Toggle Control Buttons")
        next_btn = self.controlPanel.getElem(ElemKeys.next_button)
        prev_btn = self.controlPanel.getElem(ElemKeys.prev_button)
        transform_btn = self.controlPanel.getElem(ElemKeys.transform_button)
        reset_btn = self.controlPanel.getElem(ElemKeys.reset_button)
        self.utils_btn.toggleButtons([next_btn, prev_btn, transform_btn, reset_btn])

    def f_next_step(self):
        if not self._step.isMAX() and self.state.getState() != STATE.F_END:
            self._step.increase()
            self._step.printStep()

        if(self.state.getState() == STATE.F_ROTATION):
            self.state.printState()
            if self._step.isMAX():
                self.state.setState(STATE.F_SORT)
                self._step.reset()
                self.content.setDescription(DESC.forward_sort)
            else:
                #print(self.content.getAnim())
                self.toggleControlPanelBtn()
                self.thread = QThread()
                #self.worker = Worker(self.content.rotate())
                #self.worker = Rotate(self.content)
                self.worker = AnimListener(self.content)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.toggleControlPanelBtn)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()
                self.content.rotate()

        if(self.state.getState() == STATE.F_SORT):
            self.state.printState()
            #if self._step == self._MAX_STEPS:
            if self._step.isMAX():
                self.state.setState(STATE.F_ENCODE)
                #self._step = 0
                self._step.reset()
                self.content.setDescription(DESC.forward_encode)
                #self.description.setDescription(DESC.forward_encode)
            else:
                self.content.sortTextTable()
                #row_index = self.textTable.getRef(self._step)
                row_index = self.content.getTextTableRef(self._step.getStep())
                self.content.selectSortedRow(row_index, self._step.getStep())

        if(self.state.getState() == STATE.F_ENCODE):
            self.state.printState()
            #if self._step == self._MAX_STEPS:
            if self._step.isMAX():
                self.state.setState(STATE.F_INDEX_SHOW)
                #self._step = 0
                self._step.reset()
                self.content.setDescription(DESC.forward_index)
                #self.description.setDescription(DESC.forward_index)
            else:
                self.content.selectLastChar(self._step.getStep())

        if(self.state.getState() == STATE.F_INDEX_SHOW):
            self.state.printState()
            #for i in range(self._MAX_STEPS+1):
            for i in range(self._step.MAX+1):
                #if i == self._MAX_STEPS:
                if i == self._step.MAX:
                    self.state.setState(STATE.F_INDEX_SELECT)
                    #self._step = 0
                    self._step.reset()
                else:
                    self.content.showIndex(i)

        if(self.state.getState() == STATE.F_INDEX_SELECT):
            self.state.printState()
            if(self.content.getSortedTextAtIndex(self._step.getStep()) == self.content.getInpuText()):
                self.content.selectIndex(self._step.getStep(), "next", QColor("red"), QColor("green"))
                self.state.setState(STATE.F_INDEX_FINAL)
                self.content.setDescription(DESC.forward_end)
                #self.description.setDescription(DESC.forward_end)
            else:
                self.content.selectIndex(self._step.getStep(), "next", QColor("red"), QColor("blue"))

        if(self.state.getState() == STATE.F_INDEX_FINAL):
            self.state.printState()
            self.content.showFinalEncodeLabel()
            self.content.selectFinalIndexLabel(self._step.getStep())
            self.state.setState(STATE.F_END)

        if(self.state.getState() == STATE.F_END):
            self.state.printState()
            self._step.printStep()


    def f_prev_step(self):
        self._step.printStep()
        self.state.printState()

        if (self.state.getState() == STATE.F_ROTATION):
            if (self._step.getStep() > 0):
                #tableLast = self.table[-1]
                #self.deleteLabelList(self.table[-1])
                table = self.content.getTable()
                self.utils_table.deleteLabelList(table[-1])
                del table[-1]
                self.content.removeLastText()

            next_step = self._step.getStep() - 1
            if next_step < 0:
                pass
            else:
                self._step.decrease()

        elif (self.state.getState() == STATE.F_SORT):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()

            if (self._step.getStep() >= 0):
                #self.deleteLabelList(self.tableSort[-1])
                sortedTable = self.content.getSortedTable()
                self.utils_table.deleteLabelList(sortedTable[-1])
                del sortedTable[-1]

            if (self._step.getStep() < 0):
                sortedTable = self.content.getSortedTable()
                self.utils_table.deleteLabelList(sortedTable[-1])
                #self.deleteLabelList(self.tableSort[-1])
                del sortedTable[-1]
                self.state.setState(STATE.F_ROTATION)
                self._step.setStep((self._step.MAX - 1))
                #self.displayInfoText(DESC.forward_rotation.value)
                self.content.setDescription(DESC.forward_rotation)

        elif (self.state.getState() == STATE.F_ENCODE):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()

            if (self._step.getStep() >= 0):
                encodeTable = self.content.getEncodeTable()
                self.utils_table.deleteLastLabel(encodeTable)
                #self.deleteLastLabel(self.tableEncode)
                encode = self.content.getEncode()
                encode = encode[0:-1]
                #print(encode)
                self.content.setEncode(encode)
                #self.encode = self.encode[0::-1]

            if (self._step.getStep() < 0):
                encodeTable = self.content.getEncodeTable()
                self.utils_table.deleteLastLabel(encodeTable)
                #self.deleteLastLabel(self.tableEncode)
                self.state.setState(STATE.F_SORT)
                #self._step.decrease()
                self._step.setStep((self._step.MAX - 1))
                #self.displayInfoText(DESC.forward_sort.value)
                self.content.setDescription(DESC.forward_sort)

        elif (self.state.getState() == STATE.F_INDEX_SHOW):
            for i in range(self._step.MAX):
                self._step.decrease()
                self._step.printStep()
                self.state.printState()
                if (self._step.getStep() >= 0):
                    indexTable = self.content.getIndexTable()
                    self.utils_table.deleteLastLabel(indexTable)
                    #self.deleteLastLabel(self.tableIndex)

                if (self._step.getStep() < 0):
                    indexTable = self.content.getIndexTable()
                    self.utils_table.deleteLastLabel(indexTable)
                    #self.deleteLastLabel(self.tableIndex)
                    self.state.setState(STATE.F_ENCODE)
                    self._step.setStep((self._step.MAX - 1))
                    #self._step.decrease()
                    #self.displayInfoText(DESC.forward_encode.value)
                    self.content.setDescription(DESC.forward_encode)

        elif (self.state.getState() == STATE.F_INDEX_SELECT):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            if (self._step.getStep() >= 0):
                self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))

            if (self._step.getStep() < 0):
                self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))
                self.state.setState(STATE.F_INDEX_SHOW)
                #self._step.decrease()
                self._step.setStep((self._step.MAX - 1))

        elif (self.state.getState() == STATE.F_END):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))
            self.state.setState(STATE.F_INDEX_SELECT)
            #self.utils_table.deleteResultLabel()
            resultLabel = self.content.getResultLabel()
            self.utils_table.deleteDirectoryEntry(resultLabel, 'encode')
            self.utils_table.deleteDirectoryEntry(resultLabel, 'index')
            #self.deleteResultLabel()
            #self.displayInfoText(DESC.forward_index.value)
            self.content.setDescription(DESC.forward_index)


    # def showFinalEncodeLabel(self):
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #     self.toggleButtons()
    #     encodeLabel = self.tableEncode[0]
    #     first_encode_elem_y = encodeLabel.geometry().y()
    #     first_encode_elem_x = encodeLabel.geometry().x()
    #     first_encode_elem_height = encodeLabel.geometry().height()
    #
    #     encode = QLabel(self)
    #     encode.setText("Encode: " + self.encode)
    #     encode.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
    #     encode.setStyleSheet("font-weight: bold; border: 1px solid black")
    #     encode.setTextInteractionFlags(Qt.TextSelectableByMouse)
    #     encode.setCursor(QCursor(Qt.IBeamCursor))
    #     encode.setParent(self.mainFrameWidget)
    #     encode.show()
    #
    #     y_end = first_encode_elem_y + self.resultLabelMargin + first_encode_elem_height
    #     anim_group = QSequentialAnimationGroup(self)
    #     anim = QPropertyAnimation(encode, b"geometry")
    #     #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+50, int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
    #     anim.setEndValue(QRect(first_encode_elem_x, y_end,
    #                            int(encode.sizeHint().width()*2), int(encode.sizeHint().height()*2)))
    #     speed = int(self.speedFactor*500)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #     anim_group.finished.connect(self.toggleButtons)
    #     #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     anim_group.start()
    #     self.resultLabel['encode'] = encode
    #
    # def selectFinalIndexLabel(self, row):
    #     self.toggleButtons()
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #     #encodeLabel = self.tableEncode[0]
    #     encodeLabel = self.resultLabel.get('encode')
    #     first_encode_elem_y = encodeLabel.geometry().y()
    #     first_encode_elem_x = encodeLabel.geometry().x()
    #     first_encode_elem_height = encodeLabel.geometry().height()
    #     print(str(first_encode_elem_x), str(first_encode_elem_y), str(first_encode_elem_height))
    #     anim_group = QSequentialAnimationGroup(self)
    #
    #     label = self.tableIndex[row]
    #     label_val = label.text()[0]
    #     label_x_start = label.geometry().x()
    #     label_y_start = label.geometry().y()
    #
    #     print(str(label_x_start), str(label_y_start), str(label.geometry().width()), str(label.geometry().height()))
    #     anim = QPropertyAnimation(label, b"geometry")
    #     anim.setEndValue(QRect(label_x_start, label_y_start, int(label.geometry().width()*1.3), int(label.geometry().height()*1.3)))
    #     speed = int(self.speedFactor*500)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #
    #     anim = QPropertyAnimation(label, b"geometry")
    #     anim.setEndValue(QRect(label_x_start, label_y_start, label.geometry().width(), label.geometry().height()))
    #     speed = int(self.speedFactor*500)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #     anim_group.start()
    #
    #
    #     indexLabel = QLabel(self)
    #     indexLabel.setText("Index: " + str(label_val))
    #     #indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y+50, 0, 0))
    #     indexLabel.setGeometry(QRect(first_encode_elem_x, first_encode_elem_y, 0, 0))
    #     indexLabel.setStyleSheet("font-weight: bold; border: 1px solid black")
    #     indexLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
    #     indexLabel.setCursor(QCursor(Qt.IBeamCursor))
    #     indexLabel.setParent(self.mainFrameWidget)
    #     indexLabel.show()
    #     # self.animateLabelText(indexLabel, "", "Index: ", duration=1000)
    #
    #     y_end = first_encode_elem_y + self.resultLabelMargin + first_encode_elem_height
    #     anim = QPropertyAnimation(indexLabel, b"geometry")
    #     anim.setEndValue(QRect(first_encode_elem_x, y_end,
    #                            int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
    #     #anim.setEndValue(QRect(first_encode_elem_x, first_encode_elem_y+100, int(indexLabel.sizeHint().width()*2), int(indexLabel.sizeHint().height()*2)))
    #     speed = int(self.speedFactor*500)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #     anim_group.finished.connect(self.toggleButtons)
    #     #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     anim_group.start()
    #
    #     #self.tableFinalIndex.append(indexLabel)
    #     self.resultLabel['index'] = indexLabel
    #
    #
    #
    # def selectIndex(self, row, direction, start_color, end_color):
    #     if direction == 'next':
    #         previous = row-1
    #     if direction == 'prev':
    #         previous = row+1
    #         print("Prev Select Index Step: " + str(row))
    #
    #
    #     for i in range(len(self.tableSort)):
    #         for label in self.tableSort[i]:
    #             if(i == row):
    #                 self.animateBackgroundColor(label, start_color, end_color, duration=500)
    #             elif(i == previous):
    #                 self.animateBackgroundColor(label, end_color, start_color, duration=500)
    #
    #
    #
    #
    # def showIndex(self, row):
    #     self.toggleButtons()
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #
    #     table = self.tableSort[row]
    #     firstLabel = table[0]
    #     entry_y = firstLabel.geometry().y()
    #     entry_x = firstLabel.geometry().x()
    #
    #     indexLabel_x = entry_x - self.indexMargin
    #     indexLabel = QLabel(self)
    #     labelText = str(row+1) + ".)"
    #     indexLabel.setText(labelText)
    #     indexLabel.setGeometry(QRect(indexLabel_x, entry_y, 0, 0))
    #     indexLabel.setAlignment(Qt.AlignCenter)
    #     indexLabel.setParent(self.mainFrameWidget)
    #     indexLabel.show()
    #
    #     anim = QPropertyAnimation(indexLabel, b"geometry", self)
    #     #        anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
    #     #                               indexLabel.sizeHint().height()))
    #     anim.setEndValue(QRect(indexLabel.geometry().x(), indexLabel.geometry().y(), indexLabel.sizeHint().width(),
    #                            self.labelHeight))
    #     print(str(indexLabel.geometry().x()), str(indexLabel.geometry().y()), str(indexLabel.sizeHint().width()),
    #           str(indexLabel.sizeHint().height()))
    #     speed = int(500*self.speedFactor)
    #     anim.setDuration(speed)
    #     anim.finished.connect(self.toggleButtons)
    #     #anim.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     anim.start()
    #
    #     self.tableIndex.append(indexLabel)
    #
    #
    # def selectLastChar(self, row_index):
    #     self.toggleButtons()
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #
    #     table = self.tableSort[row_index]
    #     lastLabel = table[-1]
    #
    #     lastChar = QLabel(self)
    #     lastChar.setAlignment(Qt.AlignCenter)
    #     #print("Set Text: " + str(lastLabel.text()))
    #     lastChar.setText(lastLabel.text())
    #     lastChar.setStyleSheet("background-color:red; color: white;")
    #     lastChar.resize(self.labelWidth, self.labelHeight)
    #     lastChar.move(lastLabel.geometry().x(), lastLabel.geometry().y())
    #     lastChar.setParent(self.mainFrameWidget)
    #     lastChar.show()
    #     print(str(lastLabel.geometry().x()), str(lastLabel.geometry().y()))
    #
    #     tableIndexHalf = round(len(self.tableSort)/2)
    #     tableEntryHalf = self.tableSort[tableIndexHalf]
    #     labelHalf = tableEntryHalf[0]
    #
    #     #labelHalf_y = labelHalf.geometry().y()
    #     labelHalf_y = round(self.right_box_height / 2)
    #     if(len(self.tableEncode) == 0):
    #         lastChar_x_end = self.right_box_x_start
    #     else:
    #         prev_last = self.tableEncode[-1]
    #         lastChar_x_end = self.labelWidth + self.labelMargin + prev_last.geometry().x()
    #
    #     #lastChar_x_end = (self.right_box_x_start + self.labelMargin) * self.step
    #     #lastChar_x_end = (self.right_box_x_start + ((self.labelMargin + self.labelWidth) * self.step) + self.labelMargin)
    #     #lastChar_x_end = lastChar.geometry().x() + 150 + (self.step * (lastChar.geometry().width() + 5))
    #     print(str(lastChar_x_end), str(labelHalf_y))
    #     #anim_group = QSequentialAnimationGroup(self)
    #
    #     anim_group = QSequentialAnimationGroup(self)
    #
    #     anim = QPropertyAnimation(lastChar, b"geometry", self)
    #     anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), int(lastChar.geometry().width()*1.3),
    #                            int(lastChar.geometry().height()*1.3)))
    #     speed = int(self.speedFactor * 50)
    #     anim.setDuration(speed)
    #
    #     anim_group.addAnimation(anim)
    #
    #     anim = QPropertyAnimation(lastChar, b"geometry", self)
    #     anim.setEndValue(QRect(lastChar.geometry().x(), lastChar.geometry().y(), self.labelWidth, self.labelHeight))
    #     speed = int(self.speedFactor * 50)
    #     anim.setDuration(speed)
    #
    #     anim_group.addAnimation(anim)
    #
    #     anim = QPropertyAnimation(lastChar, b"pos", self)
    #     anim.setEndValue(QPoint(lastChar_x_end, labelHalf_y))
    #     speed = int(350*self.speedFactor)
    #     anim.setDuration(speed)
    #     anim.start()
    #
    #     anim_group.addAnimation(anim)
    #     anim_group.finished.connect(self.toggleButtons)
    #     #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     anim_group.start()
    #
    #     self.animateBackgroundColor(lastChar, QColor("orange"), QColor("red"), duration=5000)
    #     self.tableEncode.append(lastChar)
    #     self.encode = self.encode + lastLabel.text()
    #
    #
    # def selectSortedRow(self, row_index):
    #     self.toggleButtons()
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #
    #     table = self.table[row_index]
    #     copyTable = []
    #     anim_group = QSequentialAnimationGroup(self)
    #
    #     for label in table:
    #         labelCopy = QLabel(self)
    #         labelCopy.setAlignment(Qt.AlignCenter)
    #         labelCopy.setText(str(label.text()))
    #         labelCopy.setStyleSheet("background-color:red; color:white;")
    #         labelCopy.resize(self.labelWidth, self.labelHeight)
    #         labelCopy.move(label.geometry().x(), label.geometry().y())
    #         labelCopy.setParent(self.mainFrameWidget)
    #         labelCopy.show()
    #         copyTable.append(labelCopy)
    #
    #     y_table = self.table[self.step]
    #     y_start = y_table[0].geometry().y()
    #     # y_start = y_label.geometry().y()
    #     first = 1
    #     for label in copyTable:
    #         if first:
    #             x_start = self.middle_box_x_start
    #             first = 0
    #         else:
    #             x_start = x_start + self.labelWidth + self.labelMargin
    #
    #         # x_start = label.geometry().x()
    #         # y_start = label.geometry().y()
    #         # x_end = x_start + self.tableMargin
    #         x_end = x_start + self.labelMargin
    #         anim = QPropertyAnimation(label, b"pos")
    #         anim.setEndValue(QPoint(x_end, y_start))
    #         speed = int(300*self.speedFactor)
    #         anim.setDuration(speed)
    #         anim_group.addAnimation(anim)
    #
    #     anim_group.finished.connect(self.toggleButtons)
    #     #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     anim_group.start()
    #
    #     for label in copyTable:
    #         self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)
    #
    #     self.tableSort.append(copyTable)
    #
    # def rotate(self):
    #     self.toggleButtons()
    #     #self.utils_btn.toggleButtons(self.controlBtnList)
    #
    #     copyTable = []
    #     anim_group = QSequentialAnimationGroup(self)
    #
    #     table = self.table[-1]
    #     for label in table:
    #         labelCopy = QLabel(self)
    #         labelCopy = CustomLabel(self)
    #         labelCopy.setAlignment(Qt.AlignCenter)
    #         labelCopy.setText(str(label.text()))
    #         #labelCopy.setStyleSheet(self.labelStyleCopyInit)
    #         labelCopy.setStyleSheet(sty.getStyle(Style.labelStyleCopyInit))
    #         labelCopy.resize(self.labelWidth, self.labelHeight)
    #         labelCopy.move(label.geometry().x(), label.geometry().y())
    #         labelCopy.setParent(self.mainFrameWidget)
    #         #print(labelCopy.palette().window().color().name())
    #         labelCopy.show()
    #         copyTable.append(labelCopy)
    #
    #     par_anim_group = QParallelAnimationGroup(self)
    #     for label in copyTable:
    #         x_start = label.geometry().x()
    #         y_start = label.geometry().y()
    #         y_end = y_start + (label.geometry().height()*2)
    #         print("y start: " + str(y_start), "y end: " + str(y_end))
    #         self.table_y.append(y_end)
    #         # print(str(x_start), str(y_start))
    #         anim = QPropertyAnimation(label, b"pos")
    #         anim.setEasingCurve(QEasingCurve.OutBounce)
    #         anim.setEndValue(QPoint(x_start, y_end))
    #         speed = int(300*self.speedFactor)
    #         anim.setDuration(speed)
    #         par_anim_group.addAnimation(anim)
    #
    #     par_anim_group.start()
    #     print(str(par_anim_group.state()))
    #     last_label = copyTable[-1]
    #     first_pos = copyTable[0].pos()
    #
    #     anim = QPropertyAnimation(last_label, b"pos")
    #     #anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+100))
    #     anim.setEndValue(QPoint(last_label.geometry().x(), first_pos.y()+self.labelLineMarginDouble))
    #     speed = int(200*self.speedFactor)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #
    #     for i in range(len(copyTable)-2, -1, -1):
    #         label = copyTable[i]
    #         y_start = label.geometry().y()
    #         y_end = y_start + (label.geometry().height()*2)
    #         # y_end = y_start + 50
    #         x_end = copyTable[i+1].geometry().x()
    #         anim = QPropertyAnimation(label, b"pos")
    #         anim.setEndValue(QPoint(x_end, y_end))
    #         speed = int(150*self.speedFactor)
    #         anim.setDuration(speed)
    #         anim_group.addAnimation(anim)
    #
    #     anim = QPropertyAnimation(last_label, b"pos")
    #     #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+100))
    #     anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self.labelLineMarginDouble))
    #     speed = int(400*self.speedFactor)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #
    #     anim = QPropertyAnimation(last_label, b"pos")
    #     #anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+50))
    #     anim.setEndValue(QPoint(first_pos.x(), first_pos.y()+self.labelLineMargin))
    #     speed = int(400 * self.speedFactor)
    #     anim.setDuration(speed)
    #     anim_group.addAnimation(anim)
    #     anim_group.finished.connect(self.toggleButtons)
    #     #print(self.controlBtnList)
    #     #anim_group.finished.connect(self.utils_btn.toggleButtons(self.controlBtnList))
    #     #anim_group.finished.connect(self.utils_btn.toggle)
    #     anim_group.start()
    #
    #     for label in copyTable:
    #         self.animateBackgroundColor(label, QColor("orange"), QColor("red"), duration=2500)
    #
    #     self.tableLast = copyTable.copy()
    #     tableRotated = self.rotateTable(copyTable)
    #     self.table.append(tableRotated)
    #
    #     text_rotate = iText.rotateText(self.textTable.getLastText())
    #     self.textTable.addText(text_rotate)
    #
    # def animateBackgroundColor(self, widget, start_color, end_color, duration=1000):
    #     duration = int(duration*self.speedFactor)
    #     anim = QVariantAnimation(widget, duration=duration, startValue=start_color, endValue=end_color, loopCount=1)
    #     anim.valueChanged.connect(functools.partial(self.setLabelBackground, widget))
    #     anim.start(QAbstractAnimation.DeleteWhenStopped)
    #
    # def setLabelBackground(self, widget, color):
    #     widget.setStyleSheet("background-color: {}; color: white;".format(color.name()))
    #
    # def animateLabelText(self, widget, start_text, end_text, duration=1000):
    #     duration = int(duration*self.speedFactor)
    #     anim = QVariantAnimation(widget, duration=duration, startValue=start_text, endValue=end_text, loopCount=1)
    #     anim.valueChanged.connect(functools.partial(self.setLabelText, widget))
    #     anim.start(QAbstractAnimation.DeleteWhenStopped)
    #
    # def setLabelText(self, widget, text):
    #     widget.setText(text)
    #
    # def setLabelStyle(self, table, style):
    #     for label in table:
    #         label.setStyleSheet(style)
    #


    def createMenu(self):
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)


app = QApplication(sys.argv)
window = Gui()
sys.exit(app.exec())

import sys
import time
import traceback

from model.iText import Text, TextTable
from model import iText
from controller import Utils
from model.Description import DESC
from controller.State import STATE, State
from view.ControlPanel import ControlPanel, ElemKeys, Direction
from controller.Step import Step
from controller.Window import Window
from view.Forward import Forward as f_view
from view.Backwards import Backwards as b_view
from view.ColorSettings import ColorSetting

from PyQt5.QtWidgets import QWidget, QMainWindow, QAction
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, QRect

from view.ColorSettings import ColorType


class ListenerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    valueChanged = pyqtSignal()


class AnimAllListener(QRunnable):
    def __init__(self, func, *args):
        super(AnimAllListener, self).__init__()
        self._func = func
        self._args = list[args]
        self._signals = ListenerSignals()

    def run(self):
        try:
            while(self._func.getAnimCounter() == 0):
                time.sleep(0.001)
            while(self._func.getAnimCounter() > 0):
                time.sleep(0.001)

        except:
            traceback.print_exc()
        finally:
            #print("Finished")
            self._signals.finished.emit()


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
        self._threadpool = QThreadPool()
        self._animation_finished = 0
        self.initUI()

    #################### HELPER ####################

    def resetWindow(self):
        childs = self.mainFrameWidget.children()
        for child in childs:
            print(child.objectName())
            if child.objectName() == 'Content':
                child.deleteLater()

    def isDeleted(self, widget):
        try:
            widget.objectName()
        except:
            return True

        return False

    def updateSpeed(self, content):
        factor = ((self.speed_slider.value() / 5) ** -1)
        content.updateSpeed(factor)

    #################### INIT GUI ####################

    def initUI(self):
        self.createMenu()
        self.initWindow()
        self.controlPanel = ControlPanel(self)
        self.controlPanel.setObjectName('ControlPanel')
        self.controlPanel.setGeo(QRect(0, self.menu_bar_height, self.win.getWindowWidth(),
                                       int(self.win.getWindowHeight()*0.1)))
        self.controlPanel.setParent(self.mainFrameWidget)

        self.controlPanel.connectBtnOnClick(ElemKeys.transform_button, self.transform)
        self.controlPanel.show()

        self.speed_slider = self.controlPanel.getElem(ElemKeys.speed_slider)

        self._color_edit_btn = self.controlPanel.getElem(ElemKeys.edit_color_button)
        self.controlPanel.connectBtnOnClick(ElemKeys.edit_color_button, self.openColorSetting)
        self._color_setting = ColorSetting()
        self._color_setting.signals.finished.connect(self.settingClosed)

        self._choose_color = self.controlPanel.getElem(ElemKeys.choose_color_combo)

        self.setCentralWidget(self.mainFrameWidget)
        self.show()

    def initWindow(self):
        self.win = Window(self.screen())
        self.window_width = self.win.getWindowWidth()
        self.window_height = self.win.getWindowHeight()
        self.screen_width = self.win.getScreenWidth()
        self.screen_height = self.win.getScreenHeight()
        self.menu_bar_height = self.menuBar().geometry().height()

        self.main_window_x_start = round(self.screen_width/2) - round(self.window_width/2)
        self.main_window_y_start = round(self.screen_height/2) - round(self.window_height/2)

        self.setGeometry(self.main_window_x_start, self.main_window_y_start, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Burrows-Wheeler Transformation")

    def createMenu(self):
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)


    #################### INIT TRANSFORMATION ####################

    def transform(self):
        self._animation_finished = 0
        self.resetWindow()
        next_btn = self.controlPanel.getElem(ElemKeys.next_button)
        prev_btn = self.controlPanel.getElem(ElemKeys.prev_button)
        edit_btn = self.controlPanel.getElem(ElemKeys.edit_color_button)

        input_valid = True
        direction = self.controlPanel.getDirection()
        if direction == Direction.forward.value:

            self._f_input_text = self.controlPanel.getInputText()
            if(len(self._f_input_text) == 0):
                input_valid = False

            if input_valid:
                next_btn.setEnabled(True)
                prev_btn.setEnabled(True)
                edit_btn.setEnabled(True)
                typeList = [ColorType.label.value, ColorType.animation.value, ColorType.select.value, ColorType.found.value]
                self.controlPanel.setColorTypes(typeList)

                self._textTable = TextTable()
                self._textTable.addText(self._f_input_text)
                self._f_result_encode = ""
                self._f_result_index = 0
                self._f_show_index = False

                self._step.reset()
                self._step.setMax(len(self._f_input_text))
                if self.content is not None and not self.isDeleted(self.content):
                    for child in self.content.children():
                        child.deleteLater()

                self.content = f_view(self, self._f_input_text)
                self.content.setObjectName("Content")

                self.updateSpeed(self.content)
                self.content.setWidth(self.win.getWindowWidth())
                self.content.setHeight(self.win.getWindowHeight())
                self.content.setStart(0, self.controlPanel.getHeight())
                self.content.setColorSetting(self._color_setting.getColorSettings())
                self.content.initLayout()
                self.content.initForward()

                self.content.setParent(self.mainFrameWidget)
                self.content.show()

                self.state.setState(STATE.F_ROTATION)
                self.controlPanel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self.content)
                self.controlPanel.connectBtnOnClick(ElemKeys.next_button, self.f_next_step)
                self.controlPanel.connectBtnOnClick(ElemKeys.prev_button, self.f_prev_step)
                #self.controlPanel.connectBtnOnClick(ElemKeys.color_apply_button, self.updateColor)
                self._step.printStep()
            else:
                print("No Valid Input")

        if direction == Direction.backwards.value:

            encode = self.controlPanel.getInputText()
            index = self.controlPanel.getIndexText()
            if len(encode) == 0:
                input_valid = False
            elif len(index) == 0:
                input_valid = False

            if input_valid:
                next_btn.setEnabled(True)
                prev_btn.setEnabled(True)
                edit_btn.setEnabled(True)
                typeList = [ColorType.label.value, ColorType.animation.value, ColorType.select.value, ColorType.found.value]
                self.controlPanel.setColorTypes(typeList)

                self._b_index_input = str(int(index)-1)
                self._b_text_input = Text(encode)
                self._b_result = ""
                self._b_index_select_sorted = 0
                self._b_decode_refs = []

                self._step.reset()
                self._step.setMax(len(encode))

                if self.content is not None and not self.isDeleted(self.content):
                    for child in self.content.children():
                        child.deleteLater()

                self.content = b_view(self, encode, self._b_index_input)
                self.updateSpeed(self.content)
                self.content.setColorSetting(self._color_setting.getColorSettings())
                self.content.setGeo(QRect(0, self.controlPanel.getHeight(), self.win.getWindowWidth(), self.win.getWindowHeight()))
                self.content.initLayout()
                self.content.initBackwards()
                self.content.setDescription(DESC.backward_sort)
                self.content.setParent(self.mainFrameWidget)
                self.content.show()

                self.state.setState(STATE.B_INIT)
                self.controlPanel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self.content)
                self.controlPanel.connectBtnOnClick(ElemKeys.next_button, self.b_next_step)
                self.controlPanel.connectBtnOnClick(ElemKeys.prev_button, self.b_prev_step)
                self._step.printStep()
            else:
                print("No Valid Input")

        if direction == Direction.choose.value:
            pass

    #################### COLOR SETTINGS & UPDATE ####################

    def openColorSetting(self):
        type = self._choose_color.currentText()
        self.controlPanel._toggleElem(self.controlPanel.getElem(ElemKeys.choose_color_combo))
        self.controlPanel._toggleElem(self.controlPanel.getElem(ElemKeys.edit_color_button))
        print("Open Color Settings: {}".format(type))
        self._color_setting.signals.valueChanged.connect(self.colorChanged)
        self._color_setting.openSetting(type)
        self._color_setting.show()

    def settingClosed(self):
        self._color_setting.close()
        self.controlPanel._toggleElem(self.controlPanel.getElem(ElemKeys.choose_color_combo))
        self.controlPanel._toggleElem(self.controlPanel.getElem(ElemKeys.edit_color_button))

    def colorChanged(self):
        self.updateColor()

    def updateColor(self):
        self.content.setColorSetting(self._color_setting.getColorSettings())
        type = self._choose_color.currentText()

        if type == ColorType.label.value:
            self.content.updateLabelColor()

        if type == ColorType.select.value:
            self.content.updateSelectColor(self._step.getStep())

        if type == ColorType.found.value:
            self.content.updateSelectFoundColor(self._step.getStep())


    #################### ANIMATION LISTENER ####################

    def animFinished(self):
        self.controlPanel.toggleControlPanelBtn()

    def createAnimCountListener(self, content):
        self.anim_listener = AnimAllListener(content)
        self.anim_listener._signals.finished.connect(self.animFinished)
        self._threadpool.start(self.anim_listener)


    #################### FORWARD STEP LOGIC ####################

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
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.rotate()
                self._textTable.addText(iText.rotateText(self._textTable.getLastText()))

        if(self.state.getState() == STATE.F_SORT):
            self.state.printState()
            if self._step.isMAX():
                self.state.setState(STATE.F_ENCODE)
                self._step.reset()
                self.content.setDescription(DESC.forward_encode)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self._textTable.sortTable()
                row_index = self._textTable.getRef(self._step.getStep())
                self.content.selectSortedRow(row_index, self._step.getStep())

        if(self.state.getState() == STATE.F_ENCODE):
            self.state.printState()
            if self._step.isMAX():
                self.state.setState(STATE.F_INDEX_SHOW)
                self._step.reset()
                self.content.setDescription(DESC.forward_index)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.selectLastChar(self._step.getStep())
                self._f_result_encode = self._f_result_encode + self._textTable.getLastChar(self._step.getStep())

        if(self.state.getState() == STATE.F_INDEX_SHOW):
            self.state.printState()
            if not self._f_show_index:
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                for i in range(self._step.MAX):
                    print(i)
                    self.content.showIndex(i)
                self._f_show_index = True
            else:
                self.state.setState(STATE.F_INDEX_SELECT)
                self._step.reset()

        if(self.state.getState() == STATE.F_INDEX_SELECT):
            self.state.printState()
            if(self._textTable.getSortedTextAtIndex(self._step.getStep()) == self._f_input_text):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.selectIndex(self._step.getStep(), "next", found=True)
                self.state.setState(STATE.F_INDEX_FINAL)
                self.content.setDescription(DESC.forward_end)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.selectIndex(self._step.getStep(), "next", found=False)

        if(self.state.getState() == STATE.F_INDEX_FINAL):
            self.state.printState()
            self.controlPanel.toggleControlPanelBtn()
            self.createAnimCountListener(self.content)
            self.content.showFinalEncodeLabel(self._f_result_encode)
            self.controlPanel.toggleControlPanelBtn()
            self.createAnimCountListener(self.content)
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
                self.content.deleteLastTable()
                self._textTable.removeLastText()

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
                self.content.deleteLastTableSorted()

            if (self._step.getStep() < 0):
                self.content.deleteLastTableSorted()
                self.state.setState(STATE.F_ROTATION)
                self._step.setStep((self._step.MAX - 1))
                self.content.setDescription(DESC.forward_rotation)

        elif (self.state.getState() == STATE.F_ENCODE):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            self._f_result_encode = self._f_result_encode[0:-1]

            if (self._step.getStep() >= 0):
                self.content.deleteLastEncodeLabel()

            if (self._step.getStep() < 0):
                self.content.deleteLastEncodeLabel()
                self.state.setState(STATE.F_SORT)
                self._step.setStep((self._step.MAX - 1))
                self.content.setDescription(DESC.forward_sort)

        elif (self.state.getState() == STATE.F_INDEX_SHOW):
            for i in range(self._step.MAX):
                self.state.printState()
                self.content.deleteIndexTable()
                self.state.setState(STATE.F_ENCODE)
                self._step.setStep((self._step.MAX - 1))
                self.content.setDescription(DESC.forward_encode)
                self._f_show_index = False

        elif (self.state.getState() == STATE.F_INDEX_SELECT):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            if (self._step.getStep() >= 0):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.selectIndex(self._step.getStep(), "prev", found=False)

            if (self._step.getStep() < 0):
                self.content.selectIndex(self._step.getStep(), "prev", found=False)
                self.state.setState(STATE.F_INDEX_SHOW)
                self._step.setStep((self._step.MAX - 1))
        elif (self.state.getState() == STATE.F_END):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            self.content.selectIndex(self._step.getStep(), "prev", found=False)
            self.state.setState(STATE.F_INDEX_SELECT)
            self.content.deleteResultLabel()
            self.content.setDescription(DESC.forward_index)


    #################### BACKWARDS STEP LOGIC ####################

    def b_next_step(self):
        if not self._step.isMAX() and self.state.getState() != STATE.B_END:
            self._step.increase()
            self._step.printStep()

            if(self.state.getState() == STATE.B_INIT):
                self.state.printState()
                self._b_text_input.sortText()
                self._step.reset()
                self.state.setState(STATE.B_SORT)

            if(self.state.getState() == STATE.B_SORT):
                self.state.printState()
                if self._step.isMAX():
                    self.state.setState(STATE.B_ITERATE)
                    self._step.reset()
                    self.content.setDescription(DESC.backward_iterate)
                else:
                    index = self._b_text_input.getRef(self._step.getStep())
                    self.controlPanel.toggleControlPanelBtn()
                    self.createAnimCountListener(self.content)
                    self.content.selectSort(index)
                    next_step = self._step.getStep() + 1
                    if next_step == self._step.MAX:
                        self.content.selectNextSortedIndex(int(self._b_index_input), None, 'next')

            if(self.state.getState() == STATE.B_ITERATE):
                self.state.printState()
                self._step.printStep()
                if self._step.isMAX():
                    self.state.setState(STATE.B_SHOW_RESULT)
                    self.content.setDescription(DESC.backward_end)
                else:
                    if self._step.getStep() == 0:
                        self._b_index_select_sorted = self._b_index_input
                        next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                        self.content.selectNextSortedIndex(int(next_step), int(self._b_index_select_sorted), 'next')
                    else:
                        self._b_index_select_sorted = self._b_text_input.getRef(self._b_index_select_sorted)
                        next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                        if int(next_step) != int(self._b_index_input):
                            self.content.selectNextSortedIndex(int(next_step), int(self._b_index_select_sorted), 'next')
                        else:
                            self.content.selectNextSortedIndex(None, int(self._b_index_select_sorted), 'next')

                    self._b_decode_refs.append(self._b_index_select_sorted)
                    self._b_result = self._b_result + self._b_text_input.sortedCharAt(int(self._b_index_select_sorted))
                    self.controlPanel.toggleControlPanelBtn()
                    self.createAnimCountListener(self.content)
                    self.content.selectSortedChar(int(self._b_index_select_sorted))

            if(self.state.getState() == STATE.B_SHOW_RESULT):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimCountListener(self.content)
                self.content.showFinalDecodeLabel(self._b_result)
                self.state.setState(STATE.B_END)

            if(self.state.getState() == STATE.B_END):
                self.state.printState()
                self._step.printStep()

    def b_prev_step(self):
        self.state.printState()
        self._step.printStep()

        if self.state.getState() == STATE.B_SORT:
            self.state.printState()
            if self._step.getStep() >= 0:
                self.content.removeLastSortLabel()

            next_step = self._step.getStep() - 1
            if next_step < 0:
                self._step.setStep(-1)
            else:
                self._step.decrease()
                self._step.printStep()

        if self.state.getState() == STATE.B_ITERATE:
            self.state.printState()
            self._b_result = self._b_result[:-1]
            if len(self._b_decode_refs) > 0:
                if self._step.isMAX():
                    self._b_index_select_sorted = self._b_decode_refs[-1]
                    self.content.selectNextSortedIndex(int(self._b_index_select_sorted), None, 'prev')
                else:
                    self._b_index_select_sorted = self._b_decode_refs[-1]
                    next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                    self.content.selectNextSortedIndex(int(self._b_index_select_sorted), int(next_step), 'prev')
            else:
                self._b_index_select_sorted = self._b_index_input
                self.content.selectNextSortedIndex(None, int(self._b_index_select_sorted), 'prev')

            if len(self._b_decode_refs) > 1:
                self._b_index_select_sorted = self._b_decode_refs[-2]

            if len(self._b_decode_refs) > 0:
                del self._b_decode_refs[-1]

            self.content.removeLastDecodeLabel()

            if self._step.getStep() < 0:
                self.state.setState(STATE.B_SORT)
                self.content.setDescription(DESC.backward_sort)
                self._step.setStep(self._step.MAX-1)
                self.content.removeLastSortLabel()

            self._step.decrease()
            self._step.printStep()

        if self.state.getState() == STATE.B_END:
            self.state.printState()
            self._step.printStep()
            self.content.removeResultLabel()
            self.state.setState(STATE.B_ITERATE)
            self.content.setDescription(DESC.backward_iterate)


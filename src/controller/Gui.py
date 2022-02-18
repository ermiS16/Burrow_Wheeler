import time
import traceback

from model.Text import Text, TextTable
from model import Text
from model.Description import DESC, DescriptionSetting as desc_setting
from controller.State import STATE, State
from view.ControlPanel import ControlPanel, ElemKeys, Direction
from controller.Step import Step
from controller.Window import Window
from view.Forward import Forward as f_view
from view.Backwards import Backwards as b_view
from view.Init import Init as init_view
from view.ColorSettings import ColorSetting
from view.Warning import Warning as warn

from PyQt5.QtWidgets import QWidget, QMainWindow, QAction
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, QRect, QSize, Qt
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
            self._signals.finished.emit()


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainFrameWidget = QWidget(self)
        self._content = None
        self._warning = None

        self._step = Step(0, 0)
        self._step.printStep()
        self._state = State(STATE.INIT)
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
        factor = self._control_panel.getSpeedFactor()
        self._control_panel.updateSpeedInfo()
        content.updateSpeed(factor)

    #################### INIT GUI ####################

    def initUI(self):
        self.createMenu()
        self.initWindow()
        self._control_panel = ControlPanel(self)
        self._control_panel.setObjectName('ControlPanel')
        self._control_panel.setGeo(QRect(0, self._menu_bar_height, self.win.getWindowWidth(),
                                         int(self.win.getWindowHeight()*0.1)))
        self._control_panel.setParent(self.mainFrameWidget)

        self._control_panel.connectBtnOnClick(ElemKeys.transform_button, self.transform)
        self._control_panel.show()


        self._color_edit_btn = self._control_panel.getElem(ElemKeys.edit_color_button)
        self._control_panel.connectBtnOnClick(ElemKeys.edit_color_button, self.openColorSetting)
        self._color_setting = ColorSetting()
        setting_width = self.win.getWindowWidth()*0.15
        setting_height = self.win.getWindowHeight()*0.15
        self._color_setting.resize(QSize(setting_width, setting_height))

        win_half_x = self.win.getWindowWidth()/2
        win_half_y = self.win.getWindowHeight()/2
        setting_half_x = self._color_setting.geometry().width()/2
        setting_half_y = self._color_setting.geometry().height()/2

        x_start = win_half_x - setting_half_x
        y_start = win_half_y - setting_half_y
        self._color_setting.move(x_start, y_start)

        self._color_setting.signals.finished.connect(self.settingClosed)
        self._choose_color = self._control_panel.getElem(ElemKeys.choose_color_combo)

        self._warning = warn(self)

        self._description_setting = desc_setting()
        self._description_setting.loadDescriptions()

        self.clearContent()
        self._content = init_view(self)
        self._content.setGeo(
            QRect(0, self._control_panel.getHeight(), self.win.getWindowWidth(), self.win.getWindowHeight()))
        self._content.setDescription(self._description_setting.getDescription(DESC.init))
        self._content.setParent(self.mainFrameWidget)
        self._content.show()


        self.setCentralWidget(self.mainFrameWidget)
        self.show()

    def initWindow(self):
        self.win = Window(self.screen())
        self._window_width = self.win.getWindowWidth()
        self._window_height = self.win.getWindowHeight()
        self._screen_width = self.win.getScreenWidth()
        self._screen_height = self.win.getScreenHeight()
        self._menu_bar_height = self.menuBar().geometry().height()

        self._main_window_x_start = round(self._screen_width / 2) - round(self._window_width / 2)
        self._main_window_y_start = round(self._screen_height / 2) - round(self._window_height / 2)

        self.setGeometry(self._main_window_x_start, self._main_window_y_start, self._window_width, self._window_height)
        self.setFixedSize(self._window_width, self._window_height)
        self.setWindowTitle("Burrows-Wheeler Transformation")

    def createMenu(self):
        exit_act = QAction('Beenden', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_act)

    def clearContent(self):
        if self._content is not None and not self.isDeleted(self._content):
            for child in self._content.children():
                child.deleteLater()

    #################### INIT TRANSFORMATION ####################

    def transform(self):
        self._animation_finished = 0
        self.resetWindow()
        next_btn = self._control_panel.getElem(ElemKeys.next_button)
        prev_btn = self._control_panel.getElem(ElemKeys.prev_button)
        edit_btn = self._control_panel.getElem(ElemKeys.edit_color_button)

        input_valid = True
        direction = self._control_panel.getDirection()
        if direction == Direction.forward.value:

            self._f_input_text = self._control_panel.getInputText()
            if(len(self._f_input_text) < 3):
                input_valid = False
                self._warning.setWindowTitle("Ungültige Eingabe")
                self._warning.setText("Eingabe muss mindestens 3 Zeichen lang sein")
                self._warning.show()


            if input_valid:
                next_btn.setEnabled(True)
                prev_btn.setEnabled(True)
                edit_btn.setEnabled(True)
                typeList = [ColorType.label.value, ColorType.animation.value, ColorType.select.value, ColorType.found.value]
                self._control_panel.setColorTypes(typeList)

                self._textTable = TextTable()
                self._textTable.addText(self._f_input_text)
                self._f_result_encode = ""
                self._f_result_index = 0
                self._f_show_index = False

                self._step.reset()
                self._step.setMax(len(self._f_input_text))
                self.clearContent()

                self._content = f_view(self, self._f_input_text)
                self._content.setObjectName("Content")

                self.updateSpeed(self._content)
                self._content.setColorSetting(self._color_setting.getColorSettings())
                self._content.setGeo(QRect(0, self._control_panel.getHeight(), self.win.getWindowWidth(), self.win.getWindowHeight()))
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_rotation))
                self._content.setParent(self.mainFrameWidget)
                self._content.show()

                self._state.setState(STATE.F_ROTATION)
                self._control_panel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self._content)
                self._control_panel.connectBtnOnClick(ElemKeys.next_button, self.f_next_step)
                self._control_panel.connectBtnOnClick(ElemKeys.prev_button, self.f_prev_step)
                self._step.printStep()
            else:
                pass

        if direction == Direction.backwards.value:

            encode = self._control_panel.getInputText()
            index = self._control_panel.getIndexText()

            if len(encode) == 0:
                input_valid = False
                self._warning.setWindowTitle("Ungültige Eingabe")
                self._warning.setText("Eingabe muss mindestens 3 Zeichen lang sein")
                self._warning.show()

            elif len(index) == 0:
                input_valid = False
                self._warning.setWindowTitle("Ungültige Eingabe")
                self._warning.setText("Kein Index angegeben")
                self._warning.show()


            if input_valid:
                next_btn.setEnabled(True)
                prev_btn.setEnabled(True)
                edit_btn.setEnabled(True)
                typeList = [ColorType.label.value, ColorType.animation.value, ColorType.select.value, ColorType.found.value]
                self._control_panel.setColorTypes(typeList)

                self._b_index_input = str(int(index)-1)
                self._b_text_input = Text.Text(encode)
                self._b_result = ""
                self._b_index_select_sorted = 0
                self._b_decode_refs = []

                self._step.reset()
                self._step.setMax(len(encode))

                self.clearContent()

                self._content = b_view(self, encode, self._b_index_input)
                self.updateSpeed(self._content)
                self._content.setColorSetting(self._color_setting.getColorSettings())
                self._content.setGeo(QRect(0, self._control_panel.getHeight(), self.win.getWindowWidth(), self.win.getWindowHeight()))
                self._content.setDescription(self._description_setting.getDescription(DESC.backward_sort))
                self._content.setParent(self.mainFrameWidget)
                self._content.show()

                self._state.setState(STATE.B_INIT)
                self._control_panel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self._content)
                self._control_panel.connectBtnOnClick(ElemKeys.next_button, self.b_next_step)
                self._control_panel.connectBtnOnClick(ElemKeys.prev_button, self.b_prev_step)
                self._step.printStep()
            else:
                pass

        if direction == Direction.choose.value:
            self._warning = warn(self)
            self._warning.setWindowTitle("Keine Richtung")
            self._warning.setText("Bitte Richtung auswählen")
            self._warning.show()

    #################### COLOR SETTINGS & UPDATE ####################

    def openColorSetting(self):
        type = self._choose_color.currentText()
        self._control_panel.toggleElem(self._control_panel.getElem(ElemKeys.choose_color_combo))
        self._control_panel.toggleElem(self._control_panel.getElem(ElemKeys.edit_color_button))
        print("Open Color Settings: {}".format(type))
        self._color_setting.signals.valueChanged.connect(self.colorChanged)
        self._color_setting.openSetting(type)
        self._color_setting.show()

    def settingClosed(self):
        self._color_setting.close()
        self._control_panel.toggleElem(self._control_panel.getElem(ElemKeys.choose_color_combo))
        self._control_panel.toggleElem(self._control_panel.getElem(ElemKeys.edit_color_button))

    def colorChanged(self):
        self.updateColor()

    def updateColor(self):
        self._content.setColorSetting(self._color_setting.getColorSettings())
        type = self._choose_color.currentText()

        if type == ColorType.label.value:
            if self._control_panel.getDirection() == Direction.forward.value:
                if self._state.getState() == STATE.F_INDEX_SELECT:
                    self._content.updateLabelColor(ignore=self._step.getStep())
                else:
                    self._content.updateLabelColor()
            else:
                self._content.updateLabelColor()

        if type == ColorType.select.value:
            if self._control_panel.getDirection() == Direction.forward.value:
                if self._state.getState() == STATE.F_INDEX_SELECT:
                    self._content.updateSelectColor(self._step.getStep())

            if self._control_panel.getDirection() == Direction.backwards.value:
                print("Update Selection Color Backwards")
                next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                print("Index:" + str(next_step))
                self._content.updateSelectColor(next_step)

        if type == ColorType.found.value:
            if self._control_panel.getDirection() == Direction.forward.value:
                if self._state.getState() == STATE.F_END:
                    self._content.updateSelectFoundColor(self._step.getStep())

            if self._control_panel.getDirection() == Direction.backwards.value:
                for i in range(len(self._b_decode_refs)):
                    self._content.updateSelectFoundColor(int(self._b_decode_refs[i]))

    #################### ANIMATION LISTENER ####################

    def animFinished(self):
        self._control_panel.toggleControlPanelBtn()

    def createAnimCountListener(self, content):
        self.anim_listener = AnimAllListener(content)
        self.anim_listener._signals.finished.connect(self.animFinished)
        self._threadpool.start(self.anim_listener)


    #################### FORWARD STEP LOGIC ####################

    def f_next_step(self):
        if not self._step.isMAX() and self._state.getState() != STATE.F_END:
            self._step.increase()
            self._step.printStep()

        if(self._state.getState() == STATE.F_ROTATION):
            self._state.printState()
            if self._step.isMAX():
                self._state.setState(STATE.F_SORT)
                self._step.reset()
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_sort))
                #self._content.setDescription(DESC.forward_sort)
            else:
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.rotate()
                self._textTable.addText(Text.rotateText(self._textTable.getLastText()))

        if(self._state.getState() == STATE.F_SORT):
            self._state.printState()
            if self._step.isMAX():
                self._state.setState(STATE.F_ENCODE)
                self._step.reset()
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_encode))
                #self._content.setDescription(DESC.forward_encode)
            else:
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._textTable.sortTable()
                row_index = self._textTable.getRef(self._step.getStep())
                self._content.selectSortedRow(row_index, self._step.getStep())

        if(self._state.getState() == STATE.F_ENCODE):
            self._state.printState()
            if self._step.isMAX():
                self._state.setState(STATE.F_INDEX_SHOW)
                self._step.reset()
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_index))
                #self._content.setDescription(DESC.forward_index)
            else:
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.selectLastChar(self._step.getStep())
                self._f_result_encode = self._f_result_encode + self._textTable.getLastChar(self._step.getStep())

        if(self._state.getState() == STATE.F_INDEX_SHOW):
            self._state.printState()
            if not self._f_show_index:
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                for i in range(self._step.MAX):
                    self._content.showIndex(i)
                self._f_show_index = True
            else:
                self._state.setState(STATE.F_INDEX_SELECT)
                self._step.reset()

        if(self._state.getState() == STATE.F_INDEX_SELECT):
            self._state.printState()
            if(self._textTable.getSortedTextAtIndex(self._step.getStep()) == self._f_input_text):
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.selectIndex(self._step.getStep(), "next", found=True)
                self._state.setState(STATE.F_INDEX_FINAL)
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_end))
                #self._content.setDescription(DESC.forward_end)
            else:
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.selectIndex(self._step.getStep(), "next", found=False)

        if(self._state.getState() == STATE.F_INDEX_FINAL):
            self._state.printState()
            self._control_panel.toggleControlPanelBtn()
            self.createAnimCountListener(self._content)
            self._content.showFinalEncodeLabel(self._f_result_encode)
            self._control_panel.toggleControlPanelBtn()
            self.createAnimCountListener(self._content)
            self._content.selectFinalIndexLabel(self._step.getStep())
            self._state.setState(STATE.F_END)

        if(self._state.getState() == STATE.F_END):
            self._state.printState()
            self._step.printStep()


    def f_prev_step(self):
        self._step.printStep()
        self._state.printState()

        if (self._state.getState() == STATE.F_ROTATION):
            if (self._step.getStep() > 0):
                self._content.deleteLastTable()
                self._textTable.removeLastText()

            next_step = self._step.getStep() - 1
            if next_step < 0:
                pass
            else:
                self._step.decrease()

        elif (self._state.getState() == STATE.F_SORT):
            self._step.decrease()
            self._step.printStep()
            self._state.printState()

            if (self._step.getStep() >= 0):
                self._content.deleteLastTableSorted()

            if (self._step.getStep() < 0):
                self._content.deleteLastTableSorted()
                self._state.setState(STATE.F_ROTATION)
                self._step.setStep((self._step.MAX - 1))
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_rotation))
                #self._content.setDescription(DESC.forward_rotation)

        elif (self._state.getState() == STATE.F_ENCODE):
            self._step.decrease()
            self._step.printStep()
            self._state.printState()
            self._f_result_encode = self._f_result_encode[0:-1]

            if (self._step.getStep() >= 0):
                self._content.deleteLastEncodeLabel()

            if (self._step.getStep() < 0):
                self._content.deleteLastEncodeLabel()
                self._state.setState(STATE.F_SORT)
                self._step.setStep((self._step.MAX - 1))
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_sort))
                #self._content.setDescription(DESC.forward_sort)

        elif (self._state.getState() == STATE.F_INDEX_SHOW):
            for i in range(self._step.MAX):
                self._state.printState()
                self._content.deleteIndexTable()
                self._state.setState(STATE.F_ENCODE)
                self._step.setStep((self._step.MAX - 1))
                self._content.setDescription(self._description_setting.getDescription(DESC.forward_encode))
                #self._content.setDescription(DESC.forward_encode)
                self._f_show_index = False

        elif (self._state.getState() == STATE.F_INDEX_SELECT):
            self._step.decrease()
            self._step.printStep()
            self._state.printState()
            if (self._step.getStep() >= 0):
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.selectIndex(self._step.getStep(), "prev", found=False)

            if (self._step.getStep() < 0):
                self._content.selectIndex(self._step.getStep(), "prev", found=False)
                self._state.setState(STATE.F_INDEX_SHOW)
                self._step.setStep((self._step.MAX - 1))
        elif (self._state.getState() == STATE.F_END):
            self._step.decrease()
            self._step.printStep()
            self._state.printState()
            self._content.selectIndex(self._step.getStep(), "prev", found=False)
            self._state.setState(STATE.F_INDEX_SELECT)
            self._content.deleteResultLabel()
            self._content.setDescription(self._description_setting.getDescription(DESC.forward_index))
            #self._content.setDescription(DESC.forward_index)


    #################### BACKWARDS STEP LOGIC ####################

    def b_next_step(self):
        if not self._step.isMAX() and self._state.getState() != STATE.B_END:
            self._step.increase()
            self._step.printStep()

            if(self._state.getState() == STATE.B_INIT):
                self._state.printState()
                self._b_text_input.sortText()
                self._step.reset()
                self._state.setState(STATE.B_SORT)

            if(self._state.getState() == STATE.B_SORT):
                self._state.printState()
                if self._step.isMAX():
                    self._state.setState(STATE.B_ITERATE)
                    self._step.reset()
                    self._content.setDescription(self._description_setting.getDescription(DESC.backward_iterate))
                    #self._content.setDescription(DESC.backward_iterate)
                else:
                    index = self._b_text_input.getRef(self._step.getStep())
                    self._control_panel.toggleControlPanelBtn()
                    self.createAnimCountListener(self._content)
                    self._content.selectSort(index)
                    next_step = self._step.getStep() + 1
                    if next_step == self._step.MAX:
                        self._content.selectNextSortedIndex(int(self._b_index_input), None, 'next')

            if(self._state.getState() == STATE.B_ITERATE):
                self._state.printState()
                self._step.printStep()
                if self._step.isMAX():
                    self._state.setState(STATE.B_SHOW_RESULT)
                    self._content.setDescription(self._description_setting.getDescription(DESC.backward_end))
                    #self._content.setDescription(DESC.backward_end)
                else:
                    if self._step.getStep() == 0:
                        self._b_index_select_sorted = self._b_index_input
                        next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                        self._content.selectNextSortedIndex(int(next_step), int(self._b_index_select_sorted), 'next')
                    else:
                        self._b_index_select_sorted = self._b_text_input.getRef(self._b_index_select_sorted)
                        next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                        if int(next_step) != int(self._b_index_input):
                            self._content.selectNextSortedIndex(int(next_step), int(self._b_index_select_sorted), 'next')
                        else:
                            self._content.selectNextSortedIndex(None, int(self._b_index_select_sorted), 'next')

                    self._b_decode_refs.append(self._b_index_select_sorted)
                    self._b_result = self._b_result + self._b_text_input.sortedCharAt(int(self._b_index_select_sorted))
                    self._control_panel.toggleControlPanelBtn()
                    self.createAnimCountListener(self._content)
                    self._content.selectSortedChar(int(self._b_index_select_sorted))

            if(self._state.getState() == STATE.B_SHOW_RESULT):
                self._control_panel.toggleControlPanelBtn()
                self.createAnimCountListener(self._content)
                self._content.showFinalDecodeLabel(self._b_result)
                self._state.setState(STATE.B_END)

            if(self._state.getState() == STATE.B_END):
                self._state.printState()
                self._step.printStep()

    def b_prev_step(self):
        self._state.printState()
        self._step.printStep()

        if self._state.getState() == STATE.B_SORT:
            self._state.printState()
            if self._step.getStep() >= 0:
                self._content.removeLastSortLabel()

            next_step = self._step.getStep() - 1
            if next_step < 0:
                self._step.setStep(-1)
            else:
                self._step.decrease()
                self._step.printStep()

        if self._state.getState() == STATE.B_ITERATE:
            self._state.printState()
            self._b_result = self._b_result[:-1]
            if len(self._b_decode_refs) > 0:
                if self._step.isMAX():
                    self._b_index_select_sorted = self._b_decode_refs[-1]
                    self._content.selectNextSortedIndex(int(self._b_index_select_sorted), None, 'prev')
                else:
                    self._b_index_select_sorted = self._b_decode_refs[-1]
                    next_step = self._b_text_input.getRef(self._b_index_select_sorted)
                    self._content.selectNextSortedIndex(int(self._b_index_select_sorted), int(next_step), 'prev')
            else:
                self._b_index_select_sorted = self._b_index_input
                self._content.selectNextSortedIndex(None, int(self._b_index_select_sorted), 'prev')

            if len(self._b_decode_refs) > 1:
                self._b_index_select_sorted = self._b_decode_refs[-2]

            if len(self._b_decode_refs) > 0:
                del self._b_decode_refs[-1]

            self._content.removeLastDecodeLabel()

            if self._step.getStep() < 0:
                self._state.setState(STATE.B_SORT)
                self._content.setDescription(self._description_setting.getDescription(DESC.backward_sort))
                #self._content.setDescription(DESC.backward_sort)
                self._step.setStep(self._step.MAX-1)
                self._content.removeLastSortLabel()

            self._step.decrease()
            self._step.printStep()

        if self._state.getState() == STATE.B_END:
            self._state.printState()
            self._step.printStep()
            self._content.deleteResultLabel()
            self._state.setState(STATE.B_ITERATE)
            self._content.setDescription(self._description_setting.getDescription(DESC.backward_iterate))
            #self._content.setDescription(DESC.backward_iterate)


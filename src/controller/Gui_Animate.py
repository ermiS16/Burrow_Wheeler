import sys
import time
import traceback

from gui.Errno import Warnings
from data.iText import Text, TextTable
from gui import Utils
from data.Description import DESC
from gui.State import STATE, State
from gui.ControlPanel import ControlPanel, ElemKeys, Direction
from gui.Step import Step
from gui.Window import Window
from logic.Forward import Forward as f_view
from logic.Backwards import Backwards as b_view

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, QRect


class AnimListenerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)


class AnimAllListener(QObject):
    def __init__(self, func, *args):
        super(AnimListener, self).__init__()
        self._func = func
        self._args = list[args]
        self._signals = AnimListenerSignals()

    def run(self):
        try:
            while(self._func.getAnimAll() != 2):
                time.sleep(0.001)
            while(self._func.getAnimAll() == 2):
                time.sleep(0.001)
        except:
            traceback.print_exc()
        finally:
            print("Finished")
            self._signals.finished.emit()

class AnimListener(QRunnable):
    def __init__(self, func, *args):
        super(AnimListener, self).__init__()
        self._func = func
        self._args = list[args]
        self._signals = AnimListenerSignals()

    def run(self):
        t1 = time.time()
        try:
            while(self._func.getAnim() != 2):
                time.sleep(0.001)
            while(self._func.getAnim() == 2):
                time.sleep(0.001)
        except:
            traceback.print_exc()
        finally:
            print("Finished")
            self._signals.finished.emit()

class AnimGroupListener(QRunnable):
    def __init__(self, func, *args):
        super(AnimGroupListener, self).__init__()
        self._func = func
        self._args = list[args]
        self._signals = AnimListenerSignals()

    def run(self):
        t1 = time.time()
        try:
            while(self._func.getAnimGroup() != 2):
                time.sleep(0.001)
            while(self._func.getAnimGroup() == 2):
                time.sleep(0.001)
        except:
            traceback.print_exc()
        finally:
            print("Finished")
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
       # print(str(childs))
        for child in childs:
            print(child.objectName())
            if child.objectName() == 'Content':
                child.deleteLater()
      #  print(str(childs))

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
        # self.controlPanel.setWidth(self.win.getWindowWidth())
        # self.controlPanel.setHeight((self.win.getWindowHeight()*0.1))
        # self.controlPanel.setY(self.menu_bar_height)
        self.controlPanel.setParent(self.mainFrameWidget)

        self.controlPanel.connectBtnOnClick(ElemKeys.transform_button, self.transform)
        #self.controlPanel.connectBtnOnClick(ElemKeys.reset_button, self.resetWindow)
        self.controlPanel.show()

        self.speed_slider = self.controlPanel.getElem(ElemKeys.speed_slider)



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
        next_btn.setEnabled(True)
        prev_btn.setEnabled(True)

        direction = self.controlPanel.getDirection()
        print(direction)
        if direction == Direction.forward.value:

            input = self.controlPanel.getInputText()
            self._step.reset()
            self._step.setMax(len(input))
            #print(self.mainFrameWidget.children())
            if self.content is not None and not self.isDeleted(self.content):
                for child in self.content.children():
                    child.deleteLater()

            self.content = f_view(self, input)
            self.content.setObjectName("Content")

            self.updateSpeed(self.content)
            self.content.setWidth(self.win.getWindowWidth())
            self.content.setHeight(self.win.getWindowHeight())
            self.content.setStart(0, self.controlPanel.getHeight())
            self.content.initLayout()
            self.content.initForward()
            self.content.setParent(self.mainFrameWidget)
            self.content.show()

            self.state.setState(STATE.F_ROTATION)
            self.controlPanel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self.content)
            self.controlPanel.connectBtnOnClick(ElemKeys.next_button, self.f_next_step)
            self.controlPanel.connectBtnOnClick(ElemKeys.prev_button, self.f_prev_step)
            self._step.printStep()

        if direction == Direction.backwards.value:

            self.controlPanel.setInputText("a!iepdWkii")
            self.controlPanel.setIndexText("2")
            encode = self.controlPanel.getInputText()
            self._b_text_input = Text(encode)
            self._b_index_input = int(self.controlPanel.getIndexText())-1
            self._b_result = ""
            self._b_index_select_sorted = 0
            self._b_decode_refs = []

            self._step.reset()
            self._step.setMax(len(encode))

            if self.content is not None and not self.isDeleted(self.content):
                for child in self.content.children():
                    child.deleteLater()

            self.content = b_view(self, encode, self._b_index_input)
            self.content.setGeo(QRect(0, self.controlPanel.getHeight(), self.win.getWindowWidth(), self.win.getWindowHeight()))
            self.content.setDescription(DESC.backward_sort)
            self.content.setParent(self.mainFrameWidget)
            self.content.show()

            self.state.setState(STATE.B_INIT)
            self.controlPanel.connectSliderOnChange(ElemKeys.speed_slider, self.updateSpeed, self.content)
            self.controlPanel.connectBtnOnClick(ElemKeys.next_button, self.b_next_step)
            self.controlPanel.connectBtnOnClick(ElemKeys.prev_button, self.b_prev_step)
            self._step.printStep()

        if direction == Direction.choose.value:
            pass

    #################### ANIMATION LISTENER ####################

    def animationFinishedAll(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 2:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAllAnimListener(self, content):
        print("Create All Anim Listener")
        self.anim_listener = AnimListener(content)
        self.anim_listener._signals.finished.connect(self.animationFinishedAll)
        self.anim_listener.setAutoDelete(True)

        self.anim_group_listener = AnimGroupListener(content)
        self.anim_group_listener._signals.finished.connect(self.animationFinishedAll)
        self.anim_group_listener.setAutoDelete(True)
        self._threadpool.start(self.anim_listener)
        self._threadpool.start(self.anim_group_listener)

    def animationFinished(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 1:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAnimListener(self, content):
        print("Create Anim Listener")
        anim_listener = AnimListener(content)
        anim_listener._signals.finished.connect(self.animationFinished)
        anim_listener.setAutoDelete(True)
        self._threadpool.start(anim_listener)

    def animationGroupFinished(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 1:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAnimGroupListener(self, content):
        print("Create Anim Group Listener")
        anim_group_listener = AnimListener(content)
        anim_group_listener._signals.finished.connect(self.animationFinished)
        anim_group_listener.setAutoDelete(True)
        self._threadpool.start(anim_group_listener)

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
                self.createAllAnimListener(self.content)
                self.content.rotate()

        if(self.state.getState() == STATE.F_SORT):
            self.state.printState()
            if self._step.isMAX():
                self.state.setState(STATE.F_ENCODE)
                self._step.reset()
                self.content.setDescription(DESC.forward_encode)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAllAnimListener(self.content)
                self.content.sortTextTable()
                row_index = self.content.getTextTableRef(self._step.getStep())
                self.content.selectSortedRow(row_index, self._step.getStep())

        if(self.state.getState() == STATE.F_ENCODE):
            self.state.printState()
            if self._step.isMAX():
                self.state.setState(STATE.F_INDEX_SHOW)
                self._step.reset()
                self.content.setDescription(DESC.forward_index)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAllAnimListener(self.content)
                self.content.selectLastChar(self._step.getStep())

        if(self.state.getState() == STATE.F_INDEX_SHOW):
            self.state.printState()
            for i in range(self._step.MAX+1):
                if i == self._step.MAX:
                    self.state.setState(STATE.F_INDEX_SELECT)
                    self._step.reset()
                else:
                    # self.controlPanel.toggleControlPanelBtn()
                    # self.createAnimListener(self.content)
                    self.content.showIndex(i)

        if(self.state.getState() == STATE.F_INDEX_SELECT):
            self.state.printState()
            if(self.content.getSortedTextAtIndex(self._step.getStep()) == self.content.getInpuText()):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimListener(self.content)
                self.content.selectIndex(self._step.getStep(), "next", QColor("red"), QColor("green"))
                self.state.setState(STATE.F_INDEX_FINAL)
                self.content.setDescription(DESC.forward_end)
            else:
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimListener(self.content)
                self.content.selectIndex(self._step.getStep(), "next", QColor("red"), QColor("blue"))

        if(self.state.getState() == STATE.F_INDEX_FINAL):
            self.state.printState()
            self.controlPanel.toggleControlPanelBtn()
            self.createAnimGroupListener(self.content)
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
                sortedTable = self.content.getSortedTable()
                self.utils_table.deleteLabelList(sortedTable[-1])
                del sortedTable[-1]

            if (self._step.getStep() < 0):
                sortedTable = self.content.getSortedTable()
                self.utils_table.deleteLabelList(sortedTable[-1])
                del sortedTable[-1]
                self.state.setState(STATE.F_ROTATION)
                self._step.setStep((self._step.MAX - 1))
                self.content.setDescription(DESC.forward_rotation)

        elif (self.state.getState() == STATE.F_ENCODE):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()

            if (self._step.getStep() >= 0):
                encodeTable = self.content.getEncodeTable()
                self.utils_table.deleteLastLabel(encodeTable)
                encode = self.content.getEncode()
                encode = encode[0:-1]
                self.content.setEncode(encode)

            if (self._step.getStep() < 0):
                encodeTable = self.content.getEncodeTable()
                self.utils_table.deleteLastLabel(encodeTable)
                self.state.setState(STATE.F_SORT)
                self._step.setStep((self._step.MAX - 1))
                self.content.setDescription(DESC.forward_sort)

        elif (self.state.getState() == STATE.F_INDEX_SHOW):
            for i in range(self._step.MAX):
                self._step.decrease()
                self._step.printStep()
                self.state.printState()
                if (self._step.getStep() >= 0):
                    indexTable = self.content.getIndexTable()
                    self.utils_table.deleteLastLabel(indexTable)

                if (self._step.getStep() < 0):
                    indexTable = self.content.getIndexTable()
                    self.utils_table.deleteLastLabel(indexTable)
                    self.state.setState(STATE.F_ENCODE)
                    self._step.setStep((self._step.MAX - 1))
                    self.content.setDescription(DESC.forward_encode)

        elif (self.state.getState() == STATE.F_INDEX_SELECT):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            if (self._step.getStep() >= 0):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimListener(self.content)
                self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))

            if (self._step.getStep() < 0):
                self.controlPanel.toggleControlPanelBtn()
                self.createAnimListener(self.content)
                self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))
                self.state.setState(STATE.F_INDEX_SHOW)
                self._step.setStep((self._step.MAX - 1))

        elif (self.state.getState() == STATE.F_END):
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))
            self.state.setState(STATE.F_INDEX_SELECT)
            resultLabel = self.content.getResultLabel()
            self.utils_table.deleteDirectoryEntry(resultLabel, 'encode')
            self.utils_table.deleteDirectoryEntry(resultLabel, 'index')
            self.content.setDescription(DESC.forward_index)


    #################### BACKWARDS STEP LOGIC ####################

    def b_next_step(self):
        if not self._step.isMAX() and self.state.getState() != STATE.B_END:
            self._step.increase()
            self._step.printStep()

            if(self.state.getState() == STATE.B_INIT):
                self.state.printState()
                self._b_text_input.sortText()
                #self.content.sortText()
                self._step.reset()
                self.state.setState(STATE.B_SORT)

            if(self.state.getState() == STATE.B_SORT):
                self.state.printState()
                if self._step.isMAX():
                    self.state.setState(STATE.B_ITERATE)
                    self._step.reset()
                    self.content.setDescription(DESC.backward_iterate)
                else:
                    # self.controlPanel.toggleControlPanelBtn()
                    # self.createAllAnimListener(self.content)
                    index = self._b_text_input.getRef(self._step.getStep())
                    self.content.selectSort(index)

            if(self.state.getState() == STATE.B_ITERATE):
                self.state.printState()
                self._step.printStep()
                if self._step.isMAX():
                    self.state.setState(STATE.B_SHOW_RESULT)
                    self._step.reset()
                    self.content.setDescription(DESC.backward_end)
                else:
                    if self._step.getStep() == 0:
                        self._b_index_select_sorted = self._b_index_input
                    else:
                        #self._b_index_select_sorted_prev = self._b_index_select_sorted
                        self._b_index_select_sorted = self._b_text_input.getRef(self._b_index_select_sorted)

                    self._b_decode_refs.append(self._b_index_select_sorted)
                    print(self._b_decode_refs)

                    print(self._b_text_input.getText(), self._b_index_select_sorted)
                    self._b_result = self._b_result + self._b_text_input.sortedCharAt(self._b_index_select_sorted)
                    print(self._b_result)
                    self.content.selectSortedChar(self._b_index_select_sorted)

            if(self.state.getState() == STATE.B_SHOW_RESULT):
                print(self._b_result)
                self.content.showFinalDecodeLabel(self._b_result)
                self.state.setState(STATE.B_END)

            if(self.state.getState() == STATE.B_END):
                self.state.printState()
                self._step.printStep()

    def b_prev_step(self):
        self.state.printState()
        self._step.printStep()

        if self.state.getState() == STATE.B_SORT:
            if self._step.getStep() >= 0:
                self.content.removeLastSortLabel()

            next_step = self._step.getStep() - 1
            print("NEXT STEP: " + str(next_step))
            if next_step < 0:
                self._step.setStep(-1)
            else:
                self._step.decrease()

        if self.state.getState() == STATE.B_ITERATE:
            self._step.decrease()
            self._step.printStep()
            self.state.printState()
            self._b_result = self._b_result[:-1]
            if self._step.getStep() >= 0:
                self.content.removeLastDecodeLabel()
                self._b_index_select_sorted = self._b_decode_refs[-2]
                print(self._b_index_select_sorted)
                del self._b_decode_refs[-1]
                print(self._b_decode_refs)

            if self._step.getStep() < 0:
                self.content.removeLastDecodeLabel()
                self.state.setState(STATE.B_SORT)
                self._step.setStep(self._step.MAX-1)

        if self.state.getState() == STATE.B_END:
            self.state.printState()
            self._step.printStep()
            self.content.removeResultLabel()
            self._step.setStep(self._step.MAX-1)
            self.state.setState(STATE.B_ITERATE)

        print("Prev Step")


app = QApplication(sys.argv)
window = Gui()
sys.exit(app.exec())
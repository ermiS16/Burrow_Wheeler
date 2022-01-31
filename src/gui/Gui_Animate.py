import sys
import time
import traceback

from gui import Utils
from data.Description import DESC
from gui.State import STATE, State
from gui.ControlPanel import ControlPanel, ElemKeys, Direction
from gui.Step import Step
from gui.Window import Window
from logic.Forward import Forward as f_logic

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, QRect


class AnimListenerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)


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

    def resetWindow(self):
        childs = self.mainFrameWidget.children()
        print(str(childs))
        for child in childs:
            print(child.objectName())
            if child.objectName() == 'Content':
                child.deleteLater()
        print(str(childs))

    def isDeleted(self, widget):
        try:
            widget.objectName()
        except:
            return True

        return False

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

    def transform(self):
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
            print(self.mainFrameWidget.children())
            if self.content is not None and not self.isDeleted(self.content):
                for child in self.content.children():
                    child.deleteLater()

            self.content = f_logic(self, input)
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
            pass

        if direction == Direction.choose.value:
            pass

    def updateSpeed(self, content):
        factor = ((self.speed_slider.value() / 5) ** -1)
        content.updateSpeed(factor)

    # def toggleControlPanelBtn(self):
    #     print("Toggle Control Buttons")
    #     next_btn = self.controlPanel.getElem(ElemKeys.next_button)
    #     prev_btn = self.controlPanel.getElem(ElemKeys.prev_button)
    #     transform_btn = self.controlPanel.getElem(ElemKeys.transform_button)
    #     self.utils_btn.toggleButtons([next_btn, prev_btn, transform_btn])

    def animationFinishedAll(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 2:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAllAnimListener(self, content):
        anim_listener = AnimListener(content)
        anim_listener._signals.finished.connect(self.animationFinishedAll)

        anim_group_listener = AnimGroupListener(content)
        anim_group_listener._signals.finished.connect(self.animationFinishedAll)
        self._threadpool.start(anim_listener)
        self._threadpool.start(anim_group_listener)

    def animationFinished(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 1:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAnimListener(self, content):
        anim_listener = AnimListener(content)
        anim_listener._signals.finished.connect(self.animationFinished)
        self._threadpool.start(anim_listener)

    def animationGroupFinished(self):
        self._animation_finished = self._animation_finished + 1
        print("Animation finished: " + str(self._animation_finished))
        if self._animation_finished == 1:
            self.controlPanel.toggleControlPanelBtn()
            self._animation_finished = 0

    def createAnimGroupListener(self, content):
        anim_group_listener = AnimListener(content)
        anim_group_listener._signals.finished.connect(self.animationFinished)
        self._threadpool.start(anim_group_listener)



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
                    self.controlPanel.toggleControlPanelBtn()
                    self.createAnimListener(self.content)
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
            self.createAllAnimListener(self.content)
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
                self.toggleControlPanelBtn()
                self.createAllAnimListener(self.content)
                self.content.selectIndex(self._step.getStep(), "prev", QColor("red"), QColor("blue"))

            if (self._step.getStep() < 0):
                self.toggleControlPanelBtn()
                self.createAllAnimListener(self.content)
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

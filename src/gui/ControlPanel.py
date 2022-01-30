from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QLineEdit, QWidget, QComboBox
from PyQt5.QtCore import QRect, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from enum import Enum

class ElemKeys(Enum):
    input_field = 'input_field'
    delta_field = 'delta_field'
    next_button = 'next_button'
    prev_button = 'prev_button'
    transform_button = 'transform_button'
    speed_slider = 'speed_slider'
    reset_button = 'reset_button'
    direction_box = 'direction_box'

class Direction(Enum):
    forward = "Vorwärts"
    backwards = "Rückärts"
    choose = "Richtung Auswählen"

class ControlPanel(QWidget):
    def __init__(self, arg1):
        super().__init__(arg1)
        self._width = 0
        self._height = 0
        self._x = 0
        self._y = 0
        self._elem = {}
        self._controlBtnList = []
        self.directions = [Direction.choose.value, Direction.forward.value, Direction.backwards.value]
        self.input_field_label = None
        self.input_field = None
        self.transform_button = None
        self.next_button = None
        self.prev_button = None
        self.reset_button = None
        self.speed_slider = None
        self.directionCombo = None
        self.initControlPanel()

    def setWidth(self, width):
        self._width = width
        self.setGeometry(QRect(self.geometry().x(), self.geometry().y(), width, self.geometry().height()))
        self.update()

    def setHeight(self, height):
        self._height = height
        self.setGeometry(QRect(self.geometry().x(), self.geometry().y(), self.geometry().width(), height))
        self.update()

    def update(self):
        self.initControlPanel()

    def getWidth(self):
        return self.geometry().width()

    def getHeight(self):
        return self.geometry().height()

    def x(self):
        return self.geometry().x()

    def y(self):
        return self.geometry().y()

    def setX(self, x):
        self.setGeometry(QRect(x, self.geometry().y(), self.geometry().width(), self.geometry().height()))

    def setY(self, y):
        self.setGeometry(QRect(self.geometry().x(), y, self.geometry().width(), self.geometry().height()))

    def setElem(self, key, value):
        self._elem[key] = value

    def getElem(self, key):
        return self._elem.get(key.value)

    def connectBtnOnClick(self, key, func):
        elem = self.getElem(key)
        elem.disconnect()
        elem.clicked.connect(func)

    def connectSliderOnChange(self, key, func, *args):
        elem = self.getElem(key)
        elem.disconnect()
        elem.valueChanged.connect(lambda: func(*args))

    def connectDirection(self, key, func):
        elem = self.getElem(key)
        elem.disconnect()
        elem.currentTextChanged.connect(func)

    def getBtnList(self):
        return self._controlBtnList

    def getButton(self, key):
        return [btn for btn in self._controlBtnList if btn.objectName() == key.value][0]

    def btnMarginBottom(self):
        return self.button_margin_bottom

    def getInputText(self):
        return self.input_field.text()

    def getDirection(self):
        return self.directionCombo.currentText()

    def initControlPanel(self):

        self.button_width = 100
        self.button_height = 30
        self.button_margin = round(self._width / 120)
        self.button_margin_bottom = self.button_height + round(self._width / 120)



        if self.input_field_label != None:
            self.input_field_label.deleteLater()
            del self.input_field_label

        self.input_field_label = QLabel(self)
        self.input_field_label.setText("Eingabewort:")
        self.input_field_label.move(self._x, self._y)
        self.input_field_label.setParent(self)
        #self.input_field_label.setParent(self.mainFrameWidget)
        #self.input_field_label.show()
        input_field_label_length = self.input_field_label.geometry().width()

        if self.input_field != None:
            self.input_field.deleteLater()
            del self.input_field

        self.input_field = QLineEdit(self)
        self.input_field.setObjectName('input_field')
        input_field_width = self.input_field.geometry().width()
        input_field_x_start = input_field_label_length + (self.button_margin*2)
        self.input_field.move(input_field_x_start, self._y)
        input_text_regex = QRegExp(".{2,15}")
        input_text_validator = QRegExpValidator(input_text_regex)
        self.input_field.setValidator(input_text_validator)
        self.input_field.setPlaceholderText("Input")
        self.input_field.setText("Wikipedia!")

        self.setElem(ElemKeys.input_field.value, self.input_field)

        if self.transform_button != None:
            self.transform_button.deleteLater()
            del self.transform_button

        self.transform_button = QPushButton(self)
        self.transform_button.setObjectName(ElemKeys.transform_button.value)
        self.transform_button.setText("Transformiere")
        self.transform_button_x_start = input_field_width + (self.button_width) + (self.button_margin*4)
        self.transform_button.move(self.transform_button_x_start, self._y)

        self.setElem(ElemKeys.transform_button.value, self.transform_button)

        if self.next_button != None:
            self.next_button.deleteLater()
            del self.next_button

        self.next_button = QPushButton(self)
        self.next_button.setObjectName(ElemKeys.next_button.value)
        self.next_button.setText("Next")
        self.next_button.setEnabled(False)
        next_button_x_start = self._x + (self.button_width*3) + (self.button_margin*3)
        self.next_button.move(next_button_x_start, self._y)

        self.setElem(ElemKeys.next_button.value, self.next_button)

        if self.prev_button != None:
            self.prev_button.deleteLater()
            del self.prev_button

        self.prev_button = QPushButton(self)
        self.prev_button.setObjectName(ElemKeys.prev_button.value)
        self.prev_button.setText("Prev")
        self.prev_button.setEnabled(False)
        prev_x_start = self._x + (self.button_width*4) + (self.button_margin*4)
        self.prev_button.move(prev_x_start, self._y)

        self.setElem(ElemKeys.prev_button.value, self.prev_button)

        if self.reset_button != None:
            self.reset_button.deleteLater()
            del self.reset_button

        self.reset_button = QPushButton(self)
        self.reset_button.setObjectName(ElemKeys.reset_button.value)
        self.reset_button.setText("Reset")
        self.reset_button.setEnabled(True)
        reset_x_start = self._x + (self.button_width*5) + (self.button_margin*5)
        self.reset_button.move(reset_x_start, self._y)
        #self.reset_button.clicked.connect(self.resetWindow)
        #self.reset_button.setParent(self)
        #self.reset_button.setParent(self.mainFrameWidget)

        self.setElem(ElemKeys.reset_button.value, self.reset_button)

        self._controlBtnList.append(self.transform_button)
        self._controlBtnList.append(self.next_button)
        self._controlBtnList.append(self.prev_button)
        self._controlBtnList.append(self.reset_button)

        if self.speed_slider != None:
            self.speed_slider.deleteLater()
            del self.speed_slider

        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setObjectName(ElemKeys.speed_slider.value)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(14)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setValue(7)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        slider_x_start = self._x + (self.button_width*6) + (self.button_margin*6)
        slider_y_start = self._y
        if self._width > 0:
            slider_width = round(self._width / (self._width/200))
        else:
            slider_width = 0
        self.speed_slider.setGeometry(QRect(slider_x_start, self._y, slider_width, self.speed_slider.geometry().height()+5))
        #self.speed_slider.valueChanged.connect(self.updateSpeed)
        #self.speed_slider.setParent(self)
        #self.speed_slider.setParent(self.mainFrameWidget)

        self.setElem(ElemKeys.speed_slider.value, self.speed_slider)

        if self.directionCombo != None:
            self.directionCombo.deleteLater()
            del self.directionCombo

        self.directionCombo = QComboBox(self)
        self.directionCombo.setObjectName(ElemKeys.direction_box.value)
        self.directionCombo.addItems(self.directions)
        #self.mainFrameControlDirection.currentTextChanged.connect(self.switchPage)
        direction_x_start = self._x + (self.button_width*8) + (self.button_margin*8)
        self.directionCombo.move(direction_x_start, self._y)
        #self.directionCombo.setParent(self)
        #self.mainFrameControlDirection.setParent(self.mainFrameWidget)

        self.setElem(ElemKeys.direction_box.value, self.directionCombo)

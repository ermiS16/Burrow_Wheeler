from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QLineEdit, QWidget, QComboBox, QColorDialog, QMessageBox
from PyQt5.QtCore import QRect, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from enum import Enum
from view.ColorSettings import ColorType

class ElemKeys(Enum):
    input_field = 'input_field'
    input_field_label = 'input_field_label'
    delta_field = 'delta_field'
    delta_field_label = 'delta_field_label'
    next_button = 'next_button'
    prev_button = 'prev_button'
    transform_button = 'transform_button'
    speed_slider = 'speed_slider'
    speed_slider_label = 'speed_slider_label'
    speed_info = 'speed_info'
    reset_button = 'reset_button'
    direction_combo = 'direction_box'
    label_color_button = 'label_color_button'
    edit_color_button = 'edit_color_button'
    choose_color_combo = 'choose_color_combo'
    color_apply_button = 'color_apply_button'

class Direction(Enum):
    forward = "Vorwärts"
    backwards = "Rückwärts"
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

        self._directions = [Direction.choose.value, Direction.forward.value, Direction.backwards.value]
        self._colorTypes = [ColorType.label.value, ColorType.animation.value, ColorType.select.value, ColorType.found.value]
        self._input_field_label = None
        self._delta_field_label = None
        self._input_field = None
        self._delta_field = None
        self._transform_button = None
        self._next_button = None
        self._prev_button = None
        self._reset_button = None
        self._speed_slider = None
        self._speed_slider_label = None
        self._speed_info = None
        self._direction_combo = None
        self._label_color_button = None
        self._choose_color = None
        self._edit_color_button = None
        self._color_apply_button = None

        self._COUNT_ELEM_X = 7

        self.initControl()

    def setGeo(self, rect):
        self.setGeometry(rect)
        self._x = rect.x()
        self._y = rect.y()
        self._width = rect.width()
        self._height = rect.height()
        self.update()

    def setWidth(self, width):
        self._width = width
        self.setGeometry(QRect(self.geometry().x(), self.geometry().y(), width, self.geometry().height()))
        self.update()

    def setHeight(self, height):
        self._height = height
        self.setGeometry(QRect(self.geometry().x(), self.geometry().y(), self.geometry().width(), height))
        self.update()

    def update(self):
        self.initControl()

    def getWidth(self):
        return self.geometry().width()

    def getHeight(self):
        return self.geometry().height()

    def setX(self, x):
        self.setGeometry(QRect(x, self.geometry().y(), self.geometry().width(), self.geometry().height()))

    def setY(self, y):
        self.setGeometry(QRect(self.geometry().x(), y, self.geometry().width(), self.geometry().height()))

    def setElem(self, key, value):
        self._elem[key] = value

    def getElem(self, key):
        return self._elem.get(key.value)

    def removeComboBoxItems(self, combo):
        for i in range(combo.count()):
            combo.removeItem(0)

    def setColorTypes(self, typeList):
        self._colorTypes = typeList
        self.removeComboBoxItems(self._choose_color)
        self._choose_color.addItems(typeList)

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

    def toggleControlPanelBtn(self):
        for btn in self._controlBtnList:
            self.toggleElem(btn)

    def toggleDeltaInput(self):
        if self._direction_combo.currentText() == Direction.backwards.value:
            self._delta_field.setEnabled(True)
        else:
            self._delta_field.setEnabled(False)

    def toggleElem(self, elem):
        if elem.isEnabled():
            elem.setEnabled(False)
        else:
            elem.setEnabled(True)

    def getBtnList(self):
        return self._controlBtnList

    def getButton(self, key):
        return [btn for btn in self._controlBtnList if btn.objectName() == key.value][0]

    def getIndexText(self):
        return self._delta_field.text()

    def getInputText(self):
        return self._input_field.text()

    def setInputText(self, input):
        self._input_field.setText(input)

    def setIndexText(self, index):
        self._delta_field.setText(index)

    def getDirection(self):
        return self._direction_combo.currentText()

    def removeControlElement(self, elem):
        if elem != None:
            elem.deleteLater()
            del elem

    def clearControlBtnList(self):
        for btn in self._controlBtnList:
            del btn

        self._controlBtnList = []

    def getSpeedFactor(self):
        print(self._speed_slider.value())
        value = (self._speed_slider.value() / 5)
        return round(value, 2)

    def updateSpeedInfo(self):
        self._speed_info.setText(str(self.getSpeedFactor()) + "x")
        self._speed_info.resize(self._speed_info.sizeHint().width(), self._speed_info.geometry().height())

    def initControl(self):
        self.removeControlElement(self._input_field_label)
        self.removeControlElement(self._input_field)
        self.removeControlElement(self._delta_field_label)
        self.removeControlElement(self._delta_field)
        self.removeControlElement(self._transform_button)
        self.removeControlElement(self._next_button)
        self.removeControlElement(self._prev_button)
        self.removeControlElement(self._speed_slider)
        self.removeControlElement(self._speed_slider_label)
        self.removeControlElement(self._speed_info)
        self.removeControlElement(self._direction_combo)
        self.removeControlElement(self._label_color_button)
        self.removeControlElement(self._color_apply_button)
        self.removeControlElement(self._choose_color)
        self.removeControlElement(self._edit_color_button)
        self.clearControlBtnList()

        self._control_panel_width = self._width
        self._control_panel_height = self._width * 0.1    # (10% von Parent)
        self._control_panel_x = self._x
        self._control_panel_y = self._y

        elem_margin_x = self._control_panel_width * 0.025    # (2% von Parent)
        elem_margin_y = self._control_panel_height * 0.15   # (1% von Parent)

        control_panel_padding_top = self._control_panel_height * 0.01   # (2% von Parent)


        self._input_field_label = QLabel(self)
        self._input_field_label.setObjectName(ElemKeys.delta_field_label.value)
        self._input_field_label.setText("Eingabewort:")
        input_field_label_width = self._input_field_label.geometry().width()

        self._input_field = QLineEdit(self)
        self._input_field.setObjectName(ElemKeys.input_field.value)
        input_text_regex = QRegExp(".{3,15}")
        input_text_validator = QRegExpValidator(input_text_regex)
        self._input_field.setValidator(input_text_validator)
        self._input_field.setPlaceholderText("Input")
        self._input_field.setText("Wikipedia!")
        input_field_width = self._input_field.geometry().width()

        self._delta_field_label = QLabel(self)
        self._delta_field_label.setObjectName(ElemKeys.delta_field_label.value)
        self._delta_field_label.setText("Index:")
        delta_field_label_width = self._delta_field_label.geometry().width()

        self._delta_field = QLineEdit(self)
        self._delta_field.setObjectName(ElemKeys.delta_field.value)
        delta_text_regex = QRegExp("\d{,15}")
        delta_text_validator = QRegExpValidator(delta_text_regex)
        self._delta_field.setValidator(delta_text_validator)
        self._delta_field.setPlaceholderText("Index")
        self._delta_field.setEnabled(False)
        delta_field_width = self._delta_field.geometry().width()

        self._transform_button = QPushButton(self)
        self._transform_button.setObjectName(ElemKeys.transform_button.value)
        self._transform_button.setText("Transformieren")
        transform_btn_width = self._transform_button.geometry().width()

        self._next_button = QPushButton(self)
        self._next_button.setObjectName(ElemKeys.next_button.value)
        self._next_button.setText("Weiter")
        self._next_button.setEnabled(False)
        next_btn_width = self._next_button.geometry().width()

        self._prev_button = QPushButton(self)
        self._prev_button.setObjectName(ElemKeys.prev_button.value)
        self._prev_button.setText("Zurück")
        self._prev_button.setEnabled(False)
        prev_btn_width = self._prev_button.geometry().width()

        self._speed_slider_label = QLabel(self)
        self._speed_slider_label.setText("Geschwindigkeit: ")
        self._speed_slider_label.setObjectName(ElemKeys.speed_slider_label.value)
        speed_slider_label_width = self._speed_slider_label.geometry().width()

        self._speed_info = QLabel(self)
        self._speed_info.setText("1x")
        self._speed_info.setAlignment(Qt.AlignCenter)
        self._speed_info.setObjectName(ElemKeys.speed_info.value)
        speed_info_width = self._speed_info.geometry().width()

        self._speed_slider = QSlider(Qt.Horizontal, self)
        self._speed_slider.setObjectName(ElemKeys.speed_slider.value)
        self._speed_slider.setGeometry(QRect(self._speed_slider.geometry().x(), self._speed_slider.geometry().y(),
                                       int(self._speed_slider.geometry().width()*1.5), int(self._speed_slider.geometry().height()*1.3)))

        self._speed_slider.setMinimum(1)
        self._speed_slider.setMaximum(10)
        self._speed_slider.setValue(5)
        self._speed_slider.setSingleStep(1)
        self._speed_slider.setTickInterval(1)
        self._speed_slider.setTickPosition(QSlider.TicksBelow)
        self._speed_slider.valueChanged.connect(self.updateSpeedInfo)
        speed_slider_width = self._speed_slider.geometry().width()

        self._direction_combo = QComboBox(self)
        self._direction_combo.setObjectName(ElemKeys.direction_combo.value)
        self._direction_combo.addItems(self._directions)
        self._direction_combo.resize(self._direction_combo.sizeHint())
        direction_width = self._direction_combo.geometry().width()

        self._choose_color = QComboBox(self)
        self._choose_color.setObjectName(ElemKeys.choose_color_combo.value)
        self._choose_color.addItems(self._colorTypes)

        self._edit_color_button = QPushButton(self)
        self._edit_color_button.setText("Farbe editieren")
        self._edit_color_button.setEnabled(False)


        elem_all_width = (elem_margin_x * self._COUNT_ELEM_X) + input_field_width + input_field_width + \
                         transform_btn_width + next_btn_width + prev_btn_width + speed_slider_width + direction_width

        elem_all_width_half = elem_all_width / 2
        control_panel_center_x = self._control_panel_width / 2

        x_start = control_panel_center_x - elem_all_width_half
        y_start = self._control_panel_y + control_panel_padding_top
        #print("Input Field Label", x_start, input_field_label_width, elem_margin_x)
        self._input_field_label.move(x_start, y_start)

        x_start = x_start + input_field_label_width + elem_margin_x
        #print("Input Field", x_start, input_field_label_width, elem_margin_x)
        self._input_field.move(x_start, y_start)

        x_start = x_start + input_field_width + elem_margin_x
        #print("Direction", x_start, input_field_width, elem_margin_x)
        self._direction_combo.move(x_start, y_start)

        x_start = x_start + direction_width + elem_margin_x
        #print("Next Button", x_start, direction_width, elem_margin_x)
        self._next_button.move(x_start, y_start)

        x_start = x_start + next_btn_width + elem_margin_x
        #print("Prev Button", x_start, next_btn_width, elem_margin_x)
        self._prev_button.move(x_start, y_start)

        x_start = x_start + prev_btn_width + elem_margin_x
        #print("Speed Slider Label", x_start, prev_btn_width, elem_margin_x)
        self._speed_slider_label.move(x_start, y_start)

        x_start = x_start + speed_slider_label_width + elem_margin_x
        #print("Speed Info", x_start, prev_btn_width, elem_margin_x)
        self._speed_info.move(x_start, y_start)

        x_start = control_panel_center_x - elem_all_width_half
        y_start = y_start + elem_margin_y
        #print("Delta Field Label", x_start, delta_field_label_width, elem_margin_x)
        self._delta_field_label.move(x_start, y_start)

        x_start = x_start + delta_field_label_width + elem_margin_x
        #print("Delta Field", x_start, delta_field_label_width, elem_margin_x)
        self._delta_field.move(x_start, y_start)

        x_start = x_start + delta_field_width + elem_margin_x
        #print("Transform Button", x_start, delta_field_width, elem_margin_x)
        self._transform_button.move(x_start, y_start)

        x_start = self._next_button.geometry().x()
        self._choose_color.move(x_start, y_start)

        x_start = x_start + self._choose_color.geometry().width() + elem_margin_x
        self._edit_color_button.move(x_start, y_start)

        self._direction_combo.model().item(0).setEnabled(False)
        self._direction_combo.currentTextChanged.connect(self.toggleDeltaInput)

        x_start = self._speed_slider_label.geometry().x()
        #print("Speed Slider", x_start, prev_btn_width, elem_margin_x)
        self._speed_slider.move(x_start, y_start)


        self.setElem(ElemKeys.input_field.value, self._input_field)
        self.setElem(ElemKeys.input_field_label.value, self._input_field_label)
        self.setElem(ElemKeys.delta_field.value, self._delta_field)
        self.setElem(ElemKeys.delta_field_label.value, self._delta_field_label)
        self.setElem(ElemKeys.transform_button.value, self._transform_button)
        self.setElem(ElemKeys.next_button.value, self._next_button)
        self.setElem(ElemKeys.prev_button.value, self._prev_button)
        self.setElem(ElemKeys.direction_combo.value, self._direction_combo)
        self.setElem(ElemKeys.speed_slider.value, self._speed_slider)
        self.setElem(ElemKeys.speed_slider_label.value, self._speed_slider_label)
        self.setElem(ElemKeys.speed_info.value, self._speed_info)
        self.setElem(ElemKeys.label_color_button.value, self._label_color_button)
        self.setElem(ElemKeys.choose_color_combo.value, self._choose_color)
        self.setElem(ElemKeys.edit_color_button.value, self._edit_color_button)
        self.setElem(ElemKeys.color_apply_button.value, self._color_apply_button)

        self._controlBtnList.append(self._transform_button)
        self._controlBtnList.append(self._next_button)
        self._controlBtnList.append(self._prev_button)
        self._controlBtnList.append(self._edit_color_button)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        self._color = color.name()
        #print(color.name())

    def getLabelColor(self):
        return self._color

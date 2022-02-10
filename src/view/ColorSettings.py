import traceback
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QThreadPool, QRunnable, QObject
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QColorDialog
from enum import Enum

class ColorType(Enum):
    label = 'Label'
    animation = 'Animation'
    select = 'Selektion'
    found = 'Gefunden'

class Setting(Enum):
    label_background = 'label_background'
    label_text = 'label_text'
    label_style = 'label_style'
    label_animation_background = 'label_animation_background'
    label_animation_text = 'label_animation_text'
    label_animation_style = 'label_animation_style'
    label_select_background = 'label_select_background'
    label_select_text = 'label_select_text'
    label_select_style = 'label_select_style'
    label_select_found_background = 'label_select_found_background'
    label_select_found_text = 'label_select_found_text'
    label_select_found_style = 'label_select_found_style'

class Signals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    valueChanged = pyqtSignal()


class ColorSetting(QWidget):
    def __init__(self):
        super().__init__()
        self._label_background = "red"
        self._label_text = "white"
        self._label_style = self.getStyle(ColorType.label.value)

        self._label_animation_background = "orange"
        self._label_animation_text = "white"
        self._label_animation_style = self.getStyle(ColorType.animation.value)

        self._label_select_background = "blue"
        self._label_select_text = "white"
        self._label_select_style = self.getStyle(ColorType.select.value)

        self._label_select_found_background = "green"
        self._label_select_found_text = "white"
        self._label_select_found_style = self.getStyle(ColorType.select.value)

        self._background_tmp = ""
        self._text_tmp = ""

        self._color_settings = {'label_background': self._label_background, 'label_text': self._label_text,
                                'label_style': self._label_style,
                                'label_animation_background': self._label_animation_background, 'label_animation_text': self._label_animation_text,
                                'label_animation_style': self._label_animation_style,
                                'label_select_background': self._label_select_background, 'label_select_text': self._label_select_text,
                                'label_select_style': self._label_select_style,
                                'label_select_found_background': self._label_select_found_background, 'label_select_found_text': self._label_select_found_text,
                                'label_select_found_style': self._label_select_found_style
                                }

        self._window = None
        self._previewLabel = None
        self._type = None

        self.signals = Signals()

    def openSetting(self, type):
        self._type = type

        if self._window != None:
            self._window.deleteLater()

        self.setWindowTitle("Color Settings")
        self.setGeometry(QRect(0, 0, 500, 500))
        self.loadSettings()


    def loadSettings(self):
        self._info_text = "Text"
        self._info_label = "Hintergrund"

        if self._previewLabel != None:
            self._previewLabel.deleteLater()

        self._previewLabel = QLabel(self)
        self._previewLabel.setText("Text")
        self._previewLabel.setAlignment(Qt.AlignCenter)
        self._previewLabel.setGeometry(QRect(400, 200, 100, 50))
        self.initTempColors()
        style = self.getTempStyle()

        self._previewLabel.setStyleSheet(style)

        background_btn = QPushButton(self)
        background_btn.setText("Hintergrund")
        background_btn.setGeometry(QRect(100, 200, background_btn.geometry().width(), background_btn.geometry().height()))
        background_btn.clicked.connect(lambda: self.setColor('background'))

        text_btn = QPushButton(self)
        text_btn.setText("Text")
        text_btn.setGeometry(QRect(100, 300, text_btn.geometry().width(), text_btn.geometry().height()))
        text_btn.clicked.connect(lambda: self.setColor('text'))

        self._apply_btn = QPushButton(self)
        self._apply_btn.setText("Übernehmen")
        self._apply_btn.setGeometry(QRect(100, 400, self._apply_btn.geometry().width(), self._apply_btn.geometry().height()))
        self._apply_btn.clicked.connect(self.apply)

        self._close_btn = QPushButton(self)
        self._close_btn.setText("Schließen")
        self._close_btn.setGeometry(QRect(200, 400, self._close_btn.geometry().width(), self._close_btn.geometry().height()))
        self._close_btn.clicked.connect(self.emitFinish)


    def getSetting(self, setting):
        return self._color_settings.get(Setting.setting.value)

    def initTempColors(self):
        if self._type == ColorType.label.value:
            self._background_tmp = self._label_background
            self._text_tmp = self._label_text

        if self._type == ColorType.animation.value:
            self._background_tmp = self._label_animation_background
            self._text_tmp = self._label_animation_text

        if self._type == ColorType.select.value:
            self._background_tmp = self._label_select_background
            self._text_tmp = self._label_select_text

        if self._type == ColorType.found.value:
            self._background_tmp = self._label_select_found_background
            self._text_tmp = self._label_select_found_text

    def getColor(self, type):
        if type == ColorType.label.value:
            return (self._label_background, self._label_text)

        if type == ColorType.animation.value:
            return (self._label_animation_background, self._label_animation_text)

        if type == ColorType.select.value:
            return (self._label_select_background, self._label_select_text)

        if type == ColorType.found.value:
            return (self._label_select_found_background, self._label_select_found_text)

        return None

    def getStyle(self, type):
        if type == ColorType.label.value:
            return "background-color: {}; color: {};".format(self._label_background, self._label_text)
        if type == ColorType.animation.value:
            return "background-color: {}; color: {};".format(self._label_animation_background, self._label_animation_text)
        if type == ColorType.select.value:
            return "background-color: {}; color: {};".format(self._label_select_background, self._label_select_text)
        if type == ColorType.found.value:
            return "background-color: {}; color: {};".format(self._label_select_found_background, self._label_select_found_text)

        return None

    def getTempStyle(self):
        return r"background-color: {}; color: {};".format(self._background_tmp, self._text_tmp)

    def getColorSettings(self):
        return self._color_settings

    def updateColorSettings(self):
        print("Update Color Settings")
        self._color_settings[Setting.label_background.value] = self._label_background
        self._color_settings[Setting.label_text.value] = self._label_text
        self._color_settings[Setting.label_style.value] = self._label_style
        self._color_settings[Setting.label_animation_background.value] = self._label_animation_background
        self._color_settings[Setting.label_animation_text.value] = self._label_animation_text
        self._color_settings[Setting.label_animation_style.value] = self._label_animation_style
        self._color_settings[Setting.label_select_background.value] = self._label_select_background
        self._color_settings[Setting.label_select_text.value] = self._label_select_text
        self._color_settings[Setting.label_select_style.value] = self._label_select_style
        self._color_settings[Setting.label_select_found_background.value] = self._label_select_found_background
        self._color_settings[Setting.label_select_found_text.value] = self._label_select_found_text
        self._color_settings[Setting.label_select_found_style.value] = self._label_select_found_style

        print(self._color_settings.get(Setting.label_style.value))
        self.signals.valueChanged.emit()


    def setColor(self, type):
        changed = False
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor().name()
        if type == 'background':
            if self._background_tmp == color:
                changed = True
            self._background_tmp = color
        if type == 'text':
            if self._text_tmp == color:
                changed = True
            self._text_tmp = color

        style = self.getTempStyle()
        self._previewLabel.setStyleSheet(style)
        if changed:
            self._apply_btn.setEnabled(True)

    def apply(self):
        if self._type == ColorType.label.value:
            self._label_background = self._background_tmp
            self._label_text = self._text_tmp
            self._label_style = self.getStyle(self._type)
            print(self._label_style)

        if self._type == ColorType.animation.value:
            self._label_animation_background = self._background_tmp
            self._label_animation_text = self._text_tmp
            self._label_animation_style = self.getStyle(self._type)

        if self._type == ColorType.select.value:
            self._label_select_background = self._background_tmp
            self._label_select_text = self._text_tmp
            self._label_select_style = self.getStyle(self._type)

        if self._type == ColorType.found.value:
            self._label_select_found_background = self._background_tmp
            self._label_select_found_text = self._text_tmp
            self._label_select_found_style = self.getStyle(self._type)

        self.updateColorSettings()

    def emitFinish(self):
        self.signals.finished.emit()

    def closeEvent(self, event):
        print("Close Event")
        if self.signals.finished:
            event.accept()
        else:
            event.ignore()

    def closeSetting(self):
        self.close

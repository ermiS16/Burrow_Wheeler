import functools

from PyQt5.QtCore import QVariantAnimation
from PyQt5.QtWidgets import QWidget


class Content(QWidget):

    def __init__(self, arg1, input):
        super().__init__(self)


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
        text = widget.styleSheet().split(";")[1]
        background = r"background-color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)

    def setLabelText(self, widget, color):
        background = widget.styleSheet().split(";")[0]
        text = r"color: {}".format(color.name())
        style = background + "; " + text + ";"
        widget.setStyleSheet(style)

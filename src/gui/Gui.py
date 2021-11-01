import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel


class Gui:

    def __init__(self, realpart, imgpart):
        self.r = realpart
        self.i = imgpart

    def getRealPart(self):
        return self.r

    def getImgPart(self):
        return self.i

    def f(self):
        return "Lalalala"


x = Gui(3.0, -4.5)
print(x.f())
print(x.getImgPart())
print(x.getRealPart())

app = QApplication([])
label = QLabel(x.f())
label.show()
app.exec()

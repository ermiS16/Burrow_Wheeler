import xml.etree.ElementTree as ET
from enum import Enum, EnumMeta
from PyQt5.QtWidgets import QLabel
from gui.Style import Style

class DESC(Enum):
    forward_rotation = "forward_rotation"
    forward_sort = "forward_sort"
    forward_encode = "forward_encode"
    forward_index = "forward_index"
    forward_end = "forward_end"


class Description(QLabel):

    def __init__(self, text):
        super().__init__(text)
        self._descriptions = {}
        #self._description = desc
        self._loadDescriptions()

    def _loadDescriptions(self):
        tree = ET.parse("/home/eric/Dokumente/Repositories/hska/Burrow_Wheeler/src/data/Descriptions.xml")
        xml_root = tree.getroot()
        for child in xml_root:
            desc = child.text
            self._descriptions[child.tag] = desc.strip()

    def getDescription(self, name):
        info = self._descriptions.get(name)
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        info = info.replace("  ", "")
        return info

    def getAllDesciptions(self):
        return self._descriptions

    def setDescription(self, desc):
        self.removeDescription()
        #self._description.setText(self.getDescription(desc.value))
        self.setText(self.getDescription(desc.value))

    def removeDescription(self):
        #self._description.setText("")
        self.setText("")

    # def setStyleSheet(self, style):
    #     self._description.setStyleSheet(style)
    #
    # def setGeometry(self, geo):
    #     self._description.setGeometry(geo)
    #
    # def setAlignment(self, align):
    #     self._description.setAlignment(align)
    #
    # def setWordWrap(self, bool):
    #     self._description.setWordWrap(bool)
    #
    # def setParent(self, parent):
    #     self._description.setParent(parent)
    #
    # def show(self):
    #     self._description.show()
    #
    # def deleteLater(self):
    #     self._description.deleteLater()


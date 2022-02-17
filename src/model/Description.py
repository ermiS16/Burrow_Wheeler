import os
import xml.etree.ElementTree as ET
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout


class DESC(Enum):
    init = "init"
    forward_rotation = "forward_rotation"
    forward_sort = "forward_sort"
    forward_encode = "forward_encode"
    forward_index = "forward_index"
    forward_end = "forward_end"
    backward_sort = "backward_sort"
    backward_iterate = "backward_iterate"
    backward_end = "backward_end"


class Description(QScrollArea):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.Alignment(Qt.AlignLeft | Qt.AlignTop))

        self.label.setWordWrap(True)

        lay.addWidget(self.label)

        self._descriptions = {}
        self._loadDescriptions()

    def _loadDescriptions(self):

        filename = os.path.join(os.getcwd(), "src/res/Descriptions.xml")
        tree = ET.parse(filename)
        xml_root = tree.getroot()
        for child in xml_root:
            desc = child.text
            self._descriptions[child.tag] = desc.strip()

    def getDescription(self, name):
        info = self._descriptions.get(name)
        #info = info.replace("\n", "")
        #info = info.replace("\t", "")
        info = info.replace("  ", "")
        return info

    def getAllDesciptions(self):
        return self._descriptions

    def setDescription(self, desc):
        self.removeDescription()

        self.label.setText(self.getDescription(desc.value))

        #self.setText(self.getDescription(desc.value))

    def removeDescription(self):
        self.label.setText("")


# class Description(QLabel):
#
#     def __init__(self, text):
#         super().__init__(text)
#         self._descriptions = {}
#         self._loadDescriptions()
#
#     def _loadDescriptions(self):
#
#         filename = os.path.join(os.getcwd(), "src/res/Descriptions.xml")
#         tree = ET.parse(filename)
#         xml_root = tree.getroot()
#         for child in xml_root:
#             desc = child.text
#             self._descriptions[child.tag] = desc.strip()
#
#     def getDescription(self, name):
#         info = self._descriptions.get(name)
#         #info = info.replace("\n", "")
#         #info = info.replace("\t", "")
#         info = info.replace("  ", "")
#         return info
#
#     def getAllDesciptions(self):
#         return self._descriptions
#
#     def setDescription(self, desc):
#         self.removeDescription()
#         self.setText(self.getDescription(desc.value))
#
#     def removeDescription(self):
#         self.setText("")



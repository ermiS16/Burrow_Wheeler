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

class DescriptionSetting:

    def __init__(self):

        self._descriptions = {}
        self.loadDescriptions()

    def loadDescriptions(self):

        filename = os.path.join(os.getcwd(), "src/res/Descriptions.xml")
        tree = ET.parse(filename)
        xml_root = tree.getroot()
        for child in xml_root:
            desc = child.text
            self._descriptions[child.tag] = desc.strip()

    def getDescription(self, name):
        info = self._descriptions.get(name.value)
        info = info.replace("  ", "")
        return info

    def getAllDesciptions(self):
        return self._descriptions

import functools
import re
import sys
import time
import xml.etree.ElementTree as ET
from data import iText
from enum import Enum
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QLineEdit, QHBoxLayout, \
    QVBoxLayout, QBoxLayout, QAction, QComboBox, QScrollArea, QSizePolicy, QCheckBox, QGridLayout, QFormLayout, \
    QStackedLayout, QLayout, QSlider
from PyQt5.QtGui import QFont, QColor, QTextFormat, QRegExpValidator, QIntValidator, QCursor, QPalette
from PyQt5.QtCore import Qt, QSize, QRect, QRegExp, QPropertyAnimation, QPoint, QSequentialAnimationGroup, QEasingCurve, \
    QParallelAnimationGroup, QEvent, pyqtProperty, QVariantAnimation, QAbstractAnimation


class STATE(Enum):
    INIT = 0
    INIT_FORWARD = 1
    INIT_BACKWARD = 2
    F_ROTATION = 3
    F_SORT = 4
    F_ENCODE = 5
    F_INDEX_SHOW = 6
    F_INDEX_SELECT = 7
    F_INDEX_FINAL = 8
    F_END = 9
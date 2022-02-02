from enum import Enum

class Style(Enum):
    labelStyle = 'labelStyle'
    labelStyleCopyInit = 'labelStyleCopyInit'
    labelStyleMarked = 'labelStyleMarked'
    labelStyleSelected = 'labelStyleSelected'
    indexStyleMarked = 'indexStyleMarked'
    indexStyleSelected = 'indexStyleSelected'
    indexStyleSimple = 'indexStyleSimple'
    labelDefaultStyle = 'labelDefaultStyle'
    descriptionStyle = 'descriptionStyle'
    customLabelStyle = 'customLabelStyle'


styles = {
    'labelStyle': r"background-color:red; color:white;",
    'labelStyleCopyInit': "background-color:orange; color:white;",
    'labelStyleMarked': r"background-color:orange; color:white;",
    'labelStyleSelected': r"background-color:green; color:white;",
    'indexStyleMarked': r"background-color:gray; color:black;",
    'indexStyleSelected': r"background-color:green; color:white;",
    'indexStyleSimple': r"background-color:#eff0f1; color:black; border:1px solid black;",
    'labelDefaultStyle': r"background-color: #eff0f1; color:black;",
    'descriptionStyle': r"border: 1px solid black;",
    'customLabelStyle': r"background-color:{}; color:{};"
}

def getStyle(key):
    print(str(styles.get(key.value)))
    return styles.get(key.value)

def updateStyle(key, background, color):
    style = getStyle(Style.labelDefaultStyle)

def setBackgroundColor(color):
    updateStyle("background", color)

def setFontColor(color):
    updateStyle("color", color)


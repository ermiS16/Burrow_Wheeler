from enum import Enum

class Style(Enum):
    labelStyle = 'labelStyle'
    labelStyleCopyInit = 'labelStyleCopyInit'
    labelStyleMarked = 'labelStyleMarked'
    labelStyleSelected = 'labelStyleSelected'
    indexStyleMarked = 'indexStyleMarked'
    indexStyleSelected = 'indexStyleSelected'
    labelDefaultStyle = 'labelDefaultStyle'
    descriptionStyle = 'descriptionStyle'


styles = {
    'labelStyle': r"background-color:red; color:white;",
    'labelStyleCopyInit': "background-color:orange; color.white;",
    'labelStyleMarked': r"background-color:orange; color:white;",
    'labelStyleSelected': r"background-color:green; color:white;",
    'indexStyleMarked': r"backgroud-color:gray; color:black;",
    'indexStyleSelected': r"backgroud-color:green; color:white;",
    'labelDefaultStyle': r"background-color: #eff0f1; color:black;",
    'descriptionStyle': r"border: 1px solid black;"

}

def getStyle(key):
    return styles.get(key.value)

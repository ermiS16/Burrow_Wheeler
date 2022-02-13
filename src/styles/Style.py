from enum import Enum

class Style(Enum):
    descriptionStyle = 'descriptionStyle'
    resultLabelStyle = 'resultLabelStyle'
    infoLabelStyle = 'infoLabelStyle'

styles = {
    'descriptionStyle': r"border: 1px solid black;",
    'resultLabelStyle': r"font-weight: bold; border: 1px solid black;",
    'infoLabelStyle': r"font-weight: bold;",
}

def getStyle(key):
    return styles.get(key.value)

from enum import Enum

class STYLE(Enum):
    descriptionStyle = 'descriptionStyle'
    resultLabelStyle = 'resultLabelStyle'
    infoLabelStyle = 'infoLabelStyle'

styles = {
    'descriptionStyle': "border: 1px solid black;",
    'resultLabelStyle': "font-weight: bold; border: 1px solid black;",
    'infoLabelStyle': "font-weight: bold;"
}

def getStyle(key):
    return styles.get(key.value)

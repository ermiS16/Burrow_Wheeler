def rotateText(text):
    tmp = text[-1]
    text = text[0:len(text)-1]
    text = tmp + text
    return text


class Text:
    def __init__(self, text):
        self._text = text

    def getText(self):
        return self._text

    def getTextLength(self):
        return len(self._text)

    def charAt(self, index):
        return self._text[index]

    def getLastCahr(self):
        return self._text[-1]

    def setText(self, text):
        self._text = text


class TextTable:
    def __init__(self):
        self.table = []
        self.sortedTable = []

    def addText(self, text):
        self.table.append(text)

    def getTextAtIndex(self, index):
        return self.table[index]

    def sortTable(self):
        self.sortedTable = self.table.copy()

    def getSortedTextAtIndex(self, index):
        return self.sortedTable[index]

    def getTextList(self):
        return self.table

    def getTableLength(self):
        return len(self.table)

    def printTable(self):
        print(self.table)
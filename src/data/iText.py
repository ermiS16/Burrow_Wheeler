def rotateText(text):
    tmp = text[-1]
    text = text[0:len(text)-1]
    text = tmp + text
    return text

def getLastChar(text):
    return text[-1]

class Text:
    def __init__(self, text):
        self._text = text
        self._textSorted = ""
        self._sorted_ref_dict = {}

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

    def sortText(self):
        self._textSorted = sorted(self._text)
        textSortedTmp = self._textSorted.copy()
        indices = [i for i, ch in enumerate(self._text) if ch in self._textSorted]
        print(indices)

        for ch in self._text:
            index_sorted = textSortedTmp.index(ch)
            index_rotation = self._text.index(ch)
            self._sorted_ref_dict[index_sorted] = index_rotation
            textSortedTmp[index_sorted] = None

        self.printSortRefDict()

    def getSortedText(self):
        return self._textSorted

    def getRef(self, index):
        return self._sorted_ref_dict[index]

    def printSortRefDict(self):
        for key in self._sorted_ref_dict.keys():
            print("Key: " + str(key) + " | Value: " + str(self._sorted_ref_dict[key]))

class TextTable:
    def __init__(self):
        self.table = []
        self.sortedTable = []
        self.sorted_ref_dict = {}


    def addText(self, text):
        self.table.append(text)

    def getTextAtIndex(self, index):
        return self.table[index]

    def removeTextAtIndex(self, index):
        del self.table[index]

    def removeLastText(self):
        del self.table[-1]

    def getLastText(self):
        return self.table[-1]

    def sortTable(self):
        self.sortedTable = sorted(self.table.copy())
        for entry in self.table:
            index_sorted = self.sortedTable.index(entry)
            index_rotation = self.table.index(entry)
            self.sorted_ref_dict[index_sorted] = index_rotation
        self.printSortRefDict()

    def getSortedTextAtIndex(self, index):
        return self.sortedTable[index]

    def getTextList(self):
        return self.table


    def getRef(self, index):
        return self.sorted_ref_dict[index]

    def getTableLength(self):
        return len(self.table)

    def getTextTable(self):
        return self.table

    def getSortedTable(self):
        return self.table

    def printTable(self):
        print(self.table)

    def printSortRefDict(self):
        for key in self.sorted_ref_dict.keys():
            print("Key: " + str(key) + " | Value: " + str(self.sorted_ref_dict[key]))

    def printSortedTable(self):
        print(self.sortedTable)

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
        # self.printSortedTable()
        # self.printTable()
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


    def printTable(self):
        print(self.table)

    def printSortRefDict(self):
        for key in self.sorted_ref_dict.keys():
            print("Key: " + str(key) + " | Value: " + str(self.sorted_ref_dict[key]))

    def printSortedTable(self):
        print(self.sortedTable)

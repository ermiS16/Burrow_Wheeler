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
        self._text_sorted = ""
        self._sorted_ref_dict = {}

    def getText(self):
        return self._text

    def getTextLength(self):
        return len(self._text)

    def charAt(self, index):
        return self._text[index]

    def sortedCharAt(self, index):
        return self._text_sorted[index]

    def getSortedChar(self, index):
        return self._text_sorted[index]

    def getLastCahr(self):
        return self._text[-1]

    def setText(self, text):
        self._text = text

    def sortText(self):
        self._text_sorted = sorted(self._text)
        text_sorted_tmp = self._text_sorted.copy()
        text_tmp = [ch for ch in self._text]
        pos = 0
        for ch in self._text:
            index_sorted = text_sorted_tmp.index(ch)
            index_rotation = text_tmp.index(ch)
            self._sorted_ref_dict[index_sorted] = index_rotation
            text_sorted_tmp[index_sorted] = None
            text_tmp[index_rotation] = None
            pos = pos + 1
        self.printSortRefDict(self._sorted_ref_dict)


    def getSortedText(self):
        return self._text_sorted

    def getRef(self, index):
        return self._sorted_ref_dict[int(index)]

    def getIndexRef(self, index):
        return self._sorted_index_ref_dict[index]

    def printSortRefDict(self, dir):
        for key in dir.keys():
            print("Key: " + str(key) + " | Value: " + str(self._sorted_ref_dict[key]))

class TextTable:
    def __init__(self):
        self._table = []
        self._sorted_table = []
        self._sorted_ref_dict = {}


    def addText(self, text):
        self._table.append(text)

    def getTextAtIndex(self, index):
        return self._table[index]

    def removeTextAtIndex(self, index):
        del self._table[index]

    def removeLastText(self):
        del self._table[-1]

    def getLastText(self):
        return self._table[-1]

    def sortTable(self):
        self._sorted_table = sorted(self._table.copy())
        for entry in self._table:
            index_sorted = self._sorted_table.index(entry)
            index_rotation = self._table.index(entry)
            self._sorted_ref_dict[index_sorted] = index_rotation
        self.printSortRefDict()

    def getSortedTextAtIndex(self, index):
        return self._sorted_table[index]

    def getLastChar(self, index):
        return self._sorted_table[index][-1]

    def getTextList(self):
        return self._table


    def getRef(self, index):
        return self._sorted_ref_dict[index]

    def getTableLength(self):
        return len(self._table)

    def getTextTable(self):
        return self._table

    def getSortedTable(self):
        return self._table

    def printTable(self):
        print(self._table)

    def printSortRefDict(self):
        for key in self._sorted_ref_dict.keys():
            print("Key: " + str(key) + " | Value: " + str(self._sorted_ref_dict[key]))

    def printSortedTable(self):
        print(self._sorted_table)

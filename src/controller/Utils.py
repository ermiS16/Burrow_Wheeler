class Table:
    def __init__(self):
        pass

    def deleteDirectoryEntry(self, dir, key):
        if key in dir:
            dir[key].deleteLater()
            del dir[key]

    def deleteLastLabel(self, table):
        if len(table) > 0:
            table[-1].deleteLater()
            del table[-1]

    def resetTable(self, table):
        if(len(table) > 0):
            for i in range(len(table)):
                self.deleteLabelList(table[i])

            for list in table:
                del list

    def deleteLabelList(self, list):
        for label in list:
            label.deleteLater()
            del label


    def printLabelTable(self, table):
        content = "["
        for label in table:
            content = content + str(label.text()) + ", "

        content = content[0::-2]
        content = content + "]"


    def rotateTable(self, table):
        last = table[-1]

        for i in range(len(table) - 1, 0, -1):
            table[i] = table[i - 1]

        table[0] = last
        return table


    def rotateTableBack(self, table):
        first = table[0]

        for i in range(0, len(table) - 1, 1):
            table[i] = table[i + 1]

        table[-1] = first

class Button:
    def __init__(self):
        pass

    def toggleButtons(self, btn_list):
        for btn in btn_list:
            self.toggleButton(btn)

    def toggleButton(self, btn):
        if btn.isEnabled():
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

class Label:
    def __init__(self):
        pass

    def setText(self, label, text):
        label.setText(text)




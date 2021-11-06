class Text:
    def __init__(self, text):
        self.text = text
        self.textArray = ()

    def getText(self):
        return self.text

    def charAt(self, index):
        return self.text[index]

    def setText(self, text):
        self.text = text

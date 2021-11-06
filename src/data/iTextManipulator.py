class TextManipulator:

    def rotateText(self, text):
        tmp = text[-1]
        text = text[0:len(text)-1]
        text = tmp + text
        return text

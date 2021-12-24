from gui import Gui
from data import iText
from PyQt5.QtWidgets import QApplication
import sys
import os

if __name__ == '__main__':

    # input_text = "Wikipedia!"
    # print("Input Text: " + input_text)
    #
    # text_length = len(input_text)
    # print("Text Length: " + str(text_length) + "\n")
    # text_rotations = []
    # last_chars = []
    # encoded = ""
    # new_text = input_text
    # text_rotations.append(new_text)
    #
    # for i in range(text_length - 1):
    #     new_text = transform_step(new_text)
    #     text_rotations.append(new_text)
    #
    # print("Rotation: \n")
    # for entry in text_rotations:
    #     print(entry)
    #
    # print("\n")
    #
    # text_rotations = sorted(text_rotations)
    # print("Sorted: \n")
    # for entry in text_rotations:
    #     print(entry)
    #     last_char = entry[-1]
    #     last_chars.append(last_char)
    #
    # print("\n")
    #
    # for entry in last_chars:
    #     encoded = encoded + entry
    #
    # print("Encoded: " + encoded)
    # print(encoded)
    #
    # input_index = text_rotations.index(input_text)
    # print("Index: " + str(input_index))
    # print("\n")

    app = QApplication(sys.argv)
    window = Gui.Gui()
    sys.exit(app.exec())

    # app = Gui.Gui(3, -4.5)
    # x = app.f()
    # print(x)

import os

def rotateText(text):
    tmp = text[-1]
    text = text[0:len(text) - 1]
    text = tmp + text
    return text

def transform_step(text):
    # text_obj = iText.Text(text)
    text = rotateText(text)
    return text

input_text = "Wikipedia"
print("Input Text: " + input_text)

text_length = len(input_text)
#print("Text Length: " + str(text_length) + "\n")
text_rotations = []
last_chars = []
encoded = ""
new_text = input_text
text_rotations.append(new_text)

for i in range(text_length - 1):
    new_text = transform_step(new_text)
    text_rotations.append(new_text)

print("Rotation:")
print(text_rotations)
#  for entry in text_rotations:
#      print(entry)

print("\n")

text_rotations = sorted(text_rotations)
print("Sorted:")
print(text_rotations)
#  for entry in text_rotations:
#     print(entry)
#      last_char = entry[-1]
#      last_chars.append(last_char)

print("\n")

for entry in last_chars:
    encoded = encoded + entry

print("Encoded: " + encoded)

input_index = text_rotations.index(input_text)
print("Index: " + str(input_index))
print("\n")
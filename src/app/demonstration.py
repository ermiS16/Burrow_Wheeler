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

#input_text = r"""Die Burrows-Wheeler-Transformation (kurz: BWT) wird in Datenkompressionsverfahren eingesetzt ohne selber eine Kompression durchzuführen. Im Gegenteil, sie fügt dem Kompressionsverfahren einen Wert hinzu, während die Länge der Eingabe auch gleich die Länge der Ausgabe entspricht. Sie wurde 1994 von Michael Burrows und David Wheeler in einem Technischen Report für digital -- System Research Center vorgestellt. Durch die Eigenschaften der Transformation ist eine effiziente Speicherung der Daten durch anschließende Verfahren möglich. Ein Kompressionsverfahren, dass die BWT verwendet ist bzip2. Dort wird das Ergebnis der Transformation mit dem Move-to-front-Verfahren transformiert und anschließend mit der Huffman-Kodierung komprimiert. Die Theoretischen Grundlagen der Transformationen erläutern die funktionsweise und zeigen auf, weshalb ihr Ergebnis für andere Verfahren relevant ist. Seitens des Autors wurde eine Desktop-Anwendung entwickelt, mit der es möglich ist die Transformation Schritt für Schritt durchzuführen. Die Funktionsweise der Anwendung wird in der Bedienungsanleitung beschrieben. Für weitere Entwicklungen liegt der Dokumentation die Implementierung der Anwendung bei. In dieser werden der Ablauf, Architektur und Schnittstellen beschrieben. Mögliche Ideen zur Weiterentwicklungen werden am Ende der Dokumentation betrachtet."""
#input_text = "Hs-Karlsruhe"
#input_text = "Mississippi"
#input_text = "initialisieren"
input_text = "programmieren"

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

f = open("../Burrow_Wheeler/output/rotations.txt", "w")
for line in text_rotations:
    f.write(line)
    f.write("\n")
f.close()

#print("Rotation:")
#print(text_rotations)
#  for entry in text_rotations:
#      print(entry)

#print("\n")

text_rotations = sorted(text_rotations)
f = open("../Burrow_Wheeler/output/sorted_rotations.txt", "w")
for line in text_rotations:
    f.write(line)
    f.write("\n")
f.close()

#print("Sorted:")
#print(text_rotations)
for entry in text_rotations:
    #print(entry)
    last_char = entry[-1]
    last_chars.append(last_char)

#print("\n")

for entry in last_chars:
    encoded = encoded + entry

f = open("../Burrow_Wheeler/output/encoded.txt", "w")
f.write(encoded)
f.close()
#print("Encoded: " + encoded)

input_index = text_rotations.index(input_text)
#print("Index: " + str(input_index))
#print("\n")
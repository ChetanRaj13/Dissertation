import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

print("=== PDF Page 90 ===")
print(doc[89].get_text())

print("=== PDF Page 91 ===")
print(doc[90].get_text())

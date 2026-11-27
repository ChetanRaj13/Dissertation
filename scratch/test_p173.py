import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')
text = doc[172].get_text() # 0-indexed 172 is PDF page 173
print(f"Length of text on PDF page 173: {len(text)}")
print("Sample text:", repr(text[:500]))

# Also let's check PDF page 174
text174 = doc[173].get_text()
print(f"Length of text on PDF page 174: {len(text174)}")
print("Sample text 174:", repr(text174[:500]))

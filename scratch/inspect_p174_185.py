import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

for pno in range(173, 185):
    page = doc[pno]
    text = page.get_text()
    print(f"Page {pno+1}: len={len(text)}, sample={repr(text[:150])}")

import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

for pno in range(16, 25):
    text = doc[pno].get_text()
    print(f"=== PAGE {pno+1} ===")
    print(text[:1000])

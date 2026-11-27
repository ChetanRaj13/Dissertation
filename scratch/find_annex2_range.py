import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

for pno in range(165, 220):
    text = doc[pno].get_text()
    for line in text.split('\n')[:15]:
        if 'Annexure' in line or 'District' in line or 'DISTRICT' in line or 'State' in line:
            print(f"PDF Page {pno+1}: {line}")

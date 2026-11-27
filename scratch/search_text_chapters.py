import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

for pno in range(15, 60):
    text = doc[pno].get_text()
    if 'stage of extraction' in text.lower() or 'safe' in text.lower():
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        for l in lines:
            if any(k in l.lower() for k in ['categorization', 'stage of extraction', 'overall stage', 'table']):
                print(f"Page {pno+1}: {l}")

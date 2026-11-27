import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# Report page 62 is around PDF page 62 + 28 = 90
for pno in range(80, 100):
    text = doc[pno].get_text()
    if '6.3' in text or '6.4' in text or 'Stage of Ground Water Extraction' in text:
        print(f"=== PDF Page {pno+1} ===")
        print(text[:1500])

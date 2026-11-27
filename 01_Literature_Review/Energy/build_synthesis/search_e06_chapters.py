import fitz

doc = fitz.open('Data Centers in Virginia - JLARC Report 598.pdf')

for p in range(25, 75):
    txt = doc[p].get_text()
    if 'Chapter 3' in txt or 'Chapter 4' in txt:
        print(f"\n--- Page {p+1} ---")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for l in lines[:10]:
            print("  ", l)

import fitz

doc = fitz.open('The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf')
print('E05 total pages:', len(doc))
for p in range(len(doc)):
    txt = doc[p].get_text()
    first_line = txt.strip().split('\n')[0] if txt.strip() else ''
    print(f"Page {p+1}: {len(txt)} chars | starts: {first_line[:80]}")

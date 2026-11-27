import fitz
import re

doc = fitz.open('Data Centers in Virginia - JLARC Report 598.pdf')
print('E06 total pages:', len(doc))

# Search table of contents in first 15 pages
for p in range(min(15, len(doc))):
    txt = doc[p].get_text()
    if 'table of contents' in txt.lower() or 'contents' in txt.lower() or 'summary' in txt.lower():
        print(f"=== Page {p+1} ===")
        for line in txt.split('\n'):
            if any(term in line.lower() for term in ['chapter', 'summary', 'electricity', 'energy', 'grid', 'transmission', 'tax', 'rate', 'infrastructure']):
                print("  ", line.strip())

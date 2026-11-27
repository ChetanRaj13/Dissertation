import fitz

doc = fitz.open('Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf')
print('E07 total pages:', len(doc))

for p in range(min(15, len(doc))):
    txt = doc[p].get_text()
    if 'table of contents' in txt.lower() or 'executive summary' in txt.lower() or 'contents' in txt.lower():
        print(f"=== Page {p+1} ===")
        for line in txt.split('\n')[:15]:
            print("  ", line.strip())

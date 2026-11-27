import fitz

doc = fitz.open('Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf')

for p in range(15, 35):
    txt = doc[p].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    header = lines[0] if lines else ''
    print(f"\n--- E07 Page {p+1}: {header[:60]} ---")
    for l in lines:
        if any(w in l.lower() for w in ['key finding', 'takeaway', 'bill', 'rate', '$/mwh', 'gw', 'mw', 'twh', 'capital', 'increase by', 'percent']):
            if len(l) > 15 and len(l) < 140:
                print("  ", l)

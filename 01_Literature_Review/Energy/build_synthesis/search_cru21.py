import fitz

doc = fitz.open('CRU-21-124 Direction to the System Operators related to Data Centre grid connection.pdf')
print("=== CRU 2021 Direction (CRU/21/124) ===")
for p in range(min(6, len(doc))):
    txt = doc[p].get_text()
    for l in txt.split('\n'):
        if any(w in l.lower() for w in ['direction', 'data centre', 'criterion', 'criteria', 'onsite generation', 'dispatchable', 'location']):
            if len(l.strip()) > 15 and len(l.strip()) < 120:
                print(f"[p.{p+1}] {l.strip()}")

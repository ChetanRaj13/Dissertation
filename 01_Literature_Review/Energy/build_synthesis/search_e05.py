import fitz
import re

doc = fitz.open('The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf')

for p in range(len(doc)):
    txt = doc[p].get_text()
    for line in txt.split('\n'):
        if any(h in line.lower() for h in ['abstract', 'introduction', 'electricity', 'energy', 'carbon', 'power', 'grid', 'table', 'figure', 'conclusion']):
            if len(line.strip()) < 80 and (' ' in line.strip() or len(line.strip()) > 5):
                # potential section or key line
                pass
    # Print key snippets on energy/grid/AI
    matches = re.findall(r'([^.\n]*?(?:electricity|energy|power|TWh|GW|grid|carbon intensity|PUE)[^.\n]*?\.)', txt, re.IGNORECASE)
    print(f"=== PAGE {p+1} ({len(matches)} matches) ===")
    for m in matches[:4]:
        print("  *", m.strip().replace('\n', ' ')[:120])

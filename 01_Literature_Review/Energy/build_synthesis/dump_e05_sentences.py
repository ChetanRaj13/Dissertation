import fitz
import re

doc = fitz.open('The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf')

for p_idx in range(len(doc)):
    p_num = p_idx + 1
    txt = doc[p_idx].get_text()
    # split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', txt)
    print(f"\n--- PAGE {p_num} ---")
    for s in sentences:
        s_clean = " ".join(s.split())
        if any(w in s_clean.lower() for w in ['electricity', 'power', 'twh', 'carbon intensity', 'gco2', 'pue', 'grid', 'scope-2', 'joule', 'iea']):
            if 'water' in s_clean.lower() and not any(w in s_clean.lower() for w in ['electricity', 'twh', 'power', 'carbon', 'pue']):
                continue
            print(f"[{p_num}] {s_clean}")

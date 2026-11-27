import fitz

doc_cru25 = fitz.open('CRU-2025-236 Large Energy User connection policy decision paper.pdf')
# Let's inspect executive summary of CRU 2025 (pages 1 to 10)
print("=== CRU 2025 Executive Summary ===")
for p in range(min(8, len(doc_cru25))):
    txt = doc_cru25[p].get_text()
    for l in txt.split('\n'):
        if any(w in l.lower() for w in ['decision', 'mva', 'generation', 'storage', 'criteria', 'renewable', 'ppa', 'moratorium', 'curtailment', 'large energy user']):
            if len(l.strip()) > 15 and len(l.strip()) < 120:
                print(f"[p.{p+1}] {l.strip()}")

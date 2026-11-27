import fitz
import re

doc = fitz.open('Data Centers in Virginia - JLARC Report 598.pdf')

# Let's inspect page 5 to 15 (Summary) and Chapter 3 (pages 35 to 65)
print("=== Executive Summary key numbers ===")
for p in range(4, 14):
    txt = doc[p].get_text()
    for line in txt.split('\n'):
        if any(term in line.lower() for term in ['gw', 'twh', 'mw', 'percent', '%', 'billion', 'residential', 'rate', 'transmission', 'pjm', 'dominion', 'substation', 'unconstrained']):
            if len(line.strip()) < 120 and len(line.strip()) > 15:
                print(f"[p.{p+1}] {line.strip()}")

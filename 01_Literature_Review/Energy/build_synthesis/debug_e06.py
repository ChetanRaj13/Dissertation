import fitz
import re
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

doc = fitz.open('Data Centers in Virginia - JLARC Report 598.pdf')

failing = [
    (2, 6, "unconstrained demand for power in Virginia would double"),
    (4, 7, "Solar facilities would need to be added at roughly twice the annual rate they were added in 2024"),
    (6, 8, "Both Scenarios 1 and 2 would rely on energy from as yet unproven nuclear technologies"),
    (8, 9, "residential customer of Dominion Energy could experience"),
    (9, 9, "current rates appropriately allocate costs to the industry"),
    (10, 10, "strand utilities with infrastructure costs"),
    (14, 45, "largest new data centers can draw")
]

for row_idx, page_num, exc in failing:
    p_text = doc[page_num - 1].get_text()
    norm_p = normalize_text(p_text)
    norm_e = normalize_text(exc)
    print(f"\nRow {row_idx} (p.{page_num}):")
    if norm_e in norm_p:
        print("  Found prefix!")
    else:
        # search for key words
        first_word = norm_e.split()[0]
        pos = norm_p.find(first_word)
        print("  First word pos:", pos)
        if pos != -1:
            print("  Nearby text:", repr(norm_p[pos:pos+150]))
        else:
            print("  First word not found. Sample of page:", repr(norm_p[:150]))

import fitz
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

doc = fitz.open('Data Centers in Virginia - JLARC Report 598.pdf')

tests = [
    (2, 6, "unconstrained demand for power in Virginia would double"),
    (4, 7, "solar facilities"),
    (6, 8, "Both Scenarios 1 and 2 would rely on energy"),
    (8, 9, "residential customer of Dominion Energy"),
    (9, 9, "study found that current rates"),
    (10, 10, "strand utilities with infrastructure costs"),
    (14, 45, "largest new data centers can draw")
]

for row_idx, page_num, prefix in tests:
    norm_p = normalize_text(doc[page_num - 1].get_text())
    pos = norm_p.find(prefix.lower())
    if pos != -1:
        print(f"\nRow {row_idx} (p.{page_num}):")
        print("  Exact text:", repr(norm_p[pos:pos+200]))
    else:
        print(f"\nRow {row_idx} (p.{page_num}): prefix not found: {prefix}")

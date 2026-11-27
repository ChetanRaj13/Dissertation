import fitz
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

doc = fitz.open("Scaling India's Data Centre Ecosystem - Stakeholder Perspectives on Infrastructure, Energy, and Resilience.pdf")

tests = [
    (2, 4, "80 per cent"),
    (3, 4, "Power-sector incentives"),
    (11, 14, "create pressure on discoms"),
    (13, 15, "physical grid constraints"),
    (18, 21, "dynamic grid")
]

for row_idx, page_num, prefix in tests:
    norm_p = normalize_text(doc[page_num - 1].get_text())
    pos = norm_p.find(prefix.lower())
    if pos != -1:
        print(f"\nRow {row_idx} (p.{page_num}):")
        print("  Exact text:", repr(norm_p[pos-20:pos+160]))
    else:
        print(f"\nRow {row_idx} (p.{page_num}): prefix not found: {prefix}")

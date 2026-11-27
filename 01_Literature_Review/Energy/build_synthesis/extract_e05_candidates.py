import fitz
import re

doc = fitz.open('The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf')

for p_idx in range(len(doc)):
    p_num = p_idx + 1
    txt = doc[p_idx].get_text()
    paras = txt.split('\n\n')
    for para in paras:
        clean = " ".join(para.split())
        # Check if energy/electricity/carbon intensity/grid/PUE mentioned
        if any(w in clean.lower() for w in ['electricity', 'twh', 'power demand', 'carbon intensity', 'pue', 'grid', 'scope-2', 'gco2/kwh']):
            # Filter out paragraphs that are exclusively about water
            print(f"P.{p_num}: {clean[:140]}...")

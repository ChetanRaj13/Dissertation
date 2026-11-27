import fitz
import json
import pandas as pd
import numpy as np

# Open CGWB PDF
doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# 1. Parse Annexure I (PDF page 171)
p171 = doc[170]
words171 = p171.get_text('words')

# Group words by line y-coord
lines171 = {}
for w in words171:
    y = round(w[1], 1)
    found = False
    for yk in lines171:
        if abs(yk - y) < 2.5:
            lines171[yk].append(w)
            found = True
            break
    if not found:
        lines171[y] = [w]

annex1_rows = []
for yk in sorted(lines171.keys()):
    row = sorted(lines171[yk], key=lambda x: x[0])
    # check if row starts with a number (S.No. 1 to 36)
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            # Extract state name and columns
            # Column boundaries from x-coords:
            # S.No: ~30-45
            # State: ~45-135
            # Col 3 (Monsoon rain): ~135-185
            # Col 4 (Monsoon other): ~185-235
            # Col 5 (Non-mon rain): ~235-280
            # Col 6 (Non-mon other): ~280-325
            # Col 7 (Total recharge): ~325-375
            # Col 8 (Natural discharges): ~375-420
            # Col 9 (Extractable): ~420-470
            # Col 10 (Irrigation): ~470-515
            # Col 11 (Industrial): ~515-550
            # Col 12 (Domestic): ~550-590
            # Col 13 (Total extraction): ~590-635
            # Col 14 (Domestic 2030): ~635-680
            # Col 15 (Net availability): ~680-730
            # Col 16 (Stage %): ~730-780
            
            # Words for name: x between 45 and 135
            # But wait, Dadra & Nagar Haveli wraps across multiple lines
            name_words = [w[4] for w in row if 45 <= w[0] < 135]
            name = " ".join(name_words)
            
            # Extract numbers based on x coordinate
            col_extractable = None
            col_extraction_total = None
            col_stage = None
            
            for w in row:
                x = w[0]
                val_str = w[4]
                try:
                    val = float(val_str)
                    if 420 <= x < 470:
                        col_extractable = val
                    elif 590 <= x < 635:
                        col_extraction_total = val
                    elif 730 <= x < 780:
                        col_stage = val
                except ValueError:
                    pass
            
            annex1_rows.append({
                'sno': sno,
                'name_raw': name,
                'extractable_bcm': col_extractable,
                'extraction_total_bcm': col_extraction_total,
                'stage_pct': col_stage,
                'y': yk
            })

print(f"Extracted {len(annex1_rows)} rows from Annexure I")
for r in annex1_rows[:10]:
    print(r)

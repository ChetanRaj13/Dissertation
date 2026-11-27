import fitz
import json
import pandas as pd

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# 1. Annexure I
p171 = doc[170]
words171 = p171.get_text('words')
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

annex1 = {}
for yk in sorted(lines171.keys()):
    if yk <= 135:
        continue
    row = sorted(lines171[yk], key=lambda x: x[0])
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            col_extractable = None
            col_extraction_total = None
            col_stage = None
            for w in row:
                x = w[0]
                try:
                    val = float(w[4])
                    if 420 <= x < 470:
                        col_extractable = val
                    elif 590 <= x < 635:
                        col_extraction_total = val
                    elif 730 <= x < 780:
                        col_stage = val
                except ValueError:
                    pass
            # Name
            name_words = [w[4] for w in row if 45 <= w[0] < 135]
            name = " ".join(name_words)
            annex1[sno] = {
                'sno': sno,
                'name': name,
                'extractable_bcm': col_extractable,
                'extraction_total_bcm': col_extraction_total,
                'stage_pct': col_stage
            }

# Fix Dadra & Nagar Haveli name if truncated
if 31 in annex1:
    annex1[31]['name'] = "Dadra & Nagar Haveli and Daman & Diu"

# 2. Annexure III (A) (PDF page 215)
p215 = doc[214]
words215 = p215.get_text('words')
lines215 = {}
for w in words215:
    y = round(w[1], 1)
    found = False
    for yk in lines215:
        if abs(yk - y) < 2.5:
            lines215[yk].append(w)
            found = True
            break
    if not found:
        lines215[y] = [w]

# In p215, columns are:
# S.No (~20-40)
# State Name (~40-145)
# Total Assessed Units (~145-185)
# Safe Nos (~185-230), Safe % (~230-270)
# Semi-Critical Nos (~270-310), Semi-Critical % (~310-350)
# Critical Nos (~350-390), Critical % (~390-430)
# Over-Exploited Nos (~430-470), Over-Exploited % (~470-510)
# Saline Nos (~510-550), Saline % (~550-590)

annex3a = {}
for yk in sorted(lines215.keys()):
    if yk <= 140:
        continue
    row = sorted(lines215[yk], key=lambda x: x[0])
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            total_units = None
            safe_nos = 0
            safe_pct = 0.0
            sc_nos = 0
            sc_pct = 0.0
            crit_nos = 0
            crit_pct = 0.0
            oe_nos = 0
            oe_pct = 0.0
            sal_nos = 0
            sal_pct = 0.0
            
            for w in row:
                x = w[0]
                try:
                    val = float(w[4])
                    if 145 <= x < 185:
                        total_units = int(val)
                    elif 185 <= x < 230:
                        safe_nos = int(val)
                    elif 230 <= x < 270:
                        safe_pct = val
                    elif 270 <= x < 310:
                        sc_nos = int(val)
                    elif 310 <= x < 350:
                        sc_pct = val
                    elif 350 <= x < 390:
                        crit_nos = int(val)
                    elif 390 <= x < 430:
                        crit_pct = val
                    elif 430 <= x < 470:
                        oe_nos = int(val)
                    elif 470 <= x < 510:
                        oe_pct = val
                    elif 510 <= x < 550:
                        sal_nos = int(val)
                    elif 550 <= x < 590:
                        sal_pct = val
                except ValueError:
                    pass
            
            annex3a[sno] = {
                'sno': sno,
                'total_units': total_units,
                'safe_nos': safe_nos,
                'safe_pct': safe_pct,
                'sc_nos': sc_nos,
                'sc_pct': sc_pct,
                'crit_nos': crit_nos,
                'crit_pct': crit_pct,
                'oe_nos': oe_nos,
                'oe_pct': oe_pct,
                'sal_nos': sal_nos,
                'sal_pct': sal_pct
            }

print(f"Annexure I count: {len(annex1)}, Annexure III(A) count: {len(annex3a)}")

# Print combined table
print(f"{'SNo':<4} | {'State':<28} | {'Extractable':<11} | {'Extraction':<10} | {'Stage%':<7} | {'Total':<5} | {'Safe':<5} | {'SC':<4} | {'Crit':<4} | {'OE':<4} | {'Sal':<4}")
print("-" * 105)
for sno in range(1, 37):
    a1 = annex1.get(sno, {})
    a3 = annex3a.get(sno, {})
    print(f"{sno:<4} | {a1.get('name',''):<28} | {a1.get('extractable_bcm',''):<11} | {a1.get('extraction_total_bcm',''):<10} | {a1.get('stage_pct',''):<7} | {a3.get('total_units',''):<5} | {a3.get('safe_nos',''):<5} | {a3.get('sc_nos',''):<4} | {a3.get('crit_nos',''):<4} | {a3.get('oe_nos',''):<4} | {a3.get('sal_nos',''):<4}")

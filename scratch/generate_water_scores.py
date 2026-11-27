import os
import json
import fitz
import pandas as pd
import numpy as np

# Load energy states to get exact order and DC flags
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')

# Load CGWB PDF
doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# 1. Parse Annexure I (PDF page 171)
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
            name_words = [w[4] for w in row if 45 <= w[0] < 135]
            name = " ".join(name_words)
            annex1[sno] = {
                'sno': sno,
                'name': name,
                'extractable_bcm': col_extractable,
                'extraction_total_bcm': col_extraction_total,
                'stage_pct': col_stage
            }

# 2. Parse Annexure III (A) (PDF page 215)
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

# 3. Load JJM Data
with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_live_list = json.load(f)['d']

jjm_live = {}
for item in jjm_live_list:
    jjm_live[item['Name'].strip()] = item

# Also load offline JJM summaries (28 Oct 2026) for the 13 DC states
with open('DATA/WATER/JAL JEEVAN MISSION (TAP WATER DATA)/jal_jeevan_mission_tap_water_by_district.json', 'r', encoding='utf-8') as f:
    jjm_offline = json.load(f)['state_summaries']

jjm_offline_map = {item['state']: item for item in jjm_offline}

print("JJM offline states loaded:", len(jjm_offline_map))
print("JJM live states loaded:", len(jjm_live))

import pandas as pd
import json

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    nationwide = json.load(f)
df_all = pd.DataFrame(nationwide)

from test_all_29_ranks import res as df_29

dc_states = [
    'Andhra Pradesh', 'Bihar', 'Chhattisgarh', 'Delhi', 'Gujarat',
    'Haryana', 'Karnataka', 'Madhya Pradesh', 'Maharashtra', 'Odisha',
    'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'West Bengal'
]

state_medians = {}
for s in dc_states:
    dist_s = df_all[df_all['state'].str.lower() == s.lower()]
    med = dist_s['stage_of_extraction_pct'].median()
    state_medians[s] = med

above = 0
below = 0
equal = 0
for idx, r in df_29.iterrows():
    st = r['state']
    d_stage = r['stage_pct']
    st_med = state_medians[st]
    diff = round(d_stage - st_med, 2)
    if diff > 0:
        above += 1
        stat = "ABOVE"
    elif diff < 0:
        below += 1
        stat = "BELOW"
    else:
        equal += 1
        stat = "EQUAL"
    print(f"{r['state']:<15} | {r['district']:<20} | dist: {d_stage:<6.2f} | med: {st_med:<6.2f} | diff: {diff:<+6.2f} | {stat}")

print(f"\nTotal Above: {above}, Total Below: {below}, Total Equal: {equal}, Sum: {above+below+equal}")

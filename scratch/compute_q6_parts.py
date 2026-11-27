import json
import pandas as pd
import numpy as np

# Load all 709 districts
with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    nationwide = json.load(f)

df_all = pd.DataFrame(nationwide)

# Define 4 bands based on stage_of_extraction_pct
def get_band(val):
    if val < 70.0:
        return 'Safe (<70%)'
    elif val <= 90.0:
        return 'Semi-Critical (70-90%)'
    elif val <= 100.0:
        return 'Critical (90-100%)'
    else:
        return 'Over-Exploited (>100%)'

df_all['band'] = df_all['stage_of_extraction_pct'].apply(get_band)

print("=== PART (A): SHARE OF ALL 709 DISTRICTS VS 29 HOSTING DISTRICTS ===")
band_order = ['Safe (<70%)', 'Semi-Critical (70-90%)', 'Critical (90-100%)', 'Over-Exploited (>100%)']

# All 709 districts counts and shares
all_counts = df_all['band'].value_counts()
all_shares = (all_counts / len(df_all)) * 100.0

# 29 hosting districts
from test_all_29_ranks import res as df_29
df_29['band'] = df_29['stage_pct'].apply(get_band)
host_counts = df_29['band'].value_counts()
host_shares = (host_counts / len(df_29)) * 100.0

part_a_rows = []
for b in band_order:
    c_all = all_counts.get(b, 0)
    s_all = all_shares.get(b, 0.0)
    c_host = host_counts.get(b, 0)
    s_host = host_shares.get(b, 0.0)
    part_a_rows.append({
        'Band': b,
        'All_Districts_N': c_all,
        'All_Districts_Pct': round(s_all, 2),
        'Hosting_Districts_N': c_host,
        'Hosting_Districts_Pct': round(s_host, 2)
    })

df_part_a = pd.DataFrame(part_a_rows)
print(df_part_a.to_string(index=False))

print("\n=== PART (B): HOSTING DISTRICT STAGE VS STATE MEDIAN DISTRICT ===")
# For each of the 14 DC states:
# Compute state median district stage from df_all
dc_states = [
    'Andhra Pradesh', 'Bihar', 'Chhattisgarh', 'Delhi', 'Gujarat',
    'Haryana', 'Karnataka', 'Madhya Pradesh', 'Maharashtra', 'Odisha',
    'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'West Bengal'
]

state_medians = {}
for s in dc_states:
    dist_s = df_all[df_all['state'].str.lower() == s.lower()]
    med = dist_s['stage_of_extraction_pct'].median()
    mean = dist_s['stage_of_extraction_pct'].mean()
    count = len(dist_s)
    state_medians[s] = {'median': round(med, 2), 'mean': round(mean, 2), 'count': count}
    print(f"State: {s:<18} | Districts in CGWB: {count:<2} | Median: {med:.2f}% | Mean: {mean:.2f}%")

print("\nComparing each of the 29 hosting districts against host state median district:")
part_b_rows = []
for idx, r in df_29.iterrows():
    st = r['state']
    d_name = r['district']
    d_stage = r['stage_pct']
    st_med = state_medians[st]['median']
    diff_from_med = round(d_stage - st_med, 2)
    ratio_to_med = round(d_stage / st_med, 2) if st_med > 0 else 0
    
    status = "Above median" if diff_from_med > 0 else ("Below median" if diff_from_med < 0 else "Equal to median")
    part_b_rows.append({
        'State': st,
        'District': d_name,
        'District_Stage_Pct': d_stage,
        'State_Districts_N': state_medians[st]['count'],
        'State_Median_Stage_Pct': st_med,
        'Diff_from_Median_Points': diff_from_med,
        'Ratio_to_Median': ratio_to_med,
        'Comparison_Status': status
    })

df_part_b = pd.DataFrame(part_b_rows)
print(df_part_b.to_string(index=False))

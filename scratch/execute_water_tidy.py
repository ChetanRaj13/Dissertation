import json
import pandas as pd
import numpy as np
import scipy.stats as stats
import os

print("=== 1. Fisher Exact Test ===")
# Contingency table:
#                 Over-Exploited   Not Over-Exploited   Total
# Hosting (DC)         8                  21             29
# Other (Non-DC)      86                 594            680
# Total               94                 615            709
table = [[8, 21], [86, 594]]
oddsratio, p_two_sided = stats.fisher_exact(table, alternative='two-sided')
oddsratio_less, p_greater = stats.fisher_exact(table, alternative='greater')
print(f"Odds Ratio: {oddsratio:.4f}")
print(f"Two-sided p-value: {p_two_sided:.6f} ({p_two_sided:.4f})")
print(f"Greater (one-sided) p-value: {p_greater:.6f} ({p_greater:.4f})")

print("\n=== 2. Load Nationwide Groundwater JSON & Build Benchmark ===")
with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    nationwide = json.load(f)
df_all = pd.DataFrame(nationwide)
N_districts = len(df_all)

districts_29_meta = [
    {'state': 'Andhra Pradesh', 'district': 'Anakapalli', 'json_name': 'Anakapalli'},
    {'state': 'Andhra Pradesh', 'district': 'Guntur', 'json_name': 'Guntur'},
    {'state': 'Andhra Pradesh', 'district': 'Visakhapatnam', 'json_name': 'Visakhapatnam'},
    {'state': 'Andhra Pradesh', 'district': 'Vizianagaram', 'json_name': 'Vizianagaram'},
    {'state': 'Bihar', 'district': 'Patna', 'json_name': 'Patna'},
    {'state': 'Chhattisgarh', 'district': 'Raipur', 'json_name': 'Raipur'},
    {'state': 'Delhi', 'district': 'South East Delhi', 'json_name': 'South East'},
    {'state': 'Gujarat', 'district': 'Ahmedabad', 'json_name': 'Ahmedabad'},
    {'state': 'Gujarat', 'district': 'Gandhinagar', 'json_name': 'Gandhinagar'},
    {'state': 'Gujarat', 'district': 'Jamnagar', 'json_name': 'Jamnagar'},
    {'state': 'Haryana', 'district': 'Gurugram', 'json_name': 'Gurgaon'},
    {'state': 'Haryana', 'district': 'Panchkula', 'json_name': 'Panchkula'},
    {'state': 'Haryana', 'district': 'Sonipat', 'json_name': 'Sonipat'},
    {'state': 'Karnataka', 'district': 'Bengaluru Rural', 'json_name': 'Bengaluru (Rural)'},
    {'state': 'Karnataka', 'district': 'Bengaluru Urban', 'json_name': 'Bengaluru (Urban)'},
    {'state': 'Madhya Pradesh', 'district': 'Indore', 'json_name': 'Indore'},
    {'state': 'Maharashtra', 'district': 'Mumbai Suburban', 'json_name': 'Mumbai Sub'},
    {'state': 'Maharashtra', 'district': 'Pune', 'json_name': 'Pune'},
    {'state': 'Maharashtra', 'district': 'Raigad', 'json_name': 'Raigad'},
    {'state': 'Maharashtra', 'district': 'Thane', 'json_name': 'Thane'},
    {'state': 'Odisha', 'district': 'Khordha', 'json_name': 'Khurda'},
    {'state': 'Odisha', 'district': 'Puri', 'json_name': 'Puri'},
    {'state': 'Tamil Nadu', 'district': 'Chengalpattu', 'json_name': 'Chengalpattu'},
    {'state': 'Tamil Nadu', 'district': 'Chennai', 'json_name': 'Chennai'},
    {'state': 'Tamil Nadu', 'district': 'Kanchipuram', 'json_name': 'Kancheepuram'},
    {'state': 'Telangana', 'district': 'Ranga Reddy', 'json_name': 'Rangareddy'},
    {'state': 'Uttar Pradesh', 'district': 'Gautam Buddha Nagar', 'json_name': 'G.B.Nagar'},
    {'state': 'West Bengal', 'district': 'Hooghly', 'json_name': 'Hugli'},
    {'state': 'West Bengal', 'district': 'North 24 Parganas', 'json_name': 'North 24 Parganas'}
]

cat_map = {
    'safe': 'Safe',
    'semi_critical': 'Semi-Critical',
    'critical': 'Critical',
    'over_exploited': 'Over-Exploited',
    'saline': 'Saline'
}

dc_states = sorted(list(set(d['state'] for d in districts_29_meta)))
state_medians = {}
for s in dc_states:
    dist_s = df_all[df_all['state'].str.lower() == s.lower()]
    med = dist_s['stage_of_extraction_pct'].median()
    state_medians[s] = round(float(med), 2)

benchmark_rows = []
for item in districts_29_meta:
    s = item['state']
    d = item['district']
    jn = item['json_name']
    match = df_all[(df_all['state'].str.lower() == s.lower()) & (df_all['district'].str.lower() == jn.lower())]
    if len(match) == 0:
        raise ValueError(f"Could not find district {s} - {jn}")
    r = match.iloc[0]
    stage = round(float(r['stage_of_extraction_pct']), 2)
    raw_cat = str(r['category']).lower().strip()
    cat = cat_map.get(raw_cat, raw_cat.title())
    count_above = int((df_all['stage_of_extraction_pct'] > stage).sum())
    rank = count_above + 1
    st_med = state_medians[s]
    diff = round(stage - st_med, 2)
    ratio = round(stage / st_med, 4)
    stat = 'Above median' if diff > 0 else ('Below median' if diff < 0 else 'Equal to median')
    
    benchmark_rows.append({
        'state': s,
        'district': d,
        'cgwb_printed_name': jn,
        'stage_of_extraction_pct': stage,
        'stress_category': cat,
        'national_rank_of_709': rank,
        'state_median_district_stage_pct': st_med,
        'diff_from_state_median_pts': diff,
        'ratio_to_state_median': ratio,
        'status_vs_state_median': stat
    })

df_bench = pd.DataFrame(benchmark_rows)

# Save water_district_benchmark_v1.csv
df_bench.to_csv('water_district_benchmark_v1.csv', index=False)
os.makedirs('DATA/WATER', exist_ok=True)
df_bench.to_csv('DATA/WATER/water_district_benchmark_v1.csv', index=False)
print("Saved water_district_benchmark_v1.csv to root and DATA/WATER/")

print("\n=== 3. Update and Save district_energy_matching_v3.csv ===")
df_energy_dist = pd.read_csv('district_energy_matching_v2.csv')

# Drop any previous water cols if present to prevent collision
cols_to_drop = [c for c in ['district_gw_stage_of_extraction_pct', 'district_gw_stress_category', 'district_gw_national_rank_of_709'] if c in df_energy_dist.columns]
if cols_to_drop:
    df_energy_dist.drop(columns=cols_to_drop, inplace=True)

merged = df_energy_dist.merge(
    df_bench[['state', 'district', 'stage_of_extraction_pct', 'stress_category', 'national_rank_of_709']],
    on=['state', 'district'],
    how='left'
)
merged.rename(columns={
    'stage_of_extraction_pct': 'district_gw_stage_of_extraction_pct',
    'stress_category': 'district_gw_stress_category',
    'national_rank_of_709': 'district_gw_national_rank_of_709'
}, inplace=True)

merged.to_csv('district_energy_matching_v3.csv', index=False)
os.makedirs('DATA/ENERGY', exist_ok=True)
merged.to_csv('DATA/ENERGY/district_energy_matching_v3.csv', index=False)
print("Saved district_energy_matching_v3.csv to root and DATA/ENERGY/")

print("\n=== 4. Save water_scores_all_states_v2.csv ===")
df_state_water = pd.read_csv('water_scores_all_states_v1.csv')
df_state_water.to_csv('water_scores_all_states_v2.csv', index=False)
os.makedirs('DATA/WATER', exist_ok=True)
df_state_water.to_csv('DATA/WATER/water_scores_all_states_v2.csv', index=False)
print("Saved water_scores_all_states_v2.csv to root and DATA/WATER/")

print("\n=== 5. Final Dimensions Check ===")
for p in [
    'water_scores_all_states_v2.csv',
    'DATA/WATER/water_scores_all_states_v2.csv',
    'water_district_benchmark_v1.csv',
    'DATA/WATER/water_district_benchmark_v1.csv',
    'district_energy_matching_v3.csv',
    'DATA/ENERGY/district_energy_matching_v3.csv'
]:
    df_check = pd.read_csv(p)
    print(f"File: {p:<45} | Rows: {df_check.shape[0]:<3} | Cols: {df_check.shape[1]:<3}")

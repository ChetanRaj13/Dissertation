import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')

# 1. Update Uttar Pradesh
up_idx = df[df['state'] == 'Uttar Pradesh'].index[0]
df.at[up_idx, 'water_score'] = 1
df.at[up_idx, 'water_stress_category'] = 'Safe'
df.at[up_idx, 'cgwb_sec6_3_printed_group'] = '< 70%'
df.at[up_idx, 'borderline_stage_flag'] = 'Borderline 70% (diff: +0.00%)'

# 2. Update Delhi and Chandigarh JJM text
delhi_idx = df[df['state'] == 'Delhi'].index[0]
chd_idx = df[df['state'] == 'Chandigarh'].index[0]
df.at[delhi_idx, 'source_jjm'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'
df.at[chd_idx, 'source_jjm'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'
df.at[delhi_idx, 'jjm_equity_category'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'
df.at[chd_idx, 'jjm_equity_category'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'
df.at[delhi_idx, 'jjm_quartile_rank'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'
df.at[chd_idx, 'jjm_quartile_rank'] = 'NOT APPLICABLE (not reported by the JJM dashboard)'

# 3. Clean quartile ranks
q_map_clean = {
    'Kerala': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Jharkhand': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'West Bengal': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Rajasthan': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Madhya Pradesh': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Andhra Pradesh': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Odisha': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Manipur': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'UT of J&K and Ladakh': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Assam': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Meghalaya': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Chhattisgarh': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Tripura': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Karnataka': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Maharashtra': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Sikkim': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Uttar Pradesh': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Tamil Nadu': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Bihar': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Nagaland': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Uttarakhand': 'Q3 (50-75%: 92.17% - 98.12%)',
    'Gujarat': 'Q4 (Top quartile: 100.00% Saturated)',
    'Haryana': 'Q4 (Top quartile: 100.00% Saturated)',
    'Telangana': 'Q4 (Top quartile: 100.00% Saturated)',
    'Dadra & Nagar Haveli and Daman & Diu': 'Q4 (Top quartile: 100.00% Saturated)',
    'Arunachal Pradesh': 'Q4 (Top quartile: 100.00% Saturated)',
    'Himachal Pradesh': 'Q4 (Top quartile: 100.00% Saturated)',
    'Goa': 'Q4 (Top quartile: 100.00% Saturated)',
    'Mizoram': 'Q4 (Top quartile: 100.00% Saturated)',
    'Punjab': 'Q4 (Top quartile: 100.00% Saturated)',
    'Puducherry': 'Q4 (Top quartile: 100.00% Saturated)'
}

for idx, r in df.iterrows():
    st = r['state']
    if st in q_map_clean:
        df.at[idx, 'jjm_quartile_rank'] = q_map_clean[st]

# Save both
df.to_csv('water_scores_all_states_v1.csv', index=False)
df.to_csv('DATA/WATER/water_scores_all_states_v1.csv', index=False)

print("Saved Round 2 updates to water_scores_all_states_v1.csv in root and DATA/WATER/")
print(df[['state', 'cgwb_stage_of_extraction_pct', 'water_score', 'water_stress_category', 'borderline_stage_flag']].head(15).to_string())

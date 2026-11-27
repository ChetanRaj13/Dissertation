import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')

# Rank-based quartile assignment map
q_map = {
    'Kerala': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Jharkhand': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'West Bengal': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Rajasthan': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Madhya Pradesh': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Andhra Pradesh': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Odisha': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'Manipur': 'Q1 (Lowest 25%: 55.27% - 79.67%)',
    'UT of J&K and Ladakh': 'Q2 (25-50%: 81.79% - 90.65%)',
    'Assam': 'Q2 (25-50%: 82.06% - 90.65%)',
    'Meghalaya': 'Q2 (25-50%: 82.06% - 90.65%)',
    'Chhattisgarh': 'Q2 (25-50%: 82.06% - 90.65%)',
    'Tripura': 'Q2 (25-50%: 82.06% - 90.65%)',
    'Karnataka': 'Q2 (25-50%: 82.06% - 90.65%)',
    'Maharashtra': 'Q2 (25-50%: 82.06% - 90.65%)',
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
    if st in q_map:
        df.at[idx, 'jjm_quartile_rank'] = q_map[st]

# Save updated CSV
df.to_csv('water_scores_all_states_v1.csv', index=False)
df.to_csv('DATA/WATER/water_scores_all_states_v1.csv', index=False)
print("Updated water_scores_all_states_v1.csv successfully!")

import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
comp = df[~df['state'].isin(['Delhi', 'Chandigarh', 'DVC', 'Andaman & Nicobar', 'Lakshadweep'])].copy()
comp['jjm_cov'] = pd.to_numeric(comp['jjm_rural_tap_coverage_pct'])
comp = comp.sort_values(by='jjm_cov', ascending=True).reset_index(drop=True)
comp['rank'] = comp.index + 1
# Divide into 4 quartiles based on rank (30 states: 8, 7, 7, 8)
# Q1: 1-8 (26.7%)
# Q2: 9-15 (23.3%)
# Q3: 16-22 (23.3%)
# Q4: 23-30 (26.7%)

def assign_q(r):
    if r <= 8:
        return 'Q1 (Lowest 25%: 55.27% - 81.79%)'
    elif r <= 15:
        return 'Q2 (25-50%: 82.06% - 90.65%)'
    elif r <= 22:
        return 'Q3 (50-75%: 92.17% - 98.12%)'
    else:
        return 'Q4 (Highest 25%: 100.00% Saturated)'

comp['q_band'] = comp['rank'].apply(assign_q)
for idx, r in comp.iterrows():
    print(f"Rank {r['rank']:<2}: {r['state']:<25} | {r['jjm_cov']:<6.2f}% | {r['q_band']}")

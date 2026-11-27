import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
comp = df[~df['state'].isin(['Delhi', 'Chandigarh', 'DVC', 'Andaman & Nicobar', 'Lakshadweep'])].copy()

print("=== DC STATES (N=13 with rural HH) BY QUARTILE ===")
for q in ['Q1 (Lowest 25%: 55.27% - 79.67%)', 'Q2 (25-50%: 81.79% - 90.65%)', 'Q3 (50-75%: 92.17% - 98.12%)', 'Q4 (Top quartile: 100.00% Saturated)']:
    sub_dc = comp[(comp['data_centre_state'] == 'Yes') & (comp['jjm_quartile_rank'] == q)]
    states_str = ", ".join([f"{r['state']} ({r['jjm_rural_tap_coverage_pct']}%)" for idx, r in sub_dc.iterrows()])
    print(f"{q:<40} | Count: {len(sub_dc):<2} | {states_str}")

print("\n=== NON-DC STATES (N=18 with rural HH) BY QUARTILE ===")
for q in ['Q1 (Lowest 25%: 55.27% - 79.67%)', 'Q2 (25-50%: 81.79% - 90.65%)', 'Q3 (50-75%: 92.17% - 98.12%)', 'Q4 (Top quartile: 100.00% Saturated)']:
    sub_ndc = comp[(comp['data_centre_state'] == 'No') & (comp['jjm_quartile_rank'] == q)]
    states_str = ", ".join([f"{r['state']} ({r['jjm_rural_tap_coverage_pct']}%)" for idx, r in sub_ndc.iterrows()])
    print(f"{q:<40} | Count: {len(sub_ndc):<2} | {states_str}")

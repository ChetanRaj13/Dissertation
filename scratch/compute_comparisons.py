import pandas as pd

df = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')

# Filter out DVC, Andaman & Nicobar, Lakshadweep for comparisons
df_comp = df[~df['state'].isin(['DVC', 'Andaman & Nicobar', 'Lakshadweep'])].copy()
print(f"Comparison set size: {len(df_comp)} states/UTs (14 DC, 19 non-DC)")

# 1. State ranking on stage of extraction
df_comp['cgwb_stage_of_extraction_pct'] = pd.to_numeric(df_comp['cgwb_stage_of_extraction_pct'])
df_stage_rank = df_comp.sort_values(by='cgwb_stage_of_extraction_pct', ascending=False).reset_index(drop=True)
df_stage_rank['stage_rank'] = df_stage_rank.index + 1

print("\n=== RANKING ON STAGE OF EXTRACTION (High to Low) ===")
print(f"{'Rank':<5} | {'State':<28} | {'DC State':<9} | {'Stage%':<8} | {'Score':<5} | {'Category':<14}")
print("-" * 75)
for idx, r in df_stage_rank.iterrows():
    print(f"{r['stage_rank']:<5} | {r['state']:<28} | {r['data_centre_state']:<9} | {r['cgwb_stage_of_extraction_pct']:<8.2f} | {r['water_score']:<5} | {r['water_stress_category']:<14}")

# 2. Ranking on JJM coverage
# Note: Delhi and Chandigarh have NOT APPLICABLE
df_jjm_comp = df_comp[~df_comp['state'].isin(['Delhi', 'Chandigarh'])].copy()
df_jjm_comp['jjm_rural_tap_coverage_pct'] = pd.to_numeric(df_jjm_comp['jjm_rural_tap_coverage_pct'])
df_jjm_rank = df_jjm_comp.sort_values(by='jjm_rural_tap_coverage_pct', ascending=True).reset_index(drop=True) # Low to High (most deprived to saturated)
df_jjm_rank['jjm_rank_deprived'] = df_jjm_rank.index + 1

print("\n=== RANKING ON JJM TAP COVERAGE (Low to High: Most Deprived First) ===")
print(f"{'Rank':<5} | {'State':<28} | {'DC State':<9} | {'JJM%':<8} | {'Equity Category':<15} | {'As Of Date'}")
print("-" * 85)
for idx, r in df_jjm_rank.iterrows():
    print(f"{r['jjm_rank_deprived']:<5} | {r['state']:<28} | {r['data_centre_state']:<9} | {r['jjm_rural_tap_coverage_pct']:<8.2f} | {r['jjm_equity_category']:<15} | {r['jjm_as_of_date']}")

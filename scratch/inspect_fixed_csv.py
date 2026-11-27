import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
print(f"Columns ({len(df.columns)}):", df.columns.tolist())

print("\nSample preview:")
print(df[['state', 'cgwb_stage_of_extraction_pct', 'water_score', 'cgwb_sec6_3_printed_group', 'borderline_stage_flag', 'jjm_rural_tap_coverage_pct', 'jjm_quartile_rank', 'jjm_as_of_date']].head(15).to_string())

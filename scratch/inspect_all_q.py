import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
print(df[['state', 'data_centre_state', 'jjm_rural_tap_coverage_pct', 'jjm_quartile_rank']].to_string())

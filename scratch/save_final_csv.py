import shutil
import pandas as pd

df = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')

# Ensure directories exist and save
df.to_csv('water_scores_all_states_v1.csv', index=False)
df.to_csv('DATA/WATER/water_scores_all_states_v1.csv', index=False)

print("Saved water_scores_all_states_v1.csv in root and in DATA/WATER/")
print("Row count:", len(df))
print("Column count:", len(df.columns))

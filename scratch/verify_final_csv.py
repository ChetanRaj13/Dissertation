import pandas as pd

df1 = pd.read_csv('water_scores_all_states_v1.csv')
df2 = pd.read_csv('DATA/WATER/water_scores_all_states_v1.csv')

assert len(df1) == 36, f"Expected 36 rows, got {len(df1)}"
assert len(df2) == 36, f"Expected 36 rows, got {len(df2)}"
assert list(df1.columns) == list(df2.columns), "Columns do not match"
assert df1.equals(df2), "Files are not identical"

# Check energy states match
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')
assert list(df1['state']) == list(df_energy['state']), "State names or order do not match energy file"

print("All assertions passed successfully!")
print("Row count:", len(df1))
print("Column count:", len(df1.columns))
print("States list matches energy_scores_all_states_v2.csv exactly (36 rows).")

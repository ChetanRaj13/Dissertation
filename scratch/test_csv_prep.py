import pandas as pd
import numpy as np

# Load the test parse
# Let's verify all columns needed for water_scores_all_states_v1.csv
# 1. State names: must match energy_scores_all_states_v2.csv exactly (36 rows)
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')
state_order = df_energy['state'].tolist()
print("Total rows:", len(state_order))

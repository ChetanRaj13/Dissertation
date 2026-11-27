import json
import pandas as pd
import numpy as np

# Load energy states
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')
print("Energy states count:", len(df_energy))
states_list = df_energy['state'].tolist()
print("States list:", states_list)

# Load Annexure I and Annexure III (A) data
# We can extract all values directly from our verified parsing of PDF pages 171 and 215!

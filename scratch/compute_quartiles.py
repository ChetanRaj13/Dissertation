import pandas as pd
import json

with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_data = json.load(f)['d']

# Let's map to our 36 states from energy_scores_all_states_v2.csv
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')

# Load the live JJM map
jjm_map = {item['Name'].strip(): float(item['Per']) for item in jjm_data}
jjm_map['D&NH and D&D'] = 100.0
jjm_map['A & N Islands'] = 100.0

# J&K and Ladakh combined: 81.79
jjm_map['UT of J&K and Ladakh'] = 81.79

vals = []
for st in df_energy['state']:
    if st in ['Delhi', 'Chandigarh', 'DVC', 'Andaman & Nicobar', 'Lakshadweep']:
        continue
    val = jjm_map.get(st)
    if val is not None:
        vals.append({'state': st, 'jjm_cov': val})

df_jjm_comp = pd.DataFrame(vals)
print("Comparison states N =", len(df_jjm_comp))
print(df_jjm_comp['jjm_cov'].describe())

# Compute quartiles
q1 = df_jjm_comp['jjm_cov'].quantile(0.25)
q2 = df_jjm_comp['jjm_cov'].quantile(0.50)
q3 = df_jjm_comp['jjm_cov'].quantile(0.75)
print(f"Q1 (25th percentile): {q1:.2f}%")
print(f"Q2 (50th percentile, Median): {q2:.2f}%")
print(f"Q3 (75th percentile): {q3:.2f}%")

def get_quartile(v):
    if v <= q1:
        return 'Q1 (Lowest 25%)'
    elif v <= q2:
        return 'Q2 (25-50%)'
    elif v <= q3:
        return 'Q3 (50-75%)'
    else:
        return 'Q4 (Highest 25%)'

df_jjm_comp['quartile_rank'] = df_jjm_comp['jjm_cov'].apply(get_quartile)
print("\nQuartile distribution:")
print(df_jjm_comp['quartile_rank'].value_counts())

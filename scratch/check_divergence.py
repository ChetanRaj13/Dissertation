import pandas as pd
import json

df_states = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')
state_cats = dict(zip(df_states['state'], df_states['water_stress_category']))

with open('scratch/test_all_29_ranks.py', 'r') as f:
    # let's run the ranking and compare categories
    pass

# Load our 29 districts data from test_all_29_ranks
df_dist = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')

# Let's inspect the 29 districts mapping from test_all_29_ranks
from test_all_29_ranks import res as df_29

cat_order = {'safe': 1, 'semi_critical': 2, 'critical': 3, 'over_exploited': 4}

df_29['state_category'] = df_29['state'].map(lambda s: state_cats.get(s, '').lower().replace('-', '_'))

divergence = []
for idx, r in df_29.iterrows():
    d_cat = r['category'].lower().replace('-', '_')
    s_cat = r['state_category']
    d_score = cat_order[d_cat]
    s_score = cat_order[s_cat]
    if d_score > s_score:
        div = "district worse than state"
    elif d_score < s_score:
        div = "district better than state"
    else:
        div = "district matches state"
    divergence.append(div)

df_29['divergence_flag'] = divergence

print(f"{'State':<15} | {'District':<20} | {'Dist_Stage%':<11} | {'Dist_Cat':<14} | {'State_Cat':<14} | {'Divergence'}")
print("-" * 105)
for idx, r in df_29.iterrows():
    print(f"{r['state']:<15} | {r['district']:<20} | {r['stage_pct']:<11} | {r['category']:<14} | {r['state_category']:<14} | {r['divergence_flag']}")

import pandas as pd
import numpy as np

# Load the base energy dataframe
es_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\energy_scores_all_states_v1.csv"
df_es = pd.read_csv(es_path)

# Active jurisdictions (excluding stand-alone islands)
df_active = df_es[~df_es['flags'].fillna('').str.contains("EXCLUDED")].copy()

# Add Variant DISCOM and Delivery scores
# Delhi: private DISCOM average = (84.35 + 70.24 + 69.54) / 3 = 74.71 -> DISCOM score 2. Subst = 5 -> Delivery = 3.5
# Odisha: private DISCOM average = (94.77 + 93.00 + 78.30 + 63.91) / 4 = 82.50 -> DISCOM score 2. Subst = 2 -> Delivery = 2.0

df_active['discom_score_standard'] = pd.to_numeric(df_active['discom_score'], errors='coerce')
df_active['delivery_score_standard'] = pd.to_numeric(df_active['delivery_score'], errors='coerce')

df_active['discom_score_variant'] = df_active['discom_score_standard'].copy()
df_active.loc[df_active['state'] == 'Delhi', 'discom_score_variant'] = 2.0
df_active.loc[df_active['state'] == 'Odisha', 'discom_score_variant'] = 2.0

df_active['delivery_score_variant'] = df_active['delivery_score_standard'].copy()
df_active.loc[df_active['state'] == 'Delhi', 'delivery_score_variant'] = 3.5
df_active.loc[df_active['state'] == 'Odisha', 'delivery_score_variant'] = 2.0

metrics = [
    ('supply_score', 'Supply Score'),
    ('substation_score', 'Substation Score'),
    ('discom_score_standard', 'DISCOM Score (Standard)'),
    ('delivery_score_standard', 'Delivery Score (Standard)'),
    ('discom_score_variant', 'DISCOM Score (Variant)'),
    ('delivery_score_variant', 'Delivery Score (Variant)')
]

df_yes = df_active[df_active['data_centre_state'] == 'Yes']
df_no = df_active[df_active['data_centre_state'] == 'No']

stats_rows = []
for col, name in metrics:
    y_s = df_yes[col].dropna()
    n_s = df_no[col].dropna()
    all_s = df_active[col].dropna()
    
    stats_rows.append({
        'metric': name,
        'all_N': len(all_s),
        'all_sum': round(all_s.sum(), 2),
        'all_mean': round(all_s.mean(), 2),
        'all_median': round(all_s.median(), 2),
        'dc_N': len(y_s),
        'dc_sum': round(y_s.sum(), 2),
        'dc_mean': round(y_s.mean(), 2),
        'dc_median': round(y_s.median(), 2),
        'nondc_N': len(n_s),
        'nondc_sum': round(n_s.sum(), 2),
        'nondc_mean': round(n_s.mean(), 2),
        'nondc_median': round(n_s.median(), 2)
    })

df_stats_res = pd.DataFrame(stats_rows)
print("=== STATISTICAL COMPARISON TABLE ===")
print(df_stats_res.to_string())

# Check rankings and comparisons
print("\n=== DC STATES WORSE THAN NON-DC MEDIAN ===")
for col, name in metrics:
    n_med = df_no[col].dropna().median()
    worse = df_yes[df_yes[col] > n_med][['state', col]]
    print(f"\n{name} (Non-DC Median = {n_med}):")
    if len(worse) > 0:
        for idx, r in worse.sort_values(by=col, ascending=False).iterrows():
            print(f"  - {r['state']}: {r[col]}")
    else:
        print("  - None")

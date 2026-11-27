import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')

# Exclude DVC
df_states = df[df['state'] != 'DVC'].copy()
df_states['stage'] = pd.to_numeric(df_states['cgwb_stage_of_extraction_pct'])

print("=== CHECKING BORDERLINE STAGE VALUES (within 2 points of 70, 90, 100) ===")
borderline = []
for idx, r in df_states.iterrows():
    st = r['state']
    val = r['stage']
    dist_70 = abs(val - 70.0)
    dist_90 = abs(val - 90.0)
    dist_100 = abs(val - 100.0)
    
    flag = []
    if dist_70 <= 2.0:
        flag.append(f"Borderline 70% (diff: {val - 70.0:+.2f}%)")
    if dist_90 <= 2.0:
        flag.append(f"Borderline 90% (diff: {val - 90.0:+.2f}%)")
    if dist_100 <= 2.0:
        flag.append(f"Borderline 100% (diff: {val - 100.0:+.2f}%)")
        
    flag_str = "; ".join(flag) if flag else "No"
    borderline.append({
        'state': st,
        'stage': val,
        'dist_70': dist_70,
        'dist_90': dist_90,
        'dist_100': dist_100,
        'flag': flag_str
    })

df_b = pd.DataFrame(borderline)
print(df_b[df_b['flag'] != 'No'].to_string())

print("\nClosest to 70%:")
print(df_b.sort_values(by='dist_70')[['state', 'stage', 'dist_70']].head(5).to_string())

print("\nClosest to 90%:")
print(df_b.sort_values(by='dist_90')[['state', 'stage', 'dist_90']].head(5).to_string())

print("\nClosest to 100%:")
print(df_b.sort_values(by='dist_100')[['state', 'stage', 'dist_100']].head(5).to_string())

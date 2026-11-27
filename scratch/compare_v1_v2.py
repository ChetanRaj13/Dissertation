import pandas as pd

df_orig_v1 = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')
df_disk_v1 = pd.read_csv('water_scores_all_states_v1.csv')
df_v2 = pd.read_csv('water_scores_all_states_v2.csv')

print('Orig v1 shape:', df_orig_v1.shape)
print('Disk v1 shape:', df_disk_v1.shape)
print('V2 shape:', df_v2.shape)

# Let's check diff between disk_v1 and v2
diffs_disk = []
for idx, r1 in df_disk_v1.iterrows():
    st = r1['state']
    r2 = df_v2[df_v2['state'] == st].iloc[0]
    for col in df_disk_v1.columns:
        v1_val = str(r1[col])
        v2_val = str(r2[col])
        if v1_val != v2_val:
            diffs_disk.append({'state': st, 'column': col, 'old_value': v1_val, 'new_value': v2_val})

print(f'\nDiffs between disk v1 and v2: {len(diffs_disk)}')

# Let's check diff between original v1 (preview) and v2
common_cols = [c for c in df_orig_v1.columns if c in df_v2.columns]
added_cols = [c for c in df_v2.columns if c not in df_orig_v1.columns]
print(f'Added columns in v2: {added_cols}')

diffs_orig = []
for idx, r1 in df_orig_v1.iterrows():
    st = r1['state']
    r2 = df_v2[df_v2['state'] == st].iloc[0]
    for col in common_cols:
        v1_val = str(r1[col])
        v2_val = str(r2[col])
        if v1_val != v2_val:
            diffs_orig.append({'state': st, 'column': col, 'old_value': v1_val, 'new_value': v2_val})

print(f'Diffs between original preview v1 and v2: {len(diffs_orig)}')
for d in diffs_orig:
    print(f"{d['state']:<25} | {d['column']:<25} | {d['old_value']:<35} -> {d['new_value']}")

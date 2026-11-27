import pandas as pd

df_v1 = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')
df_v2 = pd.read_csv('water_scores_all_states_v2.csv')

print(f"v1 dimensions: {df_v1.shape[0]} rows, {df_v1.shape[1]} columns")
print(f"v2 dimensions: {df_v2.shape[0]} rows, {df_v2.shape[1]} columns")

added_cols = [c for c in df_v2.columns if c not in df_v1.columns]
print(f"Added columns in v2 ({len(added_cols)}): {added_cols}")

common_cols = [c for c in df_v1.columns if c in df_v2.columns]

diffs = []
for idx, r1 in df_v1.iterrows():
    st = r1['state']
    r2 = df_v2[df_v2['state'] == st].iloc[0]
    for col in common_cols:
        v1_val = str(r1[col])
        v2_val = str(r2[col])
        if v1_val != v2_val:
            diffs.append({
                'state': st,
                'column': col,
                'old_value': v1_val,
                'new_value': v2_val
            })

df_diffs = pd.DataFrame(diffs)
print(f"\nTotal cell-level differences across common columns: {len(df_diffs)}")
print("\nBreakdown by column:")
print(df_diffs['column'].value_counts())

# Let's inspect differences in non-JJM metadata columns
non_jjm = df_diffs[~df_diffs['column'].str.startswith('jjm') & ~df_diffs['column'].str.startswith('source_jjm')]
print("\nNon-JJM changes:")
print(non_jjm.to_string())

# Save diff to a clean csv
df_diffs.to_csv('scratch/cell_diff_v1_v2.csv', index=False)

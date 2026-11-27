import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
for col in df.columns:
    matches = df[df[col].astype(str).str.contains('<70|< 70|Safe', case=False, na=False)]
    if len(matches) > 0:
        print(f"Column '{col}' has {len(matches)} matches:")
        print(matches[col].unique()[:5])

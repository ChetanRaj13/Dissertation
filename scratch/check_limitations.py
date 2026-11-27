import pandas as pd

df = pd.read_csv('water_scores_all_states_v1.csv')
for idx, r in df.iterrows():
    if pd.notna(r['limitations']) and len(str(r['limitations'])) > 0:
        print(f"{r['state']}: {r['limitations']}")
        break

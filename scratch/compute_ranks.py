import json
import pandas as pd
import numpy as np

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"Total districts: {len(df)}")
print(df.info())
print(df['stage_of_extraction_pct'].describe())

# Check nulls or negatives
print("Nulls:", df['stage_of_extraction_pct'].isnull().sum())
print("Min:", df['stage_of_extraction_pct'].min(), "Max:", df['stage_of_extraction_pct'].max())

# Let's map the 29 hosting districts
mapping = [
    ('Andhra Pradesh', 'Anakapalli', 'Anakapalli'),
    ('Andhra Pradesh', 'Guntur', 'Guntur'),
    ('Andhra Pradesh', 'Visakhapatnam', 'Visakhapatnam'),
    ('Andhra Pradesh', 'Vizianagaram', 'Vizianagaram'),
    ('Bihar', 'Patna', 'Patna'),
    ('Chhattisgarh', 'Raipur', 'Raipur'),
    ('Delhi', 'South East Delhi', 'South East'),
    ('Gujarat', 'Ahmedabad', 'Ahmedabad'),
    ('Gujarat', 'Gandhinagar', 'Gandhinagar'),
    ('Gujarat', 'Jamnagar', 'Jamnagar'),
    ('Haryana', 'Gurugram', 'Gurgaon'),
    ('Haryana', 'Panchkula', 'Panchkula'),
    ('Haryana', 'Sonipat', 'Sonipat'),
    ('Karnataka', 'Bengaluru Rural', 'Bengaluru (Rural)'),
    ('Karnataka', 'Bengaluru Urban', 'Bengaluru (Urban)'),
    ('Madhya Pradesh', 'Indore', 'Indore'),
    ('Maharashtra', 'Mumbai Suburban', 'Mumbai Sub'),
    ('Maharashtra', 'Pune', 'Pune'),
    ('Maharashtra', 'Raigad', 'Raigad'),
    ('Maharashtra', 'Thane', 'Thane'),
    ('Odisha', 'Khordha', 'Khordha'),
    ('Odisha', 'Puri', 'Puri'),
    ('Tamil Nadu', 'Chengalpattu', 'Chengalpattu'),
    ('Tamil Nadu', 'Chennai', 'Chennai'),
    ('Tamil Nadu', 'Kanchipuram', 'Kanchipuram'),
    ('Telangana', 'Ranga Reddy', 'Ranga Reddy'),
    ('Uttar Pradesh', 'Gautam Buddha Nagar', 'Gautam Buddha Nagar'),
    ('West Bengal', 'Hooghly', 'Hooghly'),
    ('West Bengal', 'North 24 Parganas', 'North Twenty Four Parganas')
]

# Sort all districts descending by stage_of_extraction_pct
df_sorted = df.sort_values(by='stage_of_extraction_pct', ascending=False).reset_index(drop=True)
df_sorted['rank'] = df_sorted.index + 1
# Count of districts above it = rank - 1 (or ties handling)
# Percentile: (N - rank) / N * 100 or rank / N * 100. Let's compute both standard definitions.

N = len(df_sorted)
print(f"\nTotal districts N = {N}")

results = []
for state, dist, printed in mapping:
    # find row in df
    match = df[(df['state'].str.lower() == state.lower()) & 
               (df['district'].str.lower().isin([dist.lower(), printed.lower(), dist.lower().replace(' ', '')]))]
    if len(match) == 0:
        # try substring
        match = df[(df['state'].str.lower() == state.lower()) & 
                   (df['district'].str.lower().str.contains(printed.lower()[:5]))]
    if len(match) > 0:
        row = match.iloc[0]
        stage = row['stage_of_extraction_pct']
        # count of districts strictly above this stage
        count_above = (df['stage_of_extraction_pct'] > stage).sum()
        rank = count_above + 1
        # Percentile rank: % of districts with stage <= this district's stage
        # or % of districts below it
        pct_below = ((df['stage_of_extraction_pct'] <= stage).sum() / N) * 100.0
        pct_above = (count_above / N) * 100.0
        results.append({
            'state': state,
            'district': dist,
            'cgwb_name': row['district'],
            'stage_pct': stage,
            'rank': rank,
            'count_above': count_above,
            'percentile_top': round(pct_above, 2), # e.g. top 2%
            'percentile_rank': round(pct_below, 2), # percentile from bottom (standard percentile)
            'page': row.get('page')
        })
    else:
        print(f"FAILED TO MATCH: {state} - {dist} ({printed})")

res_df = pd.DataFrame(results)
print(res_df.to_string())

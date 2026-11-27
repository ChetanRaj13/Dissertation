import json
import pandas as pd

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    nationwide = json.load(f)

df = pd.DataFrame(nationwide)
N = len(df)

# Exact district mapping
districts_29 = [
    {'state': 'Andhra Pradesh', 'district': 'Anakapalli', 'json_name': 'Anakapalli'},
    {'state': 'Andhra Pradesh', 'district': 'Guntur', 'json_name': 'Guntur'},
    {'state': 'Andhra Pradesh', 'district': 'Visakhapatnam', 'json_name': 'Visakhapatnam'},
    {'state': 'Andhra Pradesh', 'district': 'Vizianagaram', 'json_name': 'Vizianagaram'},
    {'state': 'Bihar', 'district': 'Patna', 'json_name': 'Patna'},
    {'state': 'Chhattisgarh', 'district': 'Raipur', 'json_name': 'Raipur'},
    {'state': 'Delhi', 'district': 'South East Delhi', 'json_name': 'South East'},
    {'state': 'Gujarat', 'district': 'Ahmedabad', 'json_name': 'Ahmedabad'},
    {'state': 'Gujarat', 'district': 'Gandhinagar', 'json_name': 'Gandhinagar'},
    {'state': 'Gujarat', 'district': 'Jamnagar', 'json_name': 'Jamnagar'},
    {'state': 'Haryana', 'district': 'Gurugram', 'json_name': 'Gurgaon'},
    {'state': 'Haryana', 'district': 'Panchkula', 'json_name': 'Panchkula'},
    {'state': 'Haryana', 'district': 'Sonipat', 'json_name': 'Sonipat'},
    {'state': 'Karnataka', 'district': 'Bengaluru Rural', 'json_name': 'Bengaluru (Rural)'},
    {'state': 'Karnataka', 'district': 'Bengaluru Urban', 'json_name': 'Bengaluru (Urban)'},
    {'state': 'Madhya Pradesh', 'district': 'Indore', 'json_name': 'Indore'},
    {'state': 'Maharashtra', 'district': 'Mumbai Suburban', 'json_name': 'Mumbai Sub'},
    {'state': 'Maharashtra', 'district': 'Pune', 'json_name': 'Pune'},
    {'state': 'Maharashtra', 'district': 'Raigad', 'json_name': 'Raigad'},
    {'state': 'Maharashtra', 'district': 'Thane', 'json_name': 'Thane'},
    {'state': 'Odisha', 'district': 'Khordha', 'json_name': 'Khurda'},
    {'state': 'Odisha', 'district': 'Puri', 'json_name': 'Puri'},
    {'state': 'Tamil Nadu', 'district': 'Chengalpattu', 'json_name': 'Chengalpattu'},
    {'state': 'Tamil Nadu', 'district': 'Chennai', 'json_name': 'Chennai'},
    {'state': 'Tamil Nadu', 'district': 'Kanchipuram', 'json_name': 'Kancheepuram'},
    {'state': 'Telangana', 'district': 'Ranga Reddy', 'json_name': 'Rangareddy'},
    {'state': 'Uttar Pradesh', 'district': 'Gautam Buddha Nagar', 'json_name': 'G.B.Nagar'},
    {'state': 'West Bengal', 'district': 'Hooghly', 'json_name': 'Hugli'},
    {'state': 'West Bengal', 'district': 'North 24 Parganas', 'json_name': 'North 24 Parganas'}
]

rows = []
for item in districts_29:
    s = item['state']
    d = item['district']
    jn = item['json_name']
    match = df[(df['state'].str.lower() == s.lower()) & (df['district'].str.lower() == jn.lower())]
    if len(match) == 0:
        print(f"Error: Could not find {s} - {jn}")
        continue
    r = match.iloc[0]
    stage = r['stage_of_extraction_pct']
    cat = r['category']
    count_above = int((df['stage_of_extraction_pct'] > stage).sum())
    rank = count_above + 1
    # Percentile from bottom (standard percentile: % of districts with stage <= this district)
    percentile_rank = round(((df['stage_of_extraction_pct'] <= stage).sum() / N) * 100.0, 2)
    # Top percentile (% of districts strictly worse/higher)
    top_percentile = round((count_above / N) * 100.0, 2)
    rows.append({
        'state': s,
        'district': d,
        'cgwb_printed_name': jn,
        'stage_pct': stage,
        'category': cat,
        'count_above': count_above,
        'rank': rank,
        'percentile_rank': percentile_rank,
        'top_pct': top_percentile,
        'page': r.get('page')
    })

res = pd.DataFrame(rows)
print(f"Matched exactly {len(res)} of 29 districts:")
print(res.to_string())

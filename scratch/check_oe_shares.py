import json
import pandas as pd

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    nationwide = json.load(f)
df_all = pd.DataFrame(nationwide)

from test_all_29_ranks import res as df_29

oe_all = (df_all['stage_of_extraction_pct'] > 100.0).sum()
oe_host = (df_29['stage_pct'] > 100.0).sum()
oe_nonhost = oe_all - oe_host
n_nonhost = len(df_all) - len(df_29)

print(f"Total districts: {len(df_all)}, OE total: {oe_all} ({oe_all/len(df_all)*100:.2f}%)")
print(f"Hosting districts: {len(df_29)}, OE hosting: {oe_host} ({oe_host/len(df_29)*100:.2f}%)")
print(f"Other districts: {n_nonhost}, OE other: {oe_nonhost} ({oe_nonhost/n_nonhost*100:.2f}%)")

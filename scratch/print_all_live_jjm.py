import json
import pandas as pd

with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_data = json.load(f)['d']

print(f"Total live records: {len(jjm_data)}")
for r in jjm_data:
    print(f"{r['Name']:<30} | Total: {r['Total']:<10} | Tap: {r['Value']:<10} | Per: {r['Per']}%")

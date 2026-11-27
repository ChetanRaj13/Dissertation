import json
import pandas as pd

with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_data = json.load(f)['d']

print(f"Total JJM live entities: {len(jjm_data)}")
for item in jjm_data:
    print(f"{item['KeyId']} | {item['KeyValue']} | {item['Name']:<30} | {item['Per']}% | Total HH: {item['Total']} | Tap: {item['Value']}")

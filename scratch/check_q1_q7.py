import json
import re

# 1. Search final_merged_context.md
with open('final_merged_context.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== SEARCHING final_merged_context.md FOR EQUITY / CUT-OFFS / JJM ===")
patterns = [r'cut-off', r'cutoff', r'equity', r'tap-deprived', r'tap deprived', r'75%', r'90%']
found_lines = []
for line_no, line in enumerate(text.split('\n'), 1):
    for p in patterns:
        if re.search(p, line, re.I):
            found_lines.append((line_no, p, line.strip()))

print(f"Total matching lines: {len(found_lines)}")
for ln, p, l in found_lines:
    print(f"Line {ln} [{p}]: {l}")

# 2. Check Rajasthan raw record in scratch/jjm_table_graph.json
with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_data = json.load(f)['d']

print("\n=== RAJASTHAN RAW RECORD IN jjm_table_graph.json ===")
for item in jjm_data:
    if 'rajasthan' in item.get('Name', '').lower():
        print(json.dumps(item, indent=2))
        total_hh = int(item['Total'])
        tap_hh = int(item['Value'])
        per_str = item['Per']
        computed = (tap_hh / total_hh) * 100.0
        print(f"Total: {total_hh}, Tap: {tap_hh}, Per string: {per_str}, Computed: {computed:.4f}%")

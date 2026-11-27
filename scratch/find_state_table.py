with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

import re
matches = [m.start() for m in re.finditer(r'tbl_state|tblState|Bind_table_graph|table_data', js_text)]
for m in matches:
    print("--- MATCH ---")
    print(js_text[max(0, m-50):min(len(js_text), m+250)])

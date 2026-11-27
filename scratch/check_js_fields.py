with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

import re
matches = [m.start() for m in re.finditer(r'hcpws|Bind_table_graph|Per_HC_Remain|HC_Remain', js_text)]
print(f"Matches in JJM_Dashboard.js: {len(matches)}")
for m in matches[:10]:
    print("--- MATCH ---")
    print(js_text[max(0, m-100):min(len(js_text), m+200)])

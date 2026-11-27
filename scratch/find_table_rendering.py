with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<table|tbody|table-responsive|table_data', js_text, re.I)]
print(f"Matches for table: {len(matches)}")
for m in matches[:5]:
    print("--- MATCH ---")
    print(js_text[max(0, m-50):min(len(js_text), m+300)])

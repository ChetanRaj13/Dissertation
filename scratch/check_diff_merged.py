with open('final_merged_context.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(Haryana|Punjab|Rajasthan|Delhi|Tamil Nadu|Karnataka|Maharashtra|Gujarat|Uttar Pradesh).*?(extract|stage|bcm|gw)', text, re.I)
print("Matches count:", len(matches))
for m in matches[:10]:
    print(m)

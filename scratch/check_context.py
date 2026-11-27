with open('Full Context.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'Water Equity', text)
while m:
    pos = m.start()
    print('--- MATCH ---')
    print(text[max(0, pos-200):min(len(text), pos+600)])
    m = re.search(r'Water Equity', text[pos+20:])
    if m:
        pos = pos + 20 + m.start()
        print('--- NEXT MATCH ---')
        print(text[max(0, pos-200):min(len(text), pos+600)])
    break

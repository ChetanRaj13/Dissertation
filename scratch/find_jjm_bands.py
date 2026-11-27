import os, re

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.py', '.tsv', '.csv', '.json', '.txt')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    t = fl.read()
                matches = re.findall(r'(\b\w+\b\s+){0,5}(tap[ -]deprived|tap[ -]coverage|underserved|deprived|equity)(\s+\b\w+\b){0,5}', t, re.I)
                if matches and 'scratch' not in root:
                    print(f"File: {p}")
                    for m in matches[:5]:
                        # print the matched full text
                        pass
            except:
                pass

import os, glob, re

patterns = [r'tap-deprived', r'tap deprived', r'equity cut', r'water equity', r'W_equity', r'W\{equity\}', r'equity frontline']

results = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.txt', '.tex', '.py', '.tsv', '.csv', '.json')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fl:
                    content = fl.read()
                for p in patterns:
                    for m in re.finditer(p, content, re.IGNORECASE):
                        start = max(0, m.start() - 100)
                        end = min(len(content), m.end() + 150)
                        results.append((path, p, content[start:end].replace('\n', ' ')))
            except Exception as e:
                pass

print(f"Total occurrences found: {len(results)}")
for r in results[:25]:
    print(f"[{r[0]}] ({r[1]}): {r[2]}\n")

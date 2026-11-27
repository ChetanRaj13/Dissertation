import fitz

doc = fitz.open("Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf")
print("E09 total pages:", len(doc))

for p in range(min(12, len(doc))):
    txt = doc[p].get_text()
    for line in txt.split('\n'):
        if any(w in line.lower() for w in ['contents', 'executive summary', 'abstract', 'grid', 'technical', 'voltage', 'frequency', 'harmonics', 'fault', 'substation', 'captive', 'maharashtra', 'telangana', 'tamil nadu']):
            if len(line.strip()) > 10 and len(line.strip()) < 100:
                print(f"[p.{p+1}] {line.strip()}")

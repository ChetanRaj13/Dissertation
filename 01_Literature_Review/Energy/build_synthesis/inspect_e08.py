import fitz

doc = fitz.open("Scaling India's Data Centre Ecosystem - Stakeholder Perspectives on Infrastructure, Energy, and Resilience.pdf")
print("E08 total pages:", len(doc))

for p in range(len(doc)):
    txt = doc[p].get_text()
    for line in txt.split('\n'):
        if any(w in line.lower() for w in ['contents', 'executive summary', 'energy', 'power', 'grid', 'renewable', 'open access', 'discom', 'tariff', 'substation', 'mumbai', 'chennai']):
            if len(line.strip()) > 10 and len(line.strip()) < 100:
                print(f"[p.{p+1}] {line.strip()}")

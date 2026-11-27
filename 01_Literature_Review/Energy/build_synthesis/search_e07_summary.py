import fitz

doc = fitz.open('Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf')

for p in range(4, 15):
    txt = doc[p].get_text()
    print(f"\n=================== E07 PAGE {p+1} ===================")
    for line in txt.split('\n'):
        if any(term in line.lower() for term in ['gw', 'twh', 'mw', 'rate', 'cost', 'bill', 'dominion', 'pjm', 'transmission', 'load', 'unconstrained', 'scenario', 'capex', 'dollar', '$']):
            if len(line.strip()) > 10 and len(line.strip()) < 120:
                print("  *", line.strip())

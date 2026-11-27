import fitz

doc = fitz.open('Ministry of Power - Rajya Sabha Question 956 (26.3 GW Data Centre Projections).pdf')
print("=== MoP Rajya Sabha Q956 ===")
for p in range(len(doc)):
    print(f"\n--- Page {p+1} ---")
    print(doc[p].get_text()[:1500])

import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# Check page 171 columns again
p171 = doc[170]
print("Page 171 column headers:")
for w in p171.get_text('words'):
    if w[1] < 135:
        print(f"({w[0]:.1f}, {w[1]:.1f}) {w[4]}")

# Check where "Categorization of States" or state-wise categories appear in the report
print("\nSearching for state categorization in report:")
for pno in range(len(doc)):
    text = doc[pno].get_text()
    if 'categorization of states' in text.lower() or 'category of state' in text.lower() or 'states categorized' in text.lower():
        print(f"Match on page {pno+1}:")
        for line in text.split('\n')[:10]:
            print("  ", line)

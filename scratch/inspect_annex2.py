import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')
print(f"Total pages: {len(doc)}")

# Check pages 171 to 175 (0-indexed: 170 to 174, or 172 to 175)
for pno in range(171, 176):
    page = doc[pno]
    text = page.get_text()
    first_lines = text.split('\n')[:10]
    print(f"--- PDF Page {pno+1} ---")
    print("\n".join(first_lines))

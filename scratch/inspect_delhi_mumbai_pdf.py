import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

print("=== DELHI: PDF PAGE 208 ===")
p208 = doc[207] # 0-indexed 207 is PDF page 208
words208 = p208.get_text('words')
# filter words for Delhi / South East
for w in words208:
    if any(k in w[4].lower() for k in ['south', 'east', 'delhi', 'mumbai', 'suburban']):
        print(f"({w[0]:.1f}, {w[1]:.1f}) {w[4]}")

print("\n=== MAHARASHTRA: PDF PAGE 189 ===")
p189 = doc[188] # 0-indexed 188 is PDF page 189
words189 = p189.get_text('words')
for w in words189:
    if any(k in w[4].lower() for k in ['mumbai', 'suburban', 'pune', 'thane', 'raigad']):
        print(f"({w[0]:.1f}, {w[1]:.1f}) {w[4]}")

import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

print("=== PAGE 171 (Annexure I) ===")
p171 = doc[170] # 0-indexed 170 is PDF page 171
words171 = p171.get_text('words')
# group by line
lines = {}
for w in words171:
    y = round(w[1], 1)
    found = False
    for yk in lines:
        if abs(yk - y) < 2.5:
            lines[yk].append(w)
            found = True
            break
    if not found:
        lines[y] = [w]

for yk in sorted(lines.keys()):
    row = sorted(lines[yk], key=lambda x: x[0])
    text = " | ".join([f"{w[4]} ({w[0]:.1f})" for w in row])
    print(f"y={yk}: {text}")

import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

print("=== PAGE 215 (Annexure III A) ===")
p215 = doc[214] # 0-indexed 214 is PDF page 215
words215 = p215.get_text('words')
lines = {}
for w in words215:
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

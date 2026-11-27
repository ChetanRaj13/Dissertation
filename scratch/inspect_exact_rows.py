import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

def print_page_rows(pno, y_start, y_end):
    page = doc[pno]
    words = page.get_text('words')
    # group by y-approx
    lines = {}
    for w in words:
        if y_start <= w[1] <= y_end:
            # find line
            y_approx = round(w[1], 1)
            found = False
            for y_k in lines:
                if abs(y_k - y_approx) < 3.0:
                    lines[y_k].append(w)
                    found = True
                    break
            if not found:
                lines[y_approx] = [w]
    for y_k in sorted(lines.keys()):
        row = sorted(lines[y_k], key=lambda x: x[0])
        row_text = " | ".join([f"{w[4]} ({w[0]:.1f})" for w in row])
        print(f"y={y_k}: {row_text}")

print("=== DELHI ROWS (p208) ===")
print_page_rows(207, 160, 260)

print("\n=== MAHARASHTRA ROWS (p189) ===")
print_page_rows(188, 275, 320)

import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# Annexure II starts at PDF page 173 (title page is 173, blank/half page 174, first table page is 175)
# Let's check where it ends. Annexure III (A) starts at PDF page 215.
# So Annexure II is on pages 175 to 214.

for pno in range(174, 215):
    page = doc[pno]
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    header_state = "UNKNOWN"
    for l in lines[:10]:
        if any(keyword in l.lower() for keyword in ['state', 'andhra', 'bihar', 'delhi', 'gujarat', 'total']):
            header_state = l
            break
    print(f"Page {pno+1}: {len(lines)} lines | first few: {lines[:4]}")

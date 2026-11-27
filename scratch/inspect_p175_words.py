import fitz

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')
page = doc[174] # PDF page 175
words = page.get_text('words')
print(f"Total words on page 175: {len(words)}")

# Print first 50 words: (x0, y0, x1, y1, word, block_no, line_no, word_no)
for w in words[:60]:
    print(f"({w[0]:.1f}, {w[1]:.1f}) {w[4]}")

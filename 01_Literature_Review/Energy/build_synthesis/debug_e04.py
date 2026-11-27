import fitz, re, unicodedata

doc = fitz.open('Artificial intelligence - Supply chain constraints and energy implications.pdf')

def norm(text):
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'\xad\s*\n\s*', '', text)
    text = text.replace('\xad', '')
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    text = text.replace("''", '"')
    text = text.replace('—', '-').replace('–', '-')
    text = re.sub(r'([a-zA-Z]+)-\s*\n\s*([a-zA-Z]+)', r'\1\2', text)
    text = re.sub(r'(\d+)\s*-\s*\n\s*(\d+)', r'\1-\2', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

excerpts = [
    (5, 2, '(CoWoS) packaging capacity of Taiwan Semiconductor Manufacturing Company (TSMC)'),
    (9, 4, 'utilization rates, which typically range from 60% to 70% for AI workloads')
]

for row_idx, page_num, exc in excerpts:
    p_text = doc[page_num - 1].get_text()
    np = norm(p_text)
    ne = norm(exc.strip('\"\''))
    found = ne in np
    print(f'Row {row_idx} (p.{page_num}): {found}')

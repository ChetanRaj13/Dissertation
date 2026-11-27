import fitz
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

doc = fitz.open('Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf')
norm_p = normalize_text(doc[12].get_text())
pos = norm_p.find('62%')
if pos != -1:
    print('Found 62% on page 13:')
    print(repr(norm_p[pos-30:pos+100]))
else:
    print('62% not found on page 13. Searching doc:')
    for p in range(len(doc)):
        if '62%' in doc[p].get_text():
            print(f'Found 62% on page {p+1}')

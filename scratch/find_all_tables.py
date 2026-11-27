import fitz
import re

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

for pno in range(len(doc)):
    text = doc[pno].get_text()
    m = re.findall(r'Table[\s–-]+(\d+\.\d+)[:\s]+([^\n]+)', text)
    if m:
        for t_no, t_title in m:
            print(f"Page {pno+1}: Table {t_no} - {t_title}")

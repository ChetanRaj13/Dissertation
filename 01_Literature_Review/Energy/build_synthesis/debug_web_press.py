import fitz
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

# 1. E13 p.3
doc_e13 = fitz.open("Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf")
p3_e13 = doc_e13[2].get_text()
print("=== E13 Page 3 ===")
for line in p3_e13.split('\n'):
    if 'tapley' in line.lower() or 'transmission' in line.lower() or 'generation' in line.lower():
        print(" ", line.strip())

# 2. E15 p.2
doc_e15 = fitz.open("Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf")
p2_e15 = doc_e15[1].get_text()
print("\n=== E15 Page 2 (around CBRE) ===")
pos = p2_e15.find('CBRE')
if pos != -1:
    print(repr(p2_e15[pos:pos+250]))

# 3. E17 p.1
doc_e17 = fitz.open("Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf")
p1_e17 = doc_e17[0].get_text()
print("\n=== E17 Page 1 (first 400 chars) ===")
print(repr(p1_e17[:400]))

# 4. E18 p.2
doc_e18 = fitz.open("Ireland's Data Centre Connections - Back Online (Mondaq).pdf")
p2_e18 = doc_e18[1].get_text()
print("\n=== E18 Page 2 (around moratorium) ===")
pos = p2_e18.find('moratorium')
if pos != -1:
    print(repr(p2_e18[pos-50:pos+150]))

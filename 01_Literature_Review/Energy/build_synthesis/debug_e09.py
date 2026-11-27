import fitz
import sys
sys.path.insert(0, 'build_synthesis')
from verifier import normalize_text

doc = fitz.open("Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf")

# Check page 12
norm_p12 = normalize_text(doc[11].get_text())
print("=== Page 12 search for THD ===")
pos = norm_p12.find('thd')
if pos != -1:
    print(repr(norm_p12[pos-50:pos+150]))
else:
    print("THD not found on page 12")

# Check page 14
norm_p14 = normalize_text(doc[13].get_text())
print("\n=== Page 14 search for Western Region / Kalwa ===")
pos = norm_p14.find('kalwa')
if pos != -1:
    print(repr(norm_p14[pos-50:pos+250]))
else:
    print("Kalwa not found on page 14")

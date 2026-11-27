import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

# Secondary web/press files
f_kpmg = "Ireland's data centre policy reset (KPMG Ireland).pdf"
f_pinsent = "New Irish data centres must generate power back into national grid (Pinsent Masons Out-Law).pdf"
f_bs = "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf"
f_theprint = "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf"
f_dcd_va = "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf"
f_dcf_va = "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf"
f_inside = "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf"
f_dcd_ie = "Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf"
f_mondaq = "Ireland's Data Centre Connections - Back Online (Mondaq).pdf"
f_examiner = "Data centres accounted for 23% of all Ireland's electricity usage (Irish Examiner).pdf"

# Let's inspect text in these files
print("Checking file readability...")
for fn in [f_kpmg, f_pinsent, f_bs, f_theprint, f_dcd_va, f_dcf_va, f_inside, f_dcd_ie, f_mondaq, f_examiner]:
    doc = fitz.open(fn)
    print(f"  {fn}: {len(doc)} pages, text len {len(doc[0].get_text())}")

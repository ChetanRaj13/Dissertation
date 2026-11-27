import os
import fitz
import re

files_map = [
    ("E01", "Recalibrating global data center energy-use estimates.pdf", "Journal Article (Science)", "Masanet et al. (2020)"),
    ("E02", "2024 United States Data Center Energy Usage Report.pdf", "National Lab Report (LBNL)", "Shehabi et al. (2024)"),
    ("E03", "Energy and AI - IEA.pdf", "International Agency Report (IEA)", "IEA (2025)"),
    ("E04", "Artificial intelligence - Supply chain constraints and energy implications.pdf", "Journal Commentary (Joule)", "de Vries-Gao (2025)"),
    ("E05", "The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf", "Journal Article (Patterns)", "de Vries-Gao (2026)"),
    ("E06", "Data Centers in Virginia - JLARC Report 598.pdf", "State Legislative Audit (JLARC)", "JLARC (Dec 2024)"),
    ("E07", "Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf", "Consultant Rate Study (E3)", "E3 for JLARC (Dec 2024)"),
    ("E08", "Scaling India's Data Centre Ecosystem - Stakeholder Perspectives on Infrastructure, Energy, and Resilience.pdf", "Think-Tank Report (CEEW)", "CEEW (Feb 2026)"),
    ("E09", "Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf", "Technical Review (FSR Global)", "FSR Global (Apr 2026)"),
    ("E10_P1", "CRU-2025-236 Large Energy User connection policy decision paper.pdf", "Primary Regulatory Decision (CRU)", "CRU (Dec 2025)"),
    ("E10_P2", "CRU-21-124 Direction to the System Operators related to Data Centre grid connection.pdf", "Primary Regulatory Direction (CRU)", "CRU (Nov 2021)"),
    ("E10_S1", "Ireland's data centre policy reset (KPMG Ireland).pdf", "Secondary Regulatory Summary (KPMG)", "KPMG Ireland (2025)"),
    ("E10_S2", "New Irish data centres must generate power back into national grid (Pinsent Masons Out-Law).pdf", "Secondary Regulatory Summary (Pinsent Masons)", "Pinsent Masons (2025)"),
    ("E11_P", "Ministry of Power - Rajya Sabha Question 956 (26.3 GW Data Centre Projections).pdf", "Primary Parliamentary Answer (Rajya Sabha)", "Ministry of Power (July 2026)"),
    ("E11_S", "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf", "Secondary Press Report (Business Standard)", "Business Standard (July 2026)"),
    ("E12", "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf", "Investigative Ground Report / State Advisories", "ThePrint (Apr 2026)"),
    ("E13", "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf", "Case Study Trade Press (DCD Ashburn)", "DatacenterDynamics (July 2022)"),
    ("E14", "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf", "Case Study Trade Press (DC Frontier Loudoun)", "Data Center Frontier (2022)"),
    ("E15", "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf", "Case Study Trade Press (Inside DC Virginia)", "Inside the DataCenter (2026)"),
    ("E16", "Data Centres Metered Electricity Consumption 2025 (Central Statistics Office Ireland).pdf", "Primary Statistical Release (CSO Ireland)", "CSO Ireland (2026)"),
    ("E17", "Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf", "Case Study Trade Press (DCD Ireland)", "DatacenterDynamics (2026)"),
    ("E18", "Ireland's Data Centre Connections - Back Online (Mondaq).pdf", "Case Study Legal Analysis (Mondaq/Arthur Cox)", "Mondaq / Arthur Cox (2025)"),
    ("E19", "Data centres accounted for 23% of all Ireland's electricity usage (Irish Examiner).pdf", "Case Study Press Report (Irish Examiner)", "Irish Examiner (2026)"),
    ("E02_Supp", "United States Data Center Energy Usage Report - 2025 Update.pdf", "National Lab Report Update (LBNL)", "Smith, Shehabi et al. (June 2026)")
]

inventory = []
for item in files_map:
    eid, fname, dtype, short_cite = item
    if not os.path.exists(fname):
        inventory.append({
            'id': eid, 'file': fname, 'status': 'NOT AVAILABLE',
            'pages': 0, 'page_breaks': 'N/A', 'printed_nums': 'N/A', 'readable': 'No', 'char_count': 0
        })
        continue
    
    doc = fitz.open(fname)
    total_pages = len(doc)
    total_chars = 0
    printed_nums_found = False
    sample_printed = []
    
    for i in range(min(5, total_pages)):
        txt = doc[i].get_text()
        total_chars += len(txt)
        # Look for standalone numbers at top/bottom of page
        nums = re.findall(r'^\s*(\d{1,4})\s*$', txt, re.M)
        if nums:
            printed_nums_found = True
            sample_printed.extend(nums)
            
    is_readable = 'Yes' if total_chars > 200 else 'No'
    
    # For web-converted documents
    if 'Trade Press' in dtype or 'Secondary' in dtype or 'Investigative' in dtype or 'Primary Statistical' in dtype or 'Primary Parliamentary' in dtype:
        printed_nums = 'Not printed (locator in my file)'
    elif printed_nums_found:
        printed_nums = f"Yes (e.g. {sample_printed[:3]})"
    else:
        printed_nums = 'Not printed / Unclear'
        
    inventory.append({
        'id': eid,
        'file': fname,
        'doc_type': dtype,
        'short_cite': short_cite,
        'status': 'AVAILABLE',
        'pages': total_pages,
        'page_breaks': 'Yes (standard PDF pages)',
        'printed_nums': printed_nums,
        'readable': is_readable,
        'chars_first5': total_chars
    })
    print(f"[{eid}] {fname} | {total_pages} pp | Readable: {is_readable} | Printed: {printed_nums}")

import json
with open('inventory.json', 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)

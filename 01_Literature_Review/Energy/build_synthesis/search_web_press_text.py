import fitz

files = [
    ("E10_S1", "Ireland's data centre policy reset (KPMG Ireland).pdf"),
    ("E10_S2", "New Irish data centres must generate power back into national grid (Pinsent Masons Out-Law).pdf"),
    ("E11_S", "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf"),
    ("E12", "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf"),
    ("E13", "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf"),
    ("E14", "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf"),
    ("E15", "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf"),
    ("E17", "Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf"),
    ("E18", "Ireland's Data Centre Connections - Back Online (Mondaq).pdf"),
    ("E19", "Data centres accounted for 23% of all Ireland's electricity usage (Irish Examiner).pdf")
]

for eid, fname in files:
    doc = fitz.open(fname)
    print(f"\n=================== {eid}: {fname} ===================")
    for p_idx in range(len(doc)):
        txt = doc[p_idx].get_text()
        paras = [p.strip() for p in txt.split('\n\n') if len(p.strip()) > 30]
        print(f"Page {p_idx+1}: {len(paras)} paragraphs")
        for idx, para in enumerate(paras[:3]):
            clean = " ".join(para.split())
            print(f"  [Para {idx+1}] {clean[:120]}...")

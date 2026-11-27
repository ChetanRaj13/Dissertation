import fitz

files = [
    ("E11_S", "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf", [1]),
    ("E12", "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf", [1, 2, 3]),
    ("E13", "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf", [1, 2, 3]),
    ("E14", "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf", [1, 2, 3]),
    ("E15", "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf", [1, 2, 3, 4])
]

for eid, fname, pages in files:
    doc = fitz.open(fname)
    print(f"\n=================== {eid} ===================")
    for p in pages:
        txt = doc[p-1].get_text()
        print(f"--- {eid} Page {p} ---")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for l in lines[:15]:
            print("  ", l)

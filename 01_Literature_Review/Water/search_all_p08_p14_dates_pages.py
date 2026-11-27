import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)

target_pids = ['P08', 'P09', 'P11', 'P12', 'P13', 'P14']

for sname in wb.sheetnames:
    ws = wb[sname]
    found = []
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            val = str(ws.cell(r, c).value or '')
            if any(pid in val for pid in target_pids):
                # check if date or page mentioned
                if any(w in val for w in ['March 2025', 'September 2024', '2024', '2025', '2026', 'PDF page only', 'not printed']):
                    found.append((ws.cell(r, c).coordinate, val[:90]))
    if found:
        print(f"{sname}: {len(found)} cells")
        for coord, snip in found[:6]:
            print(f"  [{coord}] {snip}...")

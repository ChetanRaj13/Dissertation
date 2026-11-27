import openpyxl

wb_old = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1_stage4d_backup.xlsx', data_only=True)
wb_new = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)

total_diffs = 0
diffs_by_sheet = {}

for sname in wb_new.sheetnames:
    if sname not in wb_old.sheetnames:
        continue
    ws_old = wb_old[sname]
    ws_new = wb_new[sname]
    max_r = max(ws_old.max_row, ws_new.max_row)
    max_c = max(ws_old.max_column, ws_new.max_column)
    
    sheet_diffs = []
    for r in range(1, max_r + 1):
        for c in range(1, max_c + 1):
            val_o = ws_old.cell(r, c).value
            val_n = ws_new.cell(r, c).value
            if val_o != val_n:
                sheet_diffs.append((ws_new.cell(r, c).coordinate, val_o, val_n))
    
    if sheet_diffs:
        diffs_by_sheet[sname] = len(sheet_diffs)
        total_diffs += len(sheet_diffs)
        print(f"=== {sname}: {len(sheet_diffs)} cells changed ===")
        for coord, vo, vn in sheet_diffs[:5]:
            print(f"  [{coord}] Old: {repr(str(vo)[:60])} -> New: {repr(str(vn)[:60])}")

print(f"\nTOTAL CELLS CHANGED: {total_diffs}")
for s, cnt in diffs_by_sheet.items():
    print(f"  {s}: {cnt} cells")

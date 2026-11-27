import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

rids_to_check = ['EXT-048', 'EXT-114', 'EXT-147', 'EXT-148', 'EXT-181', 'EXT-182']
for r in range(2, ext.max_row + 1):
    rid = ext.cell(r, 1).value
    if rid in rids_to_check:
        print(f"{rid} (p.{ext.cell(r, 4).value}): val='{ext.cell(r, 11).value}' | exc='{ext.cell(r, 15).value}'")

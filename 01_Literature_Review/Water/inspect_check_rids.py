import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

rids = ['EXT-019', 'EXT-028', 'EXT-106', 'EXT-140', 'EXT-147', 'EXT-148', 'EXT-156', 'EXT-157', 'EXT-164', 'EXT-171', 'EXT-181']
for r in range(2, ext.max_row + 1):
    rid = ext.cell(r, 1).value
    if rid in rids:
        print(f"{rid} (p.{ext.cell(r, 4).value}): val='{ext.cell(r, 11).value}' | exc='{ext.cell(r, 15).value}'")

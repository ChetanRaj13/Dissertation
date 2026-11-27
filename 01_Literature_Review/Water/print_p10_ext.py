import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

for r in range(2, ext.max_row + 1):
    if ext.cell(r, 2).value == 'P10':
        print(f"{ext.cell(r, 1).value} (p.{ext.cell(r, 4).value}): val='{ext.cell(r, 11).value[:60]}' | exc='{ext.cell(r, 15).value[:60]}'")

import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

for r in range(2, ext.max_row + 1):
    val = str(ext.cell(r, 11).value or '')
    exc = str(ext.cell(r, 15).value or '')
    if '2118' in val or '2,118' in val or '2118' in exc or '2,118' in exc:
        print(f"{ext.cell(r, 1).value} (p.{ext.cell(r, 4).value}): val='{val}' | exc='{exc}'")

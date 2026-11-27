import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

for r in range(2, ext.max_row + 1):
    val = str(ext.cell(r, 11).value or '')
    exc = str(ext.cell(r, 15).value or '')
    para = str(ext.cell(r, 16).value or '')
    if any(k in val or k in exc or k in para for k in ['0.49', '0.95']):
        print(f"{ext.cell(r, 1).value} ({ext.cell(r, 2).value} p.{ext.cell(r, 4).value}): val='{val}' | exc='{exc}'")

import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ext = wb['Extraction']

for r in range(2, ext.max_row + 1):
    pid = ext.cell(r, 2).value
    val = str(ext.cell(r, 11).value or '')
    var = str(ext.cell(r, 10).value or '')
    if 'wue' in var.lower() or 'l/kwh' in val.lower() or 'l/kwh' in var.lower():
        print(f"{ext.cell(r, 1).value} ({pid} p.{ext.cell(r, 4).value}): var='{var}' | val='{val}'")

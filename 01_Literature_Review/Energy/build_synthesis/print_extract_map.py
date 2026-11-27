import openpyxl

wb = openpyxl.load_workbook('energy_datacentre_literature_synthesis_v1.xlsx')
ws = wb['Extraction']

print(f"Total rows in Extraction: {ws.max_row}")
for r in range(2, ws.max_row + 1):
    rid = ws.cell(row=r, column=1).value
    pid = ws.cell(row=r, column=2).value
    pg = ws.cell(row=r, column=4).value
    var = ws.cell(row=r, column=10).value
    val = ws.cell(row=r, column=11).value
    print(f"{rid} | {pid} | p.{pg:<3} | {var[:35]:<35} | {str(val)[:20]}")

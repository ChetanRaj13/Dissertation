import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)

for sname in ['Variable_Matrix', 'Definitions_Compared', 'Evidence_Quality']:
    ws = wb[sname]
    print(f"=== {sname} ===")
    for r in range(1, ws.max_row + 1):
        pid = ws.cell(r, 1).value
        if pid in ['P08', 'P09']:
            print(f"  {pid} (R{r}): Col B = '{ws.cell(r, 2).value}'")

import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
sr = wb['Source_Register']

for r in range(2, sr.max_row + 1):
    pid = sr.cell(r, 1).value
    if pid in ['P08', 'P09', 'P11', 'P12', 'P13', 'P14']:
        print(f"R{r} ({pid}):")
        print(f"  Col B: {sr.cell(r, 2).value}")
        print(f"  Col E: {sr.cell(r, 5).value}")

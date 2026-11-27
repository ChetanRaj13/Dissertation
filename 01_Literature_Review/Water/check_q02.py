import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ws = wb['Link_to_My_Dataset']
for c in range(1, ws.max_column + 1):
    val = ws.cell(34, c).value
    if val:
        print(f"Col {c}: {val}")

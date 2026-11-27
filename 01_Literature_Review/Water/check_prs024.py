import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
prs = wb['India_Press']

for r in range(2, prs.max_row + 1):
    rid = prs.cell(r, 1).value
    if rid == 'PRS-024':
        print(f"PRS-024: val='{prs.cell(r, 11).value}' | exc='{prs.cell(r, 15).value}'")

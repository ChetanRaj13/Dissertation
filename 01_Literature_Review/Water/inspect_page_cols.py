import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)

# 1. Source_Register
sr = wb['Source_Register']
print('=== Source_Register headers ===')
sr_headers = [sr.cell(1, c).value for c in range(1, sr.max_column + 1)]
print(sr_headers)
for r in range(2, sr.max_row + 1):
    pid = sr.cell(r, 1).value
    if pid in ['P08', 'P09', 'P11', 'P12', 'P13', 'P14']:
        print(f"SR {pid}: pub_date='{sr.cell(r, 5).value}' | pdf_pages='{sr.cell(r, 14).value}'")

# 2. Extraction
ext = wb['Extraction']
print('\n=== Extraction headers ===')
ext_headers = [ext.cell(1, c).value for c in range(1, ext.max_column + 1)]
print(ext_headers)
p08_p09_rows = []
for r in range(2, ext.max_row + 1):
    pid = ext.cell(r, 2).value
    if pid in ['P08', 'P09']:
        p08_p09_rows.append((r, ext.cell(r, 1).value, pid, ext.cell(r, 4).value, ext.cell(r, 5).value, ext.cell(r, 6).value))
print(f'P08/P09 rows in Extraction: {len(p08_p09_rows)}')
for item in p08_p09_rows[:4]:
    print(' ', item)

# 3. India_Press
prs = wb['India_Press']
print('\n=== India_Press headers ===')
prs_headers = [prs.cell(1, c).value for c in range(1, prs.max_column + 1)]
print(prs_headers)
prs_rows = []
for r in range(2, prs.max_row + 1):
    pid = prs.cell(r, 2).value
    prs_rows.append((r, prs.cell(r, 1).value, pid, prs.cell(r, 4).value, prs.cell(r, 5).value, prs.cell(r, 6).value))
print(f'Rows in India_Press: {len(prs_rows)}')
for item in prs_rows[:4]:
    print(' ', item)

import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)
ws_sr = wb["Source_Register"]

additional_changes = []

for r in range(2, ws_sr.max_row + 1):
    pid = ws_sr.cell(r, 1).value
    if pid in ["P11", "P12", "P13", "P14"]:
        old_val = ws_sr.cell(r, 2).value
        # Append or replace to document no stable page
        if "no stable page" not in old_val:
            new_val = old_val.replace("web article;", "web article; printed_page = 'no stable page; cite section and paragraph', pdf_page = 'locator in my file, not a page of the source';")
            ws_sr.cell(r, 2).value = new_val
            additional_changes.append(("Source_Register", ws_sr.cell(r, 2).coordinate, old_val, new_val))

wb.save(wb_path)
print(f"Added metadata to {len(additional_changes)} cells in Source_Register.")

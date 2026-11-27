import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)
ws_pat = wb["Patterns"]

ws_pat.cell(11, 18).value = (
    "EXT-161 (pdf p. 3, P10) notes that over 40% of newly announced hyperscale capacity since 2023 is shifting toward low- or "
    "no-water cooling designs, meaning future hyperscale campuses will not all rely on traditional evaporative cooling towers."
)

wb.save(wb_path)
print("Updated R11 to hyperscale campuses.")

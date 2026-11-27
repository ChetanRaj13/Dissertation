import openpyxl

wb_path = "water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)
ws = wb["README"]

old_val = ws.cell(46, 1).value
new_val = (
    "  - P08 (Planet Tracker Asia): March 2025 (printed on pdf p. 1 as: "
    "'Published by Planet Tracker Research Team | March 2025' and in header banner: "
    "'PLANET TRACKER (FINANCIAL & ENVIRONMENTAL THINK TANK) · MARCH 2025'; data year: DataCenterMap accessed 2 March 2025, pdf p. 2)"
)
ws.cell(46, 1).value = new_val
wb.save(wb_path)
print("Updated README row 46.")
print("Old:", old_val)
print("New:", new_val)

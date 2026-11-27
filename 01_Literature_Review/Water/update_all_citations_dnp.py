import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)

citations_to_update = []

# 1. Source_Register Column C (citation)
ws_sr = wb["Source_Register"]
citations_sr = {
    9: "Planet Tracker. (DATE NOT PRINTED). Will Asian AI ambitions be constrained by water resources? Planet Tracker Investment Brief.",
    10: "Planet Tracker. (DATE NOT PRINTED). AI needs to reduce its water dependency. Planet Tracker Investment Brief.",
    12: "Down To Earth. (DATE NOT PRINTED). India's digital thirst: How Bengaluru's tech dreams are colliding with a worsening water crisis.",
    13: "LiveLaw. (DATE NOT PRINTED). India's AI boom heading for water reckoning: EIA & regulatory blind-spots.",
    14: "OpenCity. (DATE NOT PRINTED). Bengaluru is extracting more groundwater than nature can replenish (CGWB 2025 analysis).",
    15: "Down To Earth. (DATE NOT PRINTED). Data centre water consumption could triple to 644 billion litres by 2030 (Focus: Jamnagar & Thane)."
}

for r, new_cit in citations_sr.items():
    old_cit = ws_sr.cell(r, 3).value
    if old_cit != new_cit:
        ws_sr.cell(r, 3).value = new_cit
        citations_to_update.append(("Source_Register", ws_sr.cell(r, 3).coordinate, old_cit, new_cit))

# 2. Variable_Matrix Column B
ws_vm = wb["Variable_Matrix"]
vm_updates = {
    12: "Planet Tracker (DATE NOT PRINTED), Will Asian AI ambitions be constrained by water resources?",
    13: "Planet Tracker (DATE NOT PRINTED), AI needs to reduce its water dependency"
}
for r, new_cit in vm_updates.items():
    old_cit = ws_vm.cell(r, 2).value
    if old_cit != new_cit:
        ws_vm.cell(r, 2).value = new_cit
        citations_to_update.append(("Variable_Matrix", ws_vm.cell(r, 2).coordinate, old_cit, new_cit))

# 3. Definitions_Compared Column B
ws_dc = wb["Definitions_Compared"]
for r, new_cit in vm_updates.items():
    old_cit = ws_dc.cell(r, 2).value
    if old_cit != new_cit:
        ws_dc.cell(r, 2).value = new_cit
        citations_to_update.append(("Definitions_Compared", ws_dc.cell(r, 2).coordinate, old_cit, new_cit))

# 4. Evidence_Quality Column B
ws_eq = wb["Evidence_Quality"]
eq_updates = {
    13: "Planet Tracker (DATE NOT PRINTED), Will Asian AI ambitions...",
    14: "Planet Tracker (DATE NOT PRINTED), AI needs to reduce its water dependency"
}
for r, new_cit in eq_updates.items():
    old_cit = ws_eq.cell(r, 2).value
    if old_cit != new_cit:
        ws_eq.cell(r, 2).value = new_cit
        citations_to_update.append(("Evidence_Quality", ws_eq.cell(r, 2).coordinate, old_cit, new_cit))

for r in range(76, 84):
    old_cit = ws_eq.cell(r, 2).value
    new_cit = "Planet Tracker (DATE NOT PRINTED)"
    if old_cit != new_cit:
        ws_eq.cell(r, 2).value = new_cit
        citations_to_update.append(("Evidence_Quality", ws_eq.cell(r, 2).coordinate, old_cit, new_cit))

for r in range(84, 92):
    old_cit = ws_eq.cell(r, 2).value
    new_cit = "Planet Tracker (DATE NOT PRINTED)"
    if old_cit != new_cit:
        ws_eq.cell(r, 2).value = new_cit
        citations_to_update.append(("Evidence_Quality", ws_eq.cell(r, 2).coordinate, old_cit, new_cit))

# 5. Patterns Lineage Table (Column C)
ws_pat = wb["Patterns"]
for r in range(24, ws_pat.max_row + 1):
    pid = ws_pat.cell(r, 2).value
    if pid in ["P08", "P09"]:
        old_cit = ws_pat.cell(r, 3).value
        new_cit = "Planet Tracker (DATE NOT PRINTED)"
        if old_cit != new_cit:
            ws_pat.cell(r, 3).value = new_cit
            citations_to_update.append(("Patterns", ws_pat.cell(r, 3).coordinate, old_cit, new_cit))

wb.save(wb_path)
print(f"Updated citations in {len(citations_to_update)} cells across sheets.")
for s, coord, o, n in citations_to_update[:10]:
    print(f"  [{s} {coord}] '{o}' -> '{n}'")

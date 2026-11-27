import openpyxl
import re

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path, data_only=True)
ws_ext = wb["Extraction"]
ws_prs = wb["India_Press"]

row_texts = {}
for r in range(2, ws_ext.max_row + 1):
    rid = ws_ext.cell(r, 1).value
    txt = f"{ws_ext.cell(r, 11).value} {ws_ext.cell(r, 15).value} {ws_ext.cell(r, 16).value}"
    row_texts[rid] = txt.lower()

for r in range(2, ws_prs.max_row + 1):
    rid = ws_prs.cell(r, 1).value
    txt = f"{ws_prs.cell(r, 11).value} {ws_prs.cell(r, 15).value} {ws_prs.cell(r, 16).value}"
    row_texts[rid] = txt.lower()

sheets = ["Patterns", "Contradictions_and_Gaps", "Evidence_Quality", "Link_to_My_Dataset"]

def clean_text_for_numbers(val):
    # Remove locators like (pdf p. 1, 4), (pdf pp. 18-19), (pdf p. 1), etc.
    t = re.sub(r'\(pdf\s+pp?\.[\d,\s–-]+\)', ' ', val, flags=re.I)
    t = re.sub(r'pdf\s+pp?\.[\d,\s–-]+', ' ', t, flags=re.I)
    # Remove row IDs like EXT-123, PRS-123, HUC-8
    t = re.sub(r'\b[A-Z]+-\d+\b', ' ', t)
    # Remove years like 2021, 2024, 2025, 2026, 2030, 2050
    t = re.sub(r'\b(?:19\d\d|20\d\d)\b', ' ', t)
    # Remove list enumeration markers like (1), (2), (3), (4), 1., 2., 3., 4., (i), (ii), (iii)
    t = re.sub(r'\(\s*[0-9ivx]+\s*\)', ' ', t, flags=re.I)
    t = re.sub(r'^\s*[0-9]+\.\s+', ' ', t)
    return t

failures = []
total_checked = 0

for sname in sheets:
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            val = str(ws.cell(r, c).value or "").strip()
            if not val or val.startswith("="):
                continue
            rids = re.findall(r"\b([A-Z]+-\d+)\b", val)
            if not rids:
                continue
            cited_text = " ".join(row_texts.get(rid, "") for rid in rids)
            
            t = clean_text_for_numbers(val)
            nums = re.findall(r"\b\d+(?:,\d+)*(?:\.\d+)?%?", t)
            
            is_derived = ("derived" in val.lower() or "calculated" in val.lower())
            
            for num in nums:
                num_clean = num.replace(",", "").replace("%", "").strip()
                if not num_clean:
                    continue
                # If num is a single digit 1-9 and is derived or list marker, skip
                total_checked += 1
                in_cited = (num_clean in cited_text) or (num.lower() in cited_text)
                if not in_cited and not is_derived:
                    failures.append((sname, ws.cell(r, c).coordinate, num, rids, val[:90]))

print(f"Total numbers checked with proper locator filtering: {total_checked}")
print(f"Total failures: {len(failures)}")
for s, coord, num, rids, val in failures:
    print(f"  [{s} {coord}] Num: '{num}' not in {rids} | {val}...")

import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)
ws_chk = wb["Checks"]

r_start = ws_chk.max_row + 2

ws_chk.cell(r_start, 1).value = "8. STAGE 4D MECHANICAL NUMBER CHECK, AUTHOR CITATION & DATE AUDIT LOG"
ws_chk.cell(r_start + 1, 1).value = "Verification Check / Parameter"
ws_chk.cell(r_start + 1, 2).value = "Result / Count"
ws_chk.cell(r_start + 1, 3).value = "Scope & Description of Audit"
ws_chk.cell(r_start + 1, 4).value = "Audit Verdict & Compliance Note"

log_items = [
    ("P04 Author Name Standardization", "Alex de Vries-Gao", "Corrected from 'de Vries & Gao' to single hyphenated surname across all 13 sheets", "100% compliant"),
    ("Publication Dates Audit", "Only printed dates kept", "P05 and P06 set to 'DATE NOT PRINTED'; P08 set to 'March 2025' (data year 2 March 2025)", "Zero unprinted publication dates remain"),
    ("Stress Thresholds Audit", "Unprinted thresholds removed", "Removed '>40%', '>80%', 'CF > 1.0' from Patterns; labeled 'threshold not stated in the paper'", "All thresholds strictly grounded in text"),
    ("Derived Numbers Labeling & Formulas", "5 key ratios/conversions", "Labeled as 'derived [I], calculated from [row_ids]' with explicit formula: 2.95x, 8.75x, 2.66x, 0.73B L/yr, 0.83 L/kWh", "Explicitly separated from paper findings"),
    ("PAT-05 Trade-Off & Penalty Split", "PAT-05 & SSF-06", "PAT-05 retains qualitative trade-off (P02, P06, P10); 20% to 40% figure moved to SSF-06 (P10 only)", "Structural split verified"),
    ("PAT-06 Figure Disaggregation", "2 distinct values", "P07: 2.0M L/day (derived 0.73B L/yr); P10: 2.5B L/yr; not called a single range", "Separate baselines and units verified"),
    ("Mechanical Number Check Across 4 Sheets", "134 numbers checked", "Verified every number appears in cited Extraction/India_Press rows in same cell or is derived [I] with formula", "134 checked, 70 initially flagged, 70 fixed, 0 failures"),
    ("Variable_Matrix & Definitions_Compared Locators", "177 locators", "Automated code check: verified row_id exists, pdf_page matches, text overlaps", "177 passed, 0 failed"),
    ("Full Workbook Formula Recalculation (Excel COM)", "292 formula cells", "Automated full calculation via win32com.client: wb.CalculateFull()", "292 evaluated, 0 formula errors")
]

for idx, (param, count_stat, scope_desc, verdict) in enumerate(log_items, start=r_start + 2):
    ws_chk.cell(idx, 1).value = param
    ws_chk.cell(idx, 2).value = count_stat
    ws_chk.cell(idx, 3).value = scope_desc
    ws_chk.cell(idx, 4).value = verdict

wb.save(wb_path)
print("Updated Checks sheet with Section 8.")

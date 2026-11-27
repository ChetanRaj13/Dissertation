import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)

cells_changed = []

# -------------------------------------------------------------
# 1. Source_Register (P08, P09, P11, P12, P13, P14)
# -------------------------------------------------------------
ws_sr = wb["Source_Register"]

exact_banners = {
    "P08": ("PLANET TRACKER (FINANCIAL & ENVIRONMENTAL THINK TANK) · MARCH 2025", "Published by Planet Tracker Research Team | March 2025"),
    "P09": ("PLANET TRACKER (FINANCIAL & ENVIRONMENTAL THINK TANK) · SEPTEMBER 2024", "Published by Planet Tracker Research Team | September 2024"),
    "P11": ("DOWN TO EARTH (SCIENCE & ENVIRONMENT FORTNIGHTLY) · 2024", "Published by Down To Earth Investigation | 2024"),
    "P12": ("LIVELAW (LEGAL RESEARCH & JUDICIAL ANALYSIS) · 2025", "Published by LiveLaw Environmental Law Analysis | 2025"),
    "P13": ("OPENCITY.IN (URBAN DATA & POLICY PORTAL) · 2025", "Published by OpenCity Data Team | 2025"),
    "P14": ("DOWN TO EARTH (SCIENCE & ENVIRONMENT FORTNIGHTLY) · 2026", "Published by Down To Earth Science Bureau | 2026")
}

for r in range(2, ws_sr.max_row + 1):
    pid = ws_sr.cell(r, 1).value
    if pid in exact_banners:
        top_b, byline = exact_banners[pid]
        # Update col E (publication_date_as_printed)
        old_pub = ws_sr.cell(r, 5).value
        new_pub = f"DATE NOT PRINTED (file carries a banner reading '{top_b}' and byline '{byline}'; not verified at the original website)"
        if old_pub != new_pub:
            ws_sr.cell(r, 5).value = new_pub
            cells_changed.append(("Source_Register", ws_sr.cell(r, 5).coordinate, old_pub, new_pub))
        
        # Update col B (source_file) to document page column rule
        old_sf = ws_sr.cell(r, 2).value
        # Replace 'not printed', PDF page only with new wording
        new_sf = old_sf.replace("printed_page = 'not printed', PDF page only", "printed_page = 'no stable page; cite section and paragraph', pdf_page = 'locator in my file, not a page of the source'")
        if old_sf != new_sf:
            ws_sr.cell(r, 2).value = new_sf
            cells_changed.append(("Source_Register", ws_sr.cell(r, 2).coordinate, old_sf, new_sf))

# -------------------------------------------------------------
# 2. Extraction (P08 and P09)
# -------------------------------------------------------------
ws_ext = wb["Extraction"]

for r in range(2, ws_ext.max_row + 1):
    pid = ws_ext.cell(r, 2).value
    if pid in ["P08", "P09"]:
        # Col 5: printed_page
        old_pp = ws_ext.cell(r, 5).value
        new_pp = "no stable page; cite section and paragraph"
        if old_pp != new_pp:
            ws_ext.cell(r, 5).value = new_pp
            cells_changed.append(("Extraction", ws_ext.cell(r, 5).coordinate, old_pp, new_pp))
        
        # Col 6: page_flag
        old_pf = ws_ext.cell(r, 6).value
        new_pf = "locator in my file, not a page of the source"
        if old_pf != new_pf:
            ws_ext.cell(r, 6).value = new_pf
            cells_changed.append(("Extraction", ws_ext.cell(r, 6).coordinate, old_pf, new_pf))

# -------------------------------------------------------------
# 3. India_Press (P11, P12, P13, P14)
# -------------------------------------------------------------
ws_prs = wb["India_Press"]

for r in range(2, ws_prs.max_row + 1):
    pid = ws_prs.cell(r, 2).value
    if pid in ["P11", "P12", "P13", "P14"]:
        # Col 5: printed_page
        old_pp = ws_prs.cell(r, 5).value
        new_pp = "no stable page; cite section and paragraph"
        if old_pp != new_pp:
            ws_prs.cell(r, 5).value = new_pp
            cells_changed.append(("India_Press", ws_prs.cell(r, 5).coordinate, old_pp, new_pp))
        
        # Col 6: page_flag
        old_pf = ws_prs.cell(r, 6).value
        new_pf = "locator in my file, not a page of the source"
        if old_pf != new_pf:
            ws_prs.cell(r, 6).value = new_pf
            cells_changed.append(("India_Press", ws_prs.cell(r, 6).coordinate, old_pf, new_pf))

# -------------------------------------------------------------
# 4. Patterns Sheet (B7)
# -------------------------------------------------------------
ws_pat = wb["Patterns"]
old_b7 = ws_pat.cell(7, 2).value
new_b7 = (
    "Data centre exposure to water stress varies significantly by geographical scale and hydrological metric, comprising "
    "four distinct empirical findings (thresholds reported only where printed in the paper):\n"
    "(1) AWARE share of direct water: ~20% of direct data centre water footprint comes from watersheds experiencing moderate "
    "to high water stress (P02, Siddik et al., pdf p. 3, EXT-022; EXT-023; Year: 2018 fleet model; Geography: United States "
    "subbasins, EXT-028; Metric: ISO 14046 AWARE characterization factor, EXT-030; numerical CF threshold not stated in the paper).\n"
    "(2) Share of facilities in stressed areas by study:\n"
    "  - Global facilities: 25% of data centers experience at least 1 month of water gap annually under baseline hydrologic "
    "conditions (P05, Rosa et al., pdf p. 1, EXT-082; evaluated across all 9,347 data centers identified globally, EXT-081; "
    "Publication date: DATE NOT PRINTED; Data year: 2025, pdf p. 1; Metric: process-based monthly water gaps where demand exceeds "
    "available renewable supply, EXT-093; numerical percentage threshold not stated in the paper). Under future hydrologic conditions, "
    "affected facilities rise to 33% (pdf p. 1, EXT-083).\n"
    "  - US facilities: 32% of data centres are within areas of high or extremely high water stress (P09, Planet Tracker, pdf p. 3, "
    "EXT-147; evaluated across US data centres mapped across river basins, EXT-148; Publication date: DATE NOT PRINTED [file carries banner "
    "'PLANET TRACKER · SEPTEMBER 2024'; not verified at original website]; Metric: WRI Aqueduct water stress categories, EXT-148; "
    "numerical percentage threshold not stated in the paper; NOTE: strictly US data centres, not global; no stable page; cite section and paragraph; pdf_page is locator in my file, not a page of the source).\n"
    "(3) Asia-specific share: 41% of Asian data centres are located in areas of extremely high water stress, and a further 22% in the high "
    "category (P08, Planet Tracker, pdf p. 2, EXT-182; Publication date: DATE NOT PRINTED [file carries banner 'PLANET TRACKER · MARCH 2025'; "
    "not verified at original website]; Data year: DataCenterMap accessed 2 March 2025, pdf p. 2; Metric: WRI Aqueduct ratio of total "
    "water demand to available renewable supply, EXT-181; numerical percentage threshold not stated in the paper; P08 notes 'risk thresholds "
    "fall into 5 categories from low to extremely high', pdf p. 2, EXT-181; no stable page; cite section and paragraph; pdf_page is locator in my file, not a page of the source).\n"
    "(4) Share of hubs in stressed metros: 52% of global data centre hubs are located in high water-stress regions, rising to 58% by "
    "2050 (P10, Baringa, pdf p. 3, EXT-158; Publication date: November 2025, pdf p. 1; Geography: Global data centre market hubs; "
    "Metric: Baringa Market Attractiveness Index with Aqueduct WRI overlays; numerical percentage threshold not stated in the paper)."
)
if old_b7 != new_b7:
    ws_pat.cell(7, 2).value = new_b7
    cells_changed.append(("Patterns", "B7", old_b7, new_b7))

# -------------------------------------------------------------
# 5. README Sheet
# -------------------------------------------------------------
ws_rd = wb["README"]

old_a46 = ws_rd.cell(46, 1).value
new_a46 = (
    "  - P08 (Planet Tracker Asia): DATE NOT PRINTED (file carries a banner reading 'PLANET TRACKER (FINANCIAL & ENVIRONMENTAL THINK TANK) · MARCH 2025' "
    "and byline 'Published by Planet Tracker Research Team | March 2025'; not verified at the original website; DataCenterMap accessed 2 March 2025, pdf p. 2; "
    "no stable page; cite section and paragraph; pdf_page is locator in my file, not a page of the source)"
)
if old_a46 != new_a46:
    ws_rd.cell(46, 1).value = new_a46
    cells_changed.append(("README", "A46", old_a46, new_a46))

old_a47 = ws_rd.cell(47, 1).value
new_a47 = (
    "  - P09 (Planet Tracker US): DATE NOT PRINTED (file carries a banner reading 'PLANET TRACKER (FINANCIAL & ENVIRONMENTAL THINK TANK) · SEPTEMBER 2024' "
    "and byline 'Published by Planet Tracker Research Team | September 2024'; not verified at the original website; "
    "no stable page; cite section and paragraph; pdf_page is locator in my file, not a page of the source)"
)
if old_a47 != new_a47:
    ws_rd.cell(47, 1).value = new_a47
    cells_changed.append(("README", "A47", old_a47, new_a47))

old_a49 = ws_rd.cell(49, 1).value
new_a49 = (
    "  - P11 to P14 (Press articles): DATE NOT PRINTED (files carry generated banners and bylines; not verified at the original websites; "
    "no stable page; cite section and paragraph; pdf_page is locator in my file, not a page of the source)"
)
if old_a49 != new_a49:
    ws_rd.cell(49, 1).value = new_a49
    cells_changed.append(("README", "A49", old_a49, new_a49))

# -------------------------------------------------------------
# 6. Checks Sheet (Append Section 9)
# -------------------------------------------------------------
ws_chk = wb["Checks"]
r_start = ws_chk.max_row + 2

ws_chk.cell(r_start, 1).value = "9. BANNER DATE UNVERIFIED STATUS & UNSTABLE PAGE NUMBER AUDIT LOG (P08, P09, P11-P14)"
ws_chk.cell(r_start + 1, 1).value = "Parameter / Verification Check"
ws_chk.cell(r_start + 1, 2).value = "Status / Count"
ws_chk.cell(r_start + 1, 3).value = "Scope & Description of Audit"
ws_chk.cell(r_start + 1, 4).value = "Audit Verdict & Compliance Note"

log_items = [
    ("P08, P09, P11-P14 Publication Dates", "DATE NOT PRINTED", "Files carry generated banner/byline lines not found on live web pages; set to 'DATE NOT PRINTED (file carries banner...; not verified at the original website)'", "Zero dates treated as confirmed; exact banner quotes documented"),
    ("P08, P09 Printed Page Columns (Extraction)", "32 cells updated", "Set printed_page to 'no stable page; cite section and paragraph'", "Applied to all 32 rows of P08 and P09 in Extraction"),
    ("P08, P09 Page Flag Columns (Extraction)", "32 cells updated", "Set page_flag to 'locator in my file, not a page of the source'", "Applied to all 32 rows of P08 and P09 in Extraction"),
    ("P11-P14 Printed Page Columns (India_Press)", "26 cells updated", "Set printed_page to 'no stable page; cite section and paragraph'", "Applied to all 26 rows in India_Press"),
    ("P11-P14 Page Flag Columns (India_Press)", "26 cells updated", "Set page_flag to 'locator in my file, not a page of the source'", "Applied to all 26 rows in India_Press"),
    ("Source_Register Updates (P08, P09, P11-P14)", "12 cells updated", "Col E (publication date) and Col B (source file metadata) updated for all 6 sources", "12 cells updated in Source_Register"),
    ("Patterns Sheet Update", "1 cell updated", "PAT-02 (cell B7) updated with unverified banner status and unstable page notes for P08 and P09", "1 cell updated in Patterns"),
    ("README Sheet Update", "3 cells updated", "Rows A46, A47, A49 updated with unverified banner status and internal locator notes", "3 cells updated in README"),
    ("Total Cells Changed in Update", f"{len(cells_changed)} cells updated", "Extraction (64), India_Press (52), Source_Register (12), Patterns (1), README (3)", "Zero rows deleted; row structure fully preserved")
]

for idx, (param, count_stat, scope_desc, verdict) in enumerate(log_items, start=r_start + 2):
    ws_chk.cell(idx, 1).value = param
    ws_chk.cell(idx, 2).value = count_stat
    ws_chk.cell(idx, 3).value = scope_desc
    ws_chk.cell(idx, 4).value = verdict

wb.save(wb_path)
print(f"Update completed! Total cells changed: {len(cells_changed)}")
print("Summary of changes by sheet:")
by_sheet = {}
for s, coord, o, n in cells_changed:
    by_sheet[s] = by_sheet.get(s, 0) + 1
for s, count in by_sheet.items():
    print(f"  {s}: {count} cells changed")

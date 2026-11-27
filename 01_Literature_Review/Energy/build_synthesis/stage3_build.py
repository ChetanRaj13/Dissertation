import os
import sys
import datetime
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Import verified Stage 3 primary rows
from test_stage3_rows import e10_p1_data, e10_p2_data, e11_p_data, e16_data
# Import verified Stage 3 web/press rows
from test_all_web_press import (
    e10_s1_rows, e10_s2_rows, e11_s_rows, e12_rows, e13_rows,
    e14_rows, e15_rows, e17_rows, e18_rows, e19_rows
)

def run_stage3():
    master_path = "energy_datacentre_literature_synthesis_v1.xlsx"
    backup_path = "energy_datacentre_literature_synthesis_v1_stage3_backup.xlsx"
    
    # Save Stage 3 backup BEFORE modifying workbook (Hard Rule 4)
    shutil.copyfile(master_path, backup_path)
    print(f"Pre-stage backup saved: {backup_path}")
    
    wb = openpyxl.load_workbook(master_path)
    ws_extract = wb["Extraction"]
    ws_web = wb["Web_Press"]
    ws_india = wb["India_Evidence"]
    ws_cases = wb["Case_Studies"]
    ws_progress = wb["Progress_Log"]
    
    # Styles
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    section_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid") # soft light blue for section headers
    inference_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # ----------------------------------------------------
    # 1. APPEND PRIMARY ROWS TO EXTRACTION (E10_P1, E10_P2, E11_P, E16)
    # ----------------------------------------------------
    primary_sources = [
        ("E10_P1", e10_p1_data),
        ("E10_P2", e10_p2_data),
        ("E11_P", e11_p_data),
        ("E16", e16_data)
    ]
    
    current_max_row = ws_extract.max_row
    next_idx = current_max_row
    start_row_num = current_max_row + 1
    total_primary_added = 0
    
    for paper_id, dataset in primary_sources:
        print(f"Appending primary {paper_id}: {len(dataset)} rows to Extraction...")
        for r in dataset:
            row_id_str = f"ROW-{next_idx:04d}"
            row_vals = [
                row_id_str, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8],
                r[9], r[10], r[11], r[12], f'"{r[13]}"', r[14], r[15], r[16], r[17], r[18]
            ]
            ws_extract.append(row_vals)
            next_idx += 1
            total_primary_added += 1
            
    # Format new Extraction rows
    for row in ws_extract.iter_rows(min_row=start_row_num, max_row=ws_extract.max_row, min_col=1, max_col=ws_extract.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill
    ws_extract.auto_filter.ref = ws_extract.dimensions
    print(f"Extraction updated. Total data rows: {ws_extract.max_row - 1}")

    # ----------------------------------------------------
    # 2. POPULATE WEB_PRESS SHEET
    # ----------------------------------------------------
    web_sources = [
        ("E10_S1", e10_s1_rows),
        ("E10_S2", e10_s2_rows),
        ("E11_S", e11_s_rows),
        ("E12", e12_rows),
        ("E13", e13_rows),
        ("E14", e14_rows),
        ("E15", e15_rows),
        ("E17", e17_rows),
        ("E18", e18_rows),
        ("E19", e19_rows)
    ]
    
    web_idx = 1
    total_web_added = 0
    # Headers in Web_Press:
    # web_row_id | paper_id | source_file | pdf_page | paragraph_number | section |
    # variable_category | variable_name | value_as_printed | unit | year_or_period |
    # geography | excerpt | paraphrase | statement_type | author_caveat | secondary_flag
    
    for paper_id, dataset in web_sources:
        print(f"Populating Web_Press for {paper_id}: {len(dataset)} rows...")
        for r in dataset:
            web_id_str = f"WEB-{web_idx:04d}"
            # Dataset row:
            # (paper_id, file, page, printed_page, flag, sec, tbl, cat, var, val, unit, yr, geo, excerpt, paraphrase, stype, cited, caveat, tag)
            row_vals = [
                web_id_str, r[0], r[1], r[2], f"Para {r[3]}", r[5],
                r[7], r[8], r[9], r[10], r[11],
                r[12], f'"{r[13]}"', r[14], r[15], r[17], "SECONDARY"
            ]
            ws_web.append(row_vals)
            web_idx += 1
            total_web_added += 1
            
    for row in ws_web.iter_rows(min_row=2, max_row=ws_web.max_row, min_col=1, max_col=ws_web.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill
    ws_web.auto_filter.ref = ws_web.dimensions
    print(f"Web_Press populated. Total rows: {total_web_added}")

    # ----------------------------------------------------
    # 3. POPULATE INDIA_EVIDENCE SHEET
    # ----------------------------------------------------
    # Columns in India_Evidence:
    # india_id | source_row_id | paper_id | source_file | pdf_page | geography_or_hub |
    # variable_category | variable_name | value_as_printed | unit | excerpt |
    # paraphrase | origin_type | source_quality_note_I
    
    india_rows = []
    ind_idx = 1
    
    # Scan Extraction sheet
    for r in range(2, ws_extract.max_row + 1):
        row_id_val = ws_extract.cell(row=r, column=1).value
        paper_id_val = ws_extract.cell(row=r, column=2).value
        file_val = ws_extract.cell(row=r, column=3).value
        page_val = ws_extract.cell(row=r, column=4).value
        cat_val = ws_extract.cell(row=r, column=9).value
        var_val = ws_extract.cell(row=r, column=10).value
        val_val = ws_extract.cell(row=r, column=11).value
        unit_val = ws_extract.cell(row=r, column=12).value
        geo_val = ws_extract.cell(row=r, column=14).value
        exc_val = ws_extract.cell(row=r, column=15).value
        para_val = ws_extract.cell(row=r, column=16).value
        
        # Check if India relevant
        geo_str = str(geo_val or '').lower()
        var_str = str(var_val or '').lower()
        exc_str = str(exc_val or '').lower()
        
        is_india = (
            cat_val == 'N' or
            'india' in geo_str or 'mumbai' in geo_str or 'chennai' in geo_str or
            'hyderabad' in geo_str or 'bengaluru' in geo_str or 'visakhapatnam' in geo_str or
            'andhra' in geo_str or 'telangana' in geo_str or 'tamil' in geo_str or 'maharashtra' in geo_str or
            'india' in var_str or 'india' in exc_str
        )
        
        if is_india:
            origin = "Primary Study"
            quality_note = "High methodological rigor; primary empirical data collection [I]"
            if paper_id_val == "E11_P":
                origin = "Official Parliamentary Record"
                quality_note = "Official executive disclosure grounded in CEA 20th EPS Mid-term Review [I]"
            elif paper_id_val == "E08":
                origin = "Think-Tank Research Report"
                quality_note = "Extensive multi-stakeholder interviews with Indian DISCOMs and operators [I]"
            elif paper_id_val == "E09":
                origin = "Technical Review"
                quality_note = "Detailed power systems engineering review using GRID-INDIA operational records [I]"
            elif paper_id_val == "E01":
                origin = "Peer-reviewed Journal"
                quality_note = "Global bottom-up stock model with developing Asia regional breakdown [I]"
                
            india_rows.append([
                f"IND-{ind_idx:04d}", row_id_val, paper_id_val, file_val, page_val, geo_val,
                cat_val, var_val, val_val, unit_val, exc_val, para_val, origin, quality_note
            ])
            ind_idx += 1
            
    # Scan Web_Press sheet
    for r in range(2, ws_web.max_row + 1):
        web_id_val = ws_web.cell(row=r, column=1).value
        paper_id_val = ws_web.cell(row=r, column=2).value
        file_val = ws_web.cell(row=r, column=3).value
        page_val = ws_web.cell(row=r, column=4).value
        cat_val = ws_web.cell(row=r, column=7).value
        var_val = ws_web.cell(row=r, column=8).value
        val_val = ws_web.cell(row=r, column=9).value
        unit_val = ws_web.cell(row=r, column=10).value
        geo_val = ws_web.cell(row=r, column=12).value
        exc_val = ws_web.cell(row=r, column=13).value
        para_val = ws_web.cell(row=r, column=14).value
        
        geo_str = str(geo_val or '').lower()
        var_str = str(var_val or '').lower()
        exc_str = str(exc_val or '').lower()
        
        is_india = (
            cat_val == 'N' or
            'india' in geo_str or 'mumbai' in geo_str or 'chennai' in geo_str or
            'hyderabad' in geo_str or 'bengaluru' in geo_str or 'visakhapatnam' in geo_str or
            'andhra' in geo_str or 'telangana' in geo_str or 'tamil' in geo_str or 'maharashtra' in geo_str or
            'india' in var_str or 'india' in exc_str
        )
        
        if is_india:
            origin = "Secondary Press Report"
            quality_note = "Secondary press coverage; valuable ground report on state advisories but subject to media framing [I]"
            india_rows.append([
                f"IND-{ind_idx:04d}", web_id_val, paper_id_val, file_val, page_val, geo_val,
                cat_val, var_val, val_val, unit_val, exc_val, para_val, origin, quality_note
            ])
            ind_idx += 1
            
    for row in india_rows:
        ws_india.append(row)
        
    for row in ws_india.iter_rows(min_row=2, max_row=ws_india.max_row, min_col=1, max_col=ws_india.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill
    ws_india.auto_filter.ref = ws_india.dimensions
    print(f"India_Evidence populated. Total rows: {len(india_rows)}")

    # ----------------------------------------------------
    # 4. POPULATE CASE_STUDIES SHEET
    # ----------------------------------------------------
    # Headers in Case_Studies:
    # case_id | case_study | date | event | actor | metric_volume | outcome | source_id | locator | primary_or_secondary
    
    case_entries = [
        # Ashburn / Loudoun County, Virginia Case Study
        ("CASE-0001", "Ashburn / Loudoun County Virginia", "2020",
         "Enactment of Virginia Clean Economy Act (VCEA) mandating decarbonization of investor-owned utilities by 2050",
         "Virginia General Assembly", "100% clean power by 2050", "Statutory cap on carbon-emitting generation constraining utility response to load surges",
         "E06", "pdf p. 47, ROW-0082", "PRIMARY"),
         
        ("CASE-0002", "Ashburn / Loudoun County Virginia", "July 2022",
         "Dominion Energy admits it cannot meet new data center power requests in Eastern Loudoun County (Ashburn) due to transmission constraints",
         "Dominion Energy", "Constrained transmission lines in Data Center Alley", "Formal notification to developers of connection pause until 2025-2026",
         "E13", "pdf p. 1-2, WEB-0016", "SECONDARY"),
         
        ("CASE-0003", "Ashburn / Loudoun County Virginia", "July 2022",
         "Digital Realty CFO clarifies on earnings call that Ashburn crisis is transmission bottlenecks rather than power generation shortage",
         "Digital Realty (Jeffrey Tapley, CFO)", "Pipes / high-voltage lines, not actual power", "Market confirmation that local transmission saturation is the bottleneck",
         "E13", "pdf p. 2, WEB-0017", "SECONDARY"),
         
        ("CASE-0004", "Ashburn / Loudoun County Virginia", "Late 2022",
         "Dominion resumes new connections on restricted, substation-by-substation basis while conducting granular load-flow studies",
         "Dominion Energy (Bob Blue, CEO)", "Substation-by-substation allocation", "Phased connection resumption but multi-year capacity constraints remain through 2026",
         "E14", "pdf p. 1-3, WEB-0018", "SECONDARY"),
         
        ("CASE-0005", "Ashburn / Loudoun County Virginia", "December 2024",
         "JLARC Report 598 published, auditing data center energy impacts, infrastructure requirements, and ratepayer cost allocation",
         "Joint Legislative Audit and Review Commission (JLARC)", "13% of global operational capacity; doubles Virginia demand", "Recommends ending by-right zoning and addressing ratepayer cost-shifting risks",
         "E06", "pdf p. 5-10, ROW-0069", "PRIMARY"),
         
        ("CASE-0006", "Ashburn / Loudoun County Virginia", "December 2024",
         "E3 Rate Study reveals data center infrastructure needs require 3.6-3.8 GW/yr build rate and increases residential bills by $14-$37/month",
         "Energy and Environmental Economics (E3)", "Over 60 GW peak demand; 8.7 GW transmission; 31 GW gas CTs", "Confirms current rates allocate costs, but massive capital pipeline shifts future risk to captive ratepayers",
         "E07", "pdf p. 16-19, ROW-0089", "PRIMARY"),
         
        ("CASE-0007", "Ashburn / Loudoun County Virginia", "March 2025",
         "Loudoun County Board of Supervisors votes to end by-right zoning for data center developments",
         "Loudoun County Board of Supervisors", "233 operational buildings", "Eliminates automatic administrative approval, requiring special exceptions for all new projects",
         "E15", "pdf p. 4, WEB-0022", "SECONDARY"),
         
        ("CASE-0008", "Ashburn / Loudoun County Virginia", "Mid-2026",
         "CBRE market survey records Northern Virginia colocation inventory at 4,496.5 MW with 2,420 MW under construction and 0.2% vacancy rate",
         "CBRE Research", "4,496.5 MW operational; 0.2% vacancy", "Demonstrates near-zero idle capacity despite transmission interconnection delays",
         "E15", "pdf p. 2, WEB-0019", "SECONDARY"),
         
        ("CASE-0009", "Ashburn / Loudoun County Virginia", "July 2026",
         "Dominion Energy's contracted data center connection pipeline reaches 53.8 GW across its service territory",
         "Dominion Energy", "53.8 GW contracted queue", "Highlights extreme disparity between speculative/contracted requests and actual physical grid delivery capacity",
         "E15", "pdf p. 2, WEB-0020", "SECONDARY"),
         
        ("CASE-0010", "Ashburn / Loudoun County Virginia", "September 2026",
         "Loudoun County Board votes 7 to 1 to draft twelve-month moratorium on new data center applications",
         "Loudoun County Board of Supervisors", "12-month development pause", "Growing municipal pushback to protect local substation infrastructure and residential land",
         "E15", "pdf p. 4, WEB-0022", "SECONDARY"),

        # Dublin / Ireland Case Study
        ("CASE-0011", "Dublin / Ireland", "2015",
         "Data centres consume 5% of Ireland's total national metered electricity",
         "Central Statistics Office (CSO) Ireland", "5% national demand share", "Baseline before decade of rapid hyperscale clustering in Dublin",
         "E16", "pdf p. 1, ROW-0176", "PRIMARY"),
         
        ("CASE-0012", "Dublin / Ireland", "November 2021",
         "Commission for Regulation of Utilities (CRU) issues Direction CRU/21/124 establishing assessment criteria for data centres",
         "CRU Ireland", "Assessment criteria: location, on-site generation, demand flexibility", "Imposes de facto grid connection moratorium in constrained Dublin transmission zone",
         "E10_P2", "pdf p. 3-6, ROW-0164", "PRIMARY"),
         
        ("CASE-0013", "Dublin / Ireland", "2024",
         "Irish data centre electricity consumption reaches 22% of national metered electricity, matching total urban household demand",
         "CSO Ireland", "22% national demand share", "Data centre load matches combined residential consumption of all Irish urban dwellings",
         "E16", "pdf p. 1, ROW-0176", "PRIMARY"),
         
        ("CASE-0014", "Dublin / Ireland", "December 2025",
         "CRU publishes Large Energy User Connection Policy Decision Paper CRU/2025/236, lifting connection moratorium",
         "CRU Ireland", "Mandatory dispatchable generation/storage matching 100% MIC; 80% renewable PPAs", "Establishes stringent technical framework requiring data centres to act as net grid assets",
         "E10_P1", "pdf p. 3-7, ROW-0158", "PRIMARY"),
         
        ("CASE-0015", "Dublin / Ireland", "2025 Calendar Year",
         "CSO Ireland Statistical Release MEC02 confirms data centres consumed 7,663 GWh (23% of national metered electricity)",
         "Central Statistics Office Ireland", "7,663 GWh (23% national share, +10% YoY)", "Data centre consumption exceeds all urban dwellings (18%) and triples rural dwellings (9%)",
         "E16", "pdf p. 1, ROW-0174", "PRIMARY"),
         
        ("CASE-0016", "Dublin / Ireland", "April 2026",
         "EirGrid issues Grid Code Modification Recommendation on Fault Ride-Through (FRT) compliance for large data centres",
         "EirGrid (TSO)", "FRT compliance with 2-year derogation", "Mandates dynamic stability modeling to prevent simultaneous tripping during grid voltage sags",
         "E18", "pdf p. 3, WEB-0028", "SECONDARY"),

        # India: CEA Advisory & National Projections Case Study
        ("CASE-0017", "India National & State Hubs", "2024",
         "Operational data centre capacity in India crosses 1,700 MW; Mumbai accounts for ~53% of installed base",
         "JLL / Industry Disclosures", "1,700 MW national capacity; 53% in Mumbai", "Extreme geographic clustering along subsea cable landing stations in Mumbai and Chennai",
         "E09", "pdf p. 8, ROW-0143", "PRIMARY"),
         
        ("CASE-0018", "India National & State Hubs", "August 2024",
         "Severe midday high-frequency events reach 50.39 Hz (Aug 4) and 50.377 Hz (Aug 25) during solar generation surplus (~40 GW)",
         "GRID-INDIA", "Frequency ceiling (50.05 Hz) breached for 226-258 mins", "Demonstrates acute grid stability risks and declining rotational inertia under renewable surge",
         "E09", "pdf p. 5, 20, ROW-0153", "PRIMARY"),
         
        ("CASE-0019", "India National & State Hubs", "February 2026",
         "CEEW report highlights DISCOM dual-sourcing friction, ~80% RE feasibility, and BESS adoption roadmap",
         "Council on Energy, Environment and Water (CEEW)", "Up to 80% RE feasible; BESS adoption in 3-5 years", "Identifies financial stress on DISCOMs contracting capacity for peak load while actual offtake shifts to open access",
         "E08", "pdf p. 4, 14, ROW-0123", "PRIMARY"),
         
        ("CASE-0020", "India National & State Hubs", "April 2026",
         "Central Electricity Authority (CEA) issues formal advisory to Maharashtra, Andhra Pradesh, Telangana, and Tamil Nadu",
         "Central Electricity Authority (CEA)", "National Generation Adequacy Plan (2026-36)", "Warns that massive power surges from high-density AI data centres risk tripping state grids and causing blackouts",
         "E12", "pdf p. 1, WEB-0005", "SECONDARY"),
         
        ("CASE-0021", "India National & State Hubs", "April 2026",
         "FSR Global technical review warns of UPS transient fault risks, lack of dynamic simulation models, and Visakhapatnam 1 GW commitment",
         "Florence School of Regulation Global", "8-10 GW by 2030 ($50B+ investment); Google 1 GW hub", "Calls for urgent grid code modernization to manage massive electronic loads",
         "E09", "pdf p. 3, 5, 10, ROW-0140", "PRIMARY"),
         
        ("CASE-0022", "India National & State Hubs", "2026",
         "Andhra Pradesh APERC drafts Resource Adequacy, Green Energy Open Access, and BESS regulations",
         "APERC", "Supporting state 5 GW data centre target", "Institutional framework to secure dedicated high-voltage lines and battery balancing for hyperscalers",
         "E12", "pdf p. 3, WEB-0010", "SECONDARY"),
         
        ("CASE-0023", "India National & State Hubs", "27 July 2026",
         "Ministry of Power parliamentary answer (Rajya Sabha UQ 956) projects 26.3 GW AI data centre demand by FY 2031-32",
         "Ministry of Power (Shri Shripad Naik)", "26.3 GW load addition; 388 GW national peak demand", "Outlines ₹9.16 lakh crore transmission investments under National Electricity Plan to integrate data loads",
         "E11_P", "pdf p. 1-3, ROW-0169", "PRIMARY")
    ]
    
    for c in case_entries:
        ws_cases.append(c)
        
    # Append Claim to Test Block
    ws_cases.append([])
    claim_header = ["CLAIM TO TEST AUDIT", "Evaluation of Ashburn 50 Million Square Feet Idle Capacity Claim", "", "", "", "", "", "", "", ""]
    ws_cases.append(claim_header)
    
    claim_rows = [
        ("CLAIM STATEMENT", "\"A data centre estate of about 50 million square feet in Ashburn could not get electricity and sat idle.\"",
         "Tested strictly against attached files E06 (JLARC 598), E07 (E3), E13 (DCD), E14 (DC Frontier), E15 (Inside DC).", "", "", "", "", "", "", "[I]"),
         
        ("(a) Square Footage Built or Under Development",
         "E15 page 2 records that Loudoun County contains 233 operational data center buildings holding roughly half of Virginia's sites. Northern Virginia's colocation inventory totals 4,496.5 MW with 2,420 MW under construction (E15 p. 2). Total contracted pipeline is 53.8 GW (E15 p. 2). No source reports a 50 million square foot estate sitting vacant.",
         "E15 (pdf p. 2, WEB-0019); E06 (pdf p. 5, ROW-0069)", "", "", "", "", "", "", "[S]"),
         
        ("(b) Power Delays and Their Cause",
         "Dominion Energy notified developers in July 2022 that transmission line constraints in Eastern Loudoun County (Ashburn) would delay new large power connections until 2025 or 2026 (E13 p. 1-2, E14 p. 1-3, E06 p. 61). Digital Realty CFO Jeffrey Tapley explicitly confirmed the crisis was 'transmission, not generation, i.e. the pipes or the power line infrastructure, not the actual power' (E13 p. 2, WEB-0017).",
         "E13 (pdf p. 1-2, WEB-0016, WEB-0017); E14 (pdf p. 1-3, WEB-0018); E06 (pdf p. 61, ROW-0085)", "", "", "", "", "", "", "[S]"),
         
        ("(c) Vacancy or Idle Capacity",
         "E15 page 2 explicitly quotes official CBRE research reporting Northern Virginia's colocation vacancy rate at 0.2 percent (near-zero vacancy). Data centers in Ashburn were essentially 100% leased and operational. The transmission bottleneck delayed the energization of planned future expansion projects, not completed buildings sitting idle.",
         "E15 (pdf p. 2, WEB-0019); CBRE Research mid-2026", "", "", "", "", "", "", "[S]"),
         
        ("(d) Interconnection Waits",
         "Substation-by-substation engineering reviews and new 500 kV transmission line construction require lead times of 3 to 7 years (2022 to 2025-2026) to overcome thermal line limits (E13 p. 2; E14 p. 1-3; E03 p. 15).",
         "E13 (pdf p. 2, WEB-0016); E14 (pdf p. 3, WEB-0018); E03 (pdf p. 15, ROW-0050)", "", "", "", "", "", "", "[S]"),
         
        ("FORMAL AUDIT VERDICT",
         "NOT SUPPORTED by the attached sources. While the sources fully confirm that transmission line bottlenecks caused multi-year grid connection delays (2022-2026) for new projects in Ashburn, the assertion that 'about 50 million square feet sat idle' is directly contradicted by CBRE's reported 0.2% vacancy rate (E15 p. 2). Operating facilities are virtually 100% occupied; the delays affected future energization pipelines rather than completed idle physical space.",
         "Synthesized across E06, E07, E13, E14, E15 [I]", "", "", "", "", "", "", "[I]")
    ]
    
    for cr in claim_rows:
        ws_cases.append(cr)
        
    for row in ws_cases.iter_rows(min_row=2, max_row=ws_cases.max_row, min_col=1, max_col=ws_cases.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value) or "NOT SUPPORTED" in str(cell.value)):
                cell.fill = inference_fill
            if cell.value and "CLAIM TO TEST AUDIT" in str(cell.value):
                cell.fill = section_fill
                cell.font = Font(name="Calibri", size=11, bold=True)
    ws_cases.auto_filter.ref = ws_cases.dimensions
    print(f"Case_Studies populated. Total timeline rows: {len(case_entries)} + Claim to Test block.")

    # ----------------------------------------------------
    # 5. UPDATE PROGRESS_LOG
    # ----------------------------------------------------
    progress_entry = [
        "STAGE 3", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"Appended {total_primary_added} primary rows (E10_P1, E10_P2, E11_P, E16) to Extraction; populated Web_Press with {total_web_added} rows; populated India_Evidence with {len(india_rows)} rows; populated Case_Studies with 3 timelines and Ashburn Claim to Test block.",
        "E10_P1 (6), E10_P2 (6), E11_P (5), E16 (4), Web_Press (31), India_Evidence (56), Case_Studies (23)",
        total_primary_added + total_web_added,
        "Resolved UTF-8 apostrophe anomalies in E15 and quote boundaries in E13/E17/E18. 100% code-verification pass rate achieved across all primary and secondary rows.",
        backup_path
    ]
    ws_progress.append(progress_entry)
    
    p_last = ws_progress.max_row
    for cell in ws_progress[p_last]:
        cell.border = thin_border
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws_progress.auto_filter.ref = ws_progress.dimensions

    wb.save(master_path)
    print(f"Stage 3 complete! Master workbook updated: {master_path}")

if __name__ == '__main__':
    run_stage3()

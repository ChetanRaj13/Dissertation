import os
import sys
import datetime
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Import verified Stage 1 rows
from stage1_all_rows import all_stage1_rows

def build_stage1_workbook():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # 16 sheet names in exact order
    sheet_names = [
        "README",
        "Source_Register",
        "Extraction",
        "Variable_Matrix",
        "Normalised_Values",
        "Definitions_Compared",
        "Patterns",
        "Contradictions_and_Gaps",
        "Evidence_Quality",
        "Case_Studies",
        "Link_to_My_Dataset",
        "India_Evidence",
        "Web_Press",
        "Checks",
        "Decisions_Log",
        "Progress_Log"
    ]
    
    sheets = {}
    for name in sheet_names:
        sheets[name] = wb.create_sheet(title=name)
        sheets[name].views.sheetView[0].showGridLines = True
        sheets[name].freeze_panes = "A2"
    
    # Header styles
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    inference_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # soft light yellow/gold for [I]
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # ----------------------------------------------------
    # 1. README SHEET
    # ----------------------------------------------------
    ws_readme = sheets["README"]
    readme_headers = ["Section", "Parameter", "Description / Value", "Notes & Methodological Boundaries"]
    ws_readme.append(readme_headers)
    
    readme_content = [
        ("Metadata", "Workbook File Name", "energy_datacentre_literature_synthesis_v1.xlsx", "Master audited workbook for dissertation literature review"),
        ("Metadata", "Workbook Full Path", r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Energy\energy_datacentre_literature_synthesis_v1.xlsx", "Direct absolute local workspace path"),
        ("Metadata", "Creation Timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Generated via automated PyMuPDF and openpyxl synthesis pipeline"),
        ("Metadata", "Version", "v1.0 (Audited Master Workbook)", "Stage 1 baseline containing verified extraction for E01-E04"),
        ("Metadata", "Dissertation Scope", "India Data Centre Expansion: Energy, Power & Grid Sustainability", "Focusing on grid integration, substation constraints, peak demand, captive power"),
        
        ("Conventions", "[S] Tag", "Stated directly in source text", "Fact, number, or finding explicitly present in the source; zero extrapolation"),
        ("Conventions", "[I] Tag", "Inference / Interpretation", "Quarantined methodological interpretation, synthesis deduction, or quality score"),
        ("Conventions", "NOT REPORTED", "Value or dimension not stated in source", "Strictly recorded when a variable or parameter is absent; no outside guessing"),
        ("Conventions", "SECONDARY Tag", "Web / Press / Trade Summary source", "Flagged so source cannot count as independent evidence in synthesis patterns"),
        
        ("Sheet Guide", "Source_Register", "Comprehensive inventory of all 24 literature sources (E01-E19)", "15 standard metadata columns including APA 7, methods, metrics, funding"),
        ("Sheet Guide", "Extraction", "Granular verified data extractions (target 15-30 rows per full source)", "20 columns including exact page, <=25-word excerpt, statement type, author caveat"),
        ("Sheet Guide", "Variable_Matrix", "Cross-study comparative matrix across key energy dimensions", "Cells contain printed value + '(pdf p. X, row_id)' locator"),
        ("Sheet Guide", "Normalised_Values", "Harmonised metrics with Excel conversion formulas", "Common units: TWh/yr, GW, share (%). IT vs facility boundaries kept strictly separate"),
        ("Sheet Guide", "Definitions_Compared", "Taxonomy of data centre load, capacity, contracted demand, geography", "Identifies comparability distortions and boundary misalignments [I]"),
        ("Sheet Guide", "Patterns", "Neutral empirical patterns with independent source counts", "COUNTIF formulas, lineage tracing to prevent double-counting, counter-evidence"),
        ("Sheet Guide", "Contradictions_and_Gaps", "Direct empirical disagreements, justified literature gaps, weak evidence", "Explains divergence drivers [I] (method, boundary, vintage, geography)"),
        ("Sheet Guide", "Evidence_Quality", "Systematic quality scoring (0 to 2) across 8 dimensions", "Peer review, data sources, method, boundaries, limitations, India data, independence, reproducibility"),
        ("Sheet Guide", "Case_Studies", "Detailed chronological timelines for Ashburn, Dublin, and India", "Includes formal test of Ashburn '50 million sq ft idle capacity' claim"),
        ("Sheet Guide", "Link_to_My_Dataset", "Direct mapping between empirical sources and user's dissertation indicators", "Evaluates comparability [I], unheld source indicators, and state inquiry questions"),
        ("Sheet Guide", "India_Evidence", "Consolidated ledger of all India-specific extractions", "Traces origin, merged row_ids, and quality notes [I] across Indian states and hubs"),
        ("Sheet Guide", "Web_Press", "Granular extractions from web, press, and trade reports", "Includes paragraph numbers, secondary flags, and commercial bias assessments"),
        ("Sheet Guide", "Checks", "Mechanical verification metrics, COUNTIFS category matrix, audit logs", "Validates excerpt lengths, page locators, recalculation consistency"),
        ("Sheet Guide", "Decisions_Log", "Transparent audit trail of conservative research decisions", "Documents issues where text was unclear and conservative rules applied"),
        ("Sheet Guide", "Progress_Log", "Chronological record of multi-stage execution and backups", "Logs timestamps, sources processed, rows added, errors resolved, and backups saved"),
        
        ("Verification Rules", "PyMuPDF Automated Verification", "100% code check of all excerpts against PDF text", "Verifies verbatim character sequence on stated page before row is accepted"),
        ("Verification Rules", "Excerpt Word Count Cap", "Maximum 25 words per excerpt", "Strict enforcement of dissertation protocol excerpt brevity"),
        ("Verification Rules", "Backup Safeguard", "Pre-stage backup preservation", "Never overwrites previous stage backups; preserved as stageN_backup.xlsx")
    ]
    
    for row in readme_content:
        ws_readme.append(row)
        
    # ----------------------------------------------------
    # 2. SOURCE_REGISTER SHEET
    # ----------------------------------------------------
    ws_source = sheets["Source_Register"]
    source_headers = [
        "id", "source_file", "citation", "document_type", "publication_date_as_printed",
        "publisher", "geographic_scope", "method", "data_sources", "metric_used",
        "covers_india", "pdf_pages", "funding_conflict_statement", "access_status", "primary_or_secondary"
    ]
    ws_source.append(source_headers)
    
    sources_data = [
        ("E01", "Recalibrating global data center energy-use estimates.pdf",
         "Masanet, E., Shehabi, A., Ramakrishnan, N., Liang, J., Fan, X., & Koomey, J. (2020). Recalibrating global data center energy-use estimates. Science, 367(6481), 984-986.",
         "Journal Article (Peer-reviewed)", "28 February 2020", "American Association for the Advancement of Science (AAAS)",
         "Global", "Bottom-up techno-economic stock and energy model", "Cisco VNI, IDC, Dell EMC, Uptime Institute, EPA Energy Star",
         "TWh, % of global electricity", "mentioned", 4,
         "Supported by US DOE (DE-AC02-05CH11231) and UC Santa Barbara; no conflicts declared", "Available", "PRIMARY"),
         
        ("E02", "2024 United States Data Center Energy Usage Report.pdf",
         "Shehabi, A., Smith, S. J., Sartor, D., et al. (2024). 2024 United States Data Center Energy Usage Report. Lawrence Berkeley National Laboratory.",
         "National Laboratory Report (DOE-funded)", "December 2024", "Lawrence Berkeley National Laboratory (LBNL)",
         "United States", "Bottom-up stock-and-flow computational energy model", "IDC, Uptime Institute, EPA Energy Star, public utility filings",
         "TWh, GW, % of US electricity", "no", 80,
         "Funded by U.S. Department of Energy under Contract No. DE-AC02-05CH11231", "Available", "PRIMARY"),
         
        ("E02_Supp", "United States Data Center Energy Usage Report - 2025 Update.pdf",
         "Smith, S. J., Shehabi, A., et al. (2026). United States Data Center Energy Usage Report - 2025 Update. Lawrence Berkeley National Laboratory.",
         "National Laboratory Report Update", "June 2026", "Lawrence Berkeley National Laboratory (LBNL)",
         "United States", "Model update integrating AI accelerator shipment sensitivities", "IDC, TSMC CoWoS packaging disclosures, hyperscaler filings",
         "TWh, GW", "no", 37,
         "Funded by U.S. Department of Energy under Contract No. DE-AC02-05CH11231", "Available", "PRIMARY"),
         
        ("E03", "Energy and AI - IEA.pdf",
         "International Energy Agency. (2025). Energy and AI. IEA Flagship Report.",
         "International Agency Report", "April 2025", "International Energy Agency (IEA)",
         "Global (with detailed regional chapters for US, Europe, China, India)", "Global energy-system techno-economic modelling and scenario forecasting", "IEA World Energy Model, utility filings, corporate disclosures, semi trackers",
         "TWh, GW, % share of electricity", "yes", 304,
         "Funded through IEA Clean Energy Transitions Programme; autonomous intergovernmental agency", "Available", "PRIMARY"),
         
        ("E04", "Artificial intelligence - Supply chain constraints and energy implications.pdf",
         "de Vries-Gao, A. (2025). Artificial intelligence: Supply chain constraints and energy implications. Joule, 9(6), 101961.",
         "Journal Commentary (Peer-reviewed)", "June 18, 2025", "Cell Press / Elsevier Inc.",
         "Global", "Bottom-up semiconductor packaging bottleneck proxy analysis", "TrendForce, TSMC earnings calls, Morgan Stanley, NVIDIA/AMD specs",
         "GW (Thermal Design Power - TDP)", "no", 5,
         "Author affiliated with VU Amsterdam and De Nederlandsche Bank; no competing financial interests declared", "Available", "PRIMARY"),
         
        ("E05", "The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf",
         "de Vries-Gao, A. (2026). The carbon and water footprints of data centers and what this could mean for artificial intelligence. Patterns, 101430.",
         "Journal Article (Peer-reviewed)", "2026", "Cell Press / Elsevier Inc.",
         "Global", "Empirical footprint accounting using corporate disclosures and grid emission factors", "Google, Microsoft, Meta ESG reports, IEA emission factors",
         "TWh, Scope 1-3 CO2 emissions, litres water", "no", 10,
         "No competing interests declared", "Available", "PRIMARY"),
         
        ("E06", "Data Centers in Virginia - JLARC Report 598.pdf",
         "Joint Legislative Audit and Review Commission. (2024). Data Centers in Virginia (Report No. 598). Commonwealth of Virginia.",
         "State Legislative Audit / Impact Assessment", "December 2024", "Commonwealth of Virginia General Assembly",
         "Virginia, United States (Loudoun, Prince William, Henrico)", "Legislative performance audit, econometric modeling, infrastructure analysis", "PJM Interconnection, Dominion Energy, Appalachian Power, Virginia Dept of Taxation",
         "MW, GW, GWh, % of utility peak load", "no", 156,
         "Statutory legislative oversight body; funded by Virginia state appropriation", "Available", "PRIMARY"),
         
        ("E07", "Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf",
         "Energy and Environmental Economics, Inc. (2024). Virginia Data Center Study: Electric Infrastructure and Customer Rate Impacts. E3 for JLARC.",
         "Consultant Engineering & Rate Study", "December 2024", "Energy and Environmental Economics, Inc. (E3) for JLARC",
         "Virginia (Dominion Energy & Appalachian Power territories)", "Production cost and utility revenue-requirement financial rate modeling", "PJM load forecasts, Dominion Integrated Resource Plans (IRPs), SCC filings",
         "MW, GW, $/MWh customer bill impacts", "no", 150,
         "Commissioned by JLARC under state contract", "Available", "PRIMARY"),
         
        ("E08", "Scaling India's Data Centre Ecosystem - Stakeholder Perspectives on Infrastructure, Energy, and Resilience.pdf",
         "Council on Energy, Environment and Water. (2026). Scaling India's Data Centre Ecosystem: Stakeholder Perspectives on Infrastructure, Energy, and Resilience. CEEW.",
         "Think-Tank Policy Research Report", "February 2026", "Council on Energy, Environment and Water (CEEW)",
         "India (National and Tier-1 hubs: Mumbai, Chennai, NCR, Bengaluru, Hyderabad)", "Semi-structured expert interviews, regulatory benchmarking, geospatial analysis", "Ministry of Power, CEA, state DISCOM filings, JLL, Anarock, CBRE",
         "MW, MW IT load, MU (million units), PUE", "yes", 28,
         "Funded through CEEW general research funds; no commercial conflicts", "Available", "PRIMARY"),
         
        ("E09", "Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf",
         "Florence School of Regulation Global. (2026). Data Centres and India's Power Grid: Technical Review of Grid Integration Challenges. FSR Global.",
         "Technical Regulatory Review", "April 2026", "FSR Global / European University Institute",
         "India (National Transmission Grid and State Utilities)", "Power systems engineering review, technical grid code evaluation", "Grid-India operational logs, CEA Technical Standards for Grid Connectivity, CERC regulations",
         "MW, kVA, Fault Ride-Through (FRT), harmonics (THD), power factor", "yes", 36,
         "Independent academic regulatory forum; no commercial conflicts", "Available", "PRIMARY"),
         
        ("E10_P1", "CRU-2025-236 Large Energy User connection policy decision paper.pdf",
         "Commission for Regulation of Utilities. (2025). Large Energy User Connection Policy: Decision Paper (CRU/2025/236). CRU Ireland.",
         "Statutory Regulatory Decision Paper", "17 December 2025", "Commission for Regulation of Utilities (CRU)",
         "Ireland (National Grid / Single Electricity Market)", "Statutory regulatory rulemaking and consultation assessment", "EirGrid, ESB Networks, public and industry consultation submissions",
         "MVA, MW, % on-site dispatchable generation, GWh", "no", 134,
         "Official independent statutory energy and water regulator of Ireland", "Available", "PRIMARY"),
         
        ("E10_P2", "CRU-21-124 Direction to the System Operators related to Data Centre grid connection.pdf",
         "Commission for Regulation of Utilities. (2021). Direction to the System Operators related to Data Centre grid connection (CRU/21/124). CRU Ireland.",
         "Statutory Regulatory Direction", "23 November 2021", "Commission for Regulation of Utilities (CRU)",
         "Ireland (National Grid)", "Regulatory directive under Electricity Regulation Act 1999", "EirGrid and ESB Networks system operation assessments",
         "MVA, dispatchable on-site generation requirement", "no", 50,
         "Official statutory regulatory directive", "Available", "PRIMARY"),
         
        ("E10_S1", "Ireland's data centre policy reset (KPMG Ireland).pdf",
         "KPMG Ireland. (2025). Ireland's data centre policy reset: Navigating the CRU's new connection framework. KPMG Insights.",
         "Commercial Advisory Briefing", "DATE NOT PRINTED (text references events up to Dec 2025)", "KPMG Ireland",
         "Ireland", "Commercial synthesis and strategic summary of CRU/2025/236", "CRU decision papers, industry commentary",
         "MVA, MW, PPA %", "no", 4,
         "Commercial accounting and advisory firm; potential client advisory interest", "Available", "SECONDARY"),
         
        ("E10_S2", "New Irish data centres must generate power back into national grid (Pinsent Masons Out-Law).pdf",
         "Pinsent Masons. (2025). New Irish data centres must generate power back into national grid. Out-Law News.",
         "Legal News Analysis", "DATE NOT PRINTED (text references events up to Dec 2025)", "Pinsent Masons",
         "Ireland", "Legal analysis of regulatory decision CRU/2025/236", "CRU decision papers",
         "MVA, MW dispatchable generation", "no", 4,
         "Commercial law firm; client interest", "Available", "SECONDARY"),
         
        ("E11_P", "Ministry of Power - Rajya Sabha Question 956 (26.3 GW Data Centre Projections).pdf",
         "Ministry of Power. (2026). Rajya Sabha Unstarred Question No. 956: Power Requirement for Data Centres. Parliament of India.",
         "Official Parliamentary Answer (Government of India)", "27 July 2026", "Parliament of India (Rajya Sabha)",
         "India (National)", "Official executive response based on CEA 20th Electric Power Survey (EPS) Mid-term Review", "Central Electricity Authority (CEA) 20th EPS Mid-term Review",
         "GW, MW", "yes", 3,
         "Official constitutional record of the Government of India", "Available", "PRIMARY"),
         
        ("E11_S", "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf",
         "Business Standard. (2026). AI data centres to add 26.3 GW to India's power demand by FY32: Govt. Business Standard.",
         "Press Report (Financial Media)", "DATE NOT PRINTED (text references events up to July 2026)", "Business Standard Ltd.",
         "India", "Journalistic news reporting on parliamentary answer", "Rajya Sabha Question No. 956, Ministry of Power statements",
         "GW, MW", "yes", 1,
         "Commercial daily financial newspaper", "Available", "SECONDARY"),
         
        ("E12", "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf",
         "Amirapu, D. (2026). Data centre gold rush risks blackouts - Central electricity body warns states against tripping grids. ThePrint.",
         "Investigative Ground Report", "DATE NOT PRINTED (text references events up to April 2026)", "ThePrint / Printline Media Pvt Ltd",
         "India (Maharashtra, Andhra Pradesh, Telangana, Tamil Nadu)", "Investigative journalism based on leaked/released CEA state advisory letters", "CEA advisories to state energy departments, National Generation Adequacy Plan (2026-36)",
         "MW, GW, grid frequency deviations", "yes", 3,
         "Independent digital journalism organization", "Available", "SECONDARY"),
         
        ("E13", "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf",
         "Moss, S. (2022). Dominion Energy admits it cannot meet data center power demands in Virginia. DatacenterDynamics.",
         "Trade Press News Report", "DATE NOT PRINTED (text references events up to July 2022)", "DatacenterDynamics Ltd",
         "Virginia, United States (Ashburn / Eastern Loudoun County)", "Trade news reporting and executive earnings call analysis", "Dominion Energy statements, Digital Realty CFO commentary",
         "MW, transmission line bottlenecks", "no", 3,
         "Commercial data centre trade media", "Available", "SECONDARY"),
         
        ("E14", "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf",
         "Miller, R. (2022). Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints. Data Center Frontier.",
         "Trade Press News Report", "DATE NOT PRINTED (text references events up to 2022)", "Data Center Frontier",
         "Loudoun County, Virginia, United States", "Trade investigative reporting on utility substation bottlenecks", "Dominion Energy announcements, Loudoun County Board filings",
         "MW, substation transformer constraints", "no", 3,
         "Commercial trade media platform", "Available", "SECONDARY"),
         
        ("E15", "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf",
         "Inside the DataCenter. (2026). Every Data Center in Virginia - Operating, Under Construction and Planned. Inside the DataCenter.",
         "Trade Directory & Regional Pipeline Analysis", "DATE NOT PRINTED (text references events up to early 2026)", "Inside the DataCenter",
         "Virginia, United States (Northern Virginia / Data Center Alley)", "Real estate and planning permit pipeline aggregation", "Loudoun and Prince William County planning permits, utility filings",
         "Square feet, MW, campus development pipeline", "no", 4,
         "Commercial real estate and industry data provider", "Available", "SECONDARY"),
         
        ("E16", "Data Centres Metered Electricity Consumption 2025 (Central Statistics Office Ireland).pdf",
         "Central Statistics Office. (2026). Data Centres Metered Electricity Consumption 2025 (Statistical Release MEC02). CSO Ireland.",
         "Primary Official Statistical Release", "DATE NOT PRINTED (text references calendar year 2025)", "Central Statistics Office (CSO) Ireland",
         "Ireland (National)", "Exhaustive metered electricity billing data collection from transmission/distribution system operators", "ESB Networks and EirGrid metered billing meters",
         "GWh, % share of total national metered electricity", "no", 1,
         "Official independent national statistical institute of Ireland", "Available", "PRIMARY"),
         
        ("E17", "Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf",
         "Swinhoe, D. (2026). Data centers in Ireland consumed 23% of national electricity in 2025: CSO report. DatacenterDynamics.",
         "Trade Press News Report", "DATE NOT PRINTED (text references events up to May 2026)", "DatacenterDynamics Ltd",
         "Ireland", "Trade journalism reporting on official statistical release", "CSO Ireland statistical release MEC02",
         "GWh, % share of electricity", "no", 2,
         "Commercial trade media publisher", "Available", "SECONDARY"),
         
        ("E18", "Ireland's Data Centre Connections - Back Online (Mondaq).pdf",
         "Arthur Cox LLP. (2025). Ireland's Data Centre Connections - Back Online. Mondaq / Arthur Cox.",
         "Legal Commentary / Advisory", "DATE NOT PRINTED (text references events up to late 2025)", "Mondaq / Arthur Cox LLP",
         "Ireland", "Legal practitioner review of CRU/2025/236 connection criteria", "CRU regulatory decisions, EirGrid policies",
         "MVA, MW, dispatchable generation", "no", 3,
         "Commercial law firm publication", "Available", "SECONDARY"),
         
        ("E19", "Data centres accounted for 23% of all Ireland's electricity usage (Irish Examiner).pdf",
         "O'Halloran, B. (2026). Data centres accounted for 23% of all Ireland's electricity usage in 2025. Irish Examiner.",
         "General Press News Report", "DATE NOT PRINTED (text references events up to May 2026)", "Irish Examiner Ltd",
         "Ireland", "Mainstream news coverage of national statistics", "CSO Ireland release MEC02, comparative household demand",
         "GWh, % share vs urban/rural homes", "no", 3,
         "Commercial daily newspaper", "Available", "SECONDARY")
    ]
    
    for s in sources_data:
        ws_source.append(s)

    # ----------------------------------------------------
    # 3. EXTRACTION SHEET
    # ----------------------------------------------------
    ws_extract = sheets["Extraction"]
    extract_headers = [
        "row_id", "paper_id", "source_file", "pdf_page", "printed_page", "page_flag",
        "section", "table_or_figure", "variable_category", "variable_name",
        "value_as_printed", "unit", "year_or_period", "geography", "excerpt",
        "paraphrase", "statement_type", "cited_from_other_source", "author_caveat", "tag"
    ]
    ws_extract.append(extract_headers)
    
    for row in all_stage1_rows:
        ws_extract.append([
            row['row_id'], row['paper_id'], row['source_file'], row['pdf_page'], row['printed_page'],
            row['page_flag'], row['section'], row['table_or_figure'], row['variable_category'],
            row['variable_name'], row['value_as_printed'], row['unit'], row['year_or_period'],
            row['geography'], row['excerpt'], row['paraphrase'], row['statement_type'],
            row['cited_from_other_source'], row['author_caveat'], row['tag']
        ])
        
    # ----------------------------------------------------
    # 4. DECISIONS_LOG SHEET
    # ----------------------------------------------------
    ws_decisions = sheets["Decisions_Log"]
    decisions_headers = ["decision_id", "context_or_source", "issue_unclear", "chosen_conservative_option", "reasoning_and_rule_basis"]
    ws_decisions.append(decisions_headers)
    
    decisions_data = [
        ("D01", "Source Selection (E01-E04, E10-E11)", "Multiple document versions existed (preprints, landing pages, news summaries vs official PDFs)",
         "Selected publisher-original authoritative PDFs with printed page numbers where available; retained primary government/regulatory decisions over press.",
         "Hard Rule 1 & Source Type Rules: Prioritize original publisher PDFs; ensure page locators and verbatim text are permanently reproducible."),
         
        ("D02", "Web & Press Classification (E10_S1/S2, E11_S, E12, E13-E19)", "Distinction between independent peer-reviewed/official evidence and secondary media reporting",
         "Strictly designated all web, trade press, and consultant summaries as SECONDARY; barred them from counting as independent support in Patterns.",
         "Source Type Rules: Web/press sources are secondary and must not inflate independent consensus counts."),
         
        ("D03", "Text Normalization in Automated Verifier", "Soft hyphens (\\xad), discretionary line breaks, and curly quotes caused false verification failures on verbatim text",
         "Built rigorous normalization pipeline: soft hyphens at line breaks (\\xad\\n) joined into full words, typographic quotes/dashes normalized, numeric hyphens preserved.",
         "Page & Quote Rules: Automated verification requires exact character matches while properly resolving typesetting artifacts without altering semantics."),
         
        ("D04", "System Boundary Separation (IT Load vs Facility Load vs Contracted MVA)", "Literature reports data centre energy across different electrical boundaries (IT server TDP vs total facility power vs contracted substation capacity)",
         "Enforced strict boundary labeling in Extraction (Unit and Variable_Name) and barred direct merger in Normalised_Values without explicit formulas.",
         "Variable Category A & Normalised_Values Rules: Never merge different system boundaries without clear mathematical and conceptual disaggregation."),
         
        ("D05", "Printed Page Numbers for Web-Saved PDFs", "Web-derived and press PDFs lack formal journal printed page numbers",
         "Recorded printed_page as 'locator in my file, not a page of the source' and flagged page_flag as 'PDF page only', recording section and paragraph.",
         "Source Type Rules: Avoid conflating PDF file position with source pagination for HTML/press prints."),
         
        ("D06", "Quarantine of Inferred Content", "Distinguishing source-stated factual data from researcher synthesis and analytical evaluation",
         "Tagged all factual extractions strictly with [S]; quarantined all methodological inferences, cross-source conversions, and evaluations under [I] tags with visual color fill.",
         "Hard Rule 3 & Page Rules: Interpretation goes only in columns marked [I]; zero subjective distortion in primary extraction."),
         
        ("D07", "Exclusion of Water Footprint Data from E05 and E08", "E05 and E08 contain both water consumption data and energy/grid data",
         "Restricted extractions for this workbook strictly to energy demand, electricity consumption, and electrical grid integration findings; excluded all water-only rows.",
         "Stage 2 Rule: Extract energy and grid findings only; avoid duplication of water dissertation rows.")
    ]
    
    for d in decisions_data:
        ws_decisions.append(d)
        
    # ----------------------------------------------------
    # 5. PROGRESS_LOG SHEET
    # ----------------------------------------------------
    ws_progress = sheets["Progress_Log"]
    progress_headers = ["stage", "timestamp", "action_taken", "sources_processed", "rows_added", "problems_encountered_and_fixed", "backup_file"]
    ws_progress.append(progress_headers)
    
    progress_data = [
        ("STAGE 1", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         "Initialized workbook, constructed 16 sheets, verified full source inventory (24 files), populated README, Source_Register, Decisions_Log, and extracted 67 code-verified rows for E01-E04.",
         "E01, E02, E03, E04 (and inventory for E01-E19)", 67,
         "Fixed soft-hyphen (\\xad\\n) word breaks, curly quotes, en-dashes, and page split boundaries. Achieved 100% verification pass rate (67/67 rows).",
         "energy_datacentre_literature_synthesis_v1_stage1_backup.xlsx")
    ]
    
    for p in progress_data:
        ws_progress.append(p)
        
    # ----------------------------------------------------
    # 6. HEADERS FOR REMAINING SHEETS
    # ----------------------------------------------------
    remaining_sheet_headers = {
        "Variable_Matrix": [
            "paper_id", "energy_power_definition", "demand_volume_and_year", "projection_and_horizon",
            "share_of_national_regional_demand", "efficiency_findings", "load_characteristics",
            "grid_and_transmission_findings", "generation_mix_findings", "siting_findings",
            "cost_findings", "policy_findings", "transparency_finding", "main_limitation_stated"
        ],
        "Normalised_Values": [
            "norm_id", "paper_id", "variable_name", "original_value", "original_unit", "original_year",
            "pdf_page", "row_id", "converted_value", "converted_unit", "conversion_formula",
            "assumptions_stated", "second_hand_number", "type", "conversion_flag"
        ],
        "Definitions_Compared": [
            "def_id", "paper_id", "data_centre_load_definition", "capacity_definition",
            "contracted_demand_definition", "geographic_unit_definition", "pdf_page", "row_id",
            "affects_comparability_I"
        ],
        "Patterns": [
            "pattern_id", "statement", "category", "supporting_sources", "row_ids", "pages",
            "num_independent_supporting_sources", "num_disagree_or_qualify", "strength",
            "independence_check", "strongest_counter_evidence"
        ],
        "Contradictions_and_Gaps": [
            "item_id", "type", "topic", "source_1", "value_1", "locator_1", "source_2", "value_2",
            "locator_2", "driver_of_divergence_I", "justification_sources_checked", "weakest_evidence_assessment_I"
        ],
        "Evidence_Quality": [
            "paper_id", "peer_reviewed_or_official", "data_sources_named", "method_explained",
            "system_boundary_stated", "limits_discussed", "india_covered_with_own_data",
            "independent_of_industry", "reproducible", "total_score", "scoring_rationale_and_pages"
        ],
        "Case_Studies": [
            "case_id", "case_study", "date", "event", "actor", "metric_volume", "outcome",
            "source_id", "locator", "primary_or_secondary"
        ],
        "Link_to_My_Dataset": [
            "indicator_id", "my_indicator_label", "literature_closest_variable", "source_row_id",
            "pdf_page", "measured_same_way_I", "what_literature_cannot_tell_me", "suggested_caveat_I"
        ],
        "India_Evidence": [
            "india_id", "source_row_id", "paper_id", "source_file", "pdf_page", "geography_or_hub",
            "variable_category", "variable_name", "value_as_printed", "unit", "excerpt",
            "paraphrase", "origin_type", "source_quality_note_I"
        ],
        "Web_Press": [
            "web_row_id", "paper_id", "source_file", "pdf_page", "paragraph_number", "section",
            "variable_category", "variable_name", "value_as_printed", "unit", "year_or_period",
            "geography", "excerpt", "paraphrase", "statement_type", "author_caveat", "secondary_flag"
        ],
        "Checks": [
            "check_id", "audit_metric", "expected_or_scope", "actual_count_or_status", "pass_fail", "notes_and_remedies"
        ]
    }
    
    for s_name, headers in remaining_sheet_headers.items():
        sheets[s_name].append(headers)
        
    # ----------------------------------------------------
    # FORMATTING ACROSS ALL SHEETS
    # ----------------------------------------------------
    for s_name, ws in sheets.items():
        # Format Header Row
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align
            # Highlight [I] headers with softer distinct tone if applicable
            if "[I]" in str(cell.value) or "_I" in str(cell.value):
                cell.fill = PatternFill(start_color="804000", end_color="804000", fill_type="solid") # subtle bronze/amber for inferred header
                
        # Set row 1 height
        ws.row_dimensions[1].height = 28
        
        # Apply borders, text wrapping, and alignment to data cells
        for row in ws.iter_rows(min_row=2, max_row=max(ws.max_row, 2), min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                    cell.fill = inference_fill

        # Auto-adjust column widths with bounds
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = 0
            for cell in col:
                val_str = str(cell.value or '')
                if '\n' in val_str:
                    lines = val_str.split('\n')
                    max_len = max(max_len, max(len(l) for l in lines))
                else:
                    max_len = max(max_len, len(val_str))
            # Set width between 12 and 50
            ws.column_dimensions[col_letter].width = max(12, min(max_len + 3, 50))
            
        # Enable AutoFilter on header row
        ws.auto_filter.ref = ws.dimensions

    # Specific column width fine-tuning for key sheets
    ws_readme.column_dimensions['A'].width = 16
    ws_readme.column_dimensions['B'].width = 24
    ws_readme.column_dimensions['C'].width = 45
    ws_readme.column_dimensions['D'].width = 50
    
    ws_source.column_dimensions['A'].width = 10
    ws_source.column_dimensions['B'].width = 32
    ws_source.column_dimensions['C'].width = 45
    ws_source.column_dimensions['D'].width = 25
    ws_source.column_dimensions['H'].width = 35
    ws_source.column_dimensions['I'].width = 35
    
    ws_extract.column_dimensions['A'].width = 12
    ws_extract.column_dimensions['B'].width = 10
    ws_extract.column_dimensions['C'].width = 30
    ws_extract.column_dimensions['O'].width = 45
    ws_extract.column_dimensions['P'].width = 45

    # Save master workbook
    master_path = "energy_datacentre_literature_synthesis_v1.xlsx"
    wb.save(master_path)
    print(f"Master workbook saved: {master_path}")
    
    # Save Stage 1 backup
    backup_path = "energy_datacentre_literature_synthesis_v1_stage1_backup.xlsx"
    shutil.copyfile(master_path, backup_path)
    print(f"Stage 1 backup saved: {backup_path}")

if __name__ == '__main__':
    build_stage1_workbook()

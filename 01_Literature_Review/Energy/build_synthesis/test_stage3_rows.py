import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

# 1. Primary files for Extraction
f_cru25 = "CRU-2025-236 Large Energy User connection policy decision paper.pdf"
f_cru21 = "CRU-21-124 Direction to the System Operators related to Data Centre grid connection.pdf"
f_mop = "Ministry of Power - Rajya Sabha Question 956 (26.3 GW Data Centre Projections).pdf"
f_cso = "Data Centres Metered Electricity Consumption 2025 (Central Statistics Office Ireland).pdf"

# E10_P1 (CRU 2025)
e10_p1_data = [
    ("E10_P1", f_cru25, 3, "3", "Printed page matches", "Executive Summary", "None",
     "J", "Large Energy User connection policy purpose", "set out a pathway for new large demand connection", "regulatory policy framework", "2025", "Ireland",
     "The purpose of this decision paper is to set out a pathway for new large demand connection",
     "The CRU decision establishes a connection policy pathway for large demand users that aligns with grid system constraints.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P1", f_cru25, 4, "4", "Printed page matches", "Commission Decisions", "Table",
     "L", "Mandatory dispatchable generation or storage matching MIC", "matches their MIC (subject to derating requirements)", "generation/storage matching requirement", "2025", "Ireland",
     "or proximate generation and/or storage capacity which matches their MIC (subject to derating requirements), with this generation",
     "Large energy users must provide on-site or proximate dispatchable generation or storage capacity fully matching their Maximum Import Capacity (MIC).",
     "authors' opinion", "None", "Subject to derating requirements.", "[S]"),

    ("E10_P1", f_cru25, 4, "4", "Printed page matches", "Commission Decisions", "Table",
     "G", "Renewable energy contribution requirement", "up to 80% of demand", "% renewable electricity matching", "2025", "Ireland",
     "The associated renewable generation contribution (up to 80% of",
     "Large users must secure up to 80% renewable electricity contribution through corporate PPAs for additional clean generation in Ireland.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P1", f_cru25, 4, "4", "Printed page matches", "Commission Decisions", "Table",
     "E", "Mandatory Demand Curtailment provisions", "Mandatory Demand Curtailment (MDC)", "curtailment mechanism", "2025", "Ireland",
     "requirement for Mandatory Demand Curtailment (MDC)",
     "Facilities that fail to provide dispatchable generation face mandatory demand curtailment (MDC) during grid constraint events.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P1", f_cru25, 7, "7", "Printed page matches", "Policy Context", "None",
     "G", "Requirement to provide new renewable and dispatchable generation", "required to provide new renewable and dispatchable electricity generation", "generation obligation", "2025", "Ireland",
     "New data centres connecting under this policy will be required to provide new renewable and dispatchable electricity generation",
     "New data centres seeking Irish grid connections must contract for both new renewable generation and dispatchable capacity.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P1", f_cru25, 7, "7", "Printed page matches", "Policy Context", "None",
     "L", "Participation in wholesale electricity market", "generation projects will participate in", "market participation requirement", "2025", "Ireland",
     "support the wider electricity network and market, the generation projects will participate in",
     "On-site dispatchable generation assets contracted by data centres must participate in the wholesale Single Electricity Market (SEM).",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

# E10_P2 (CRU 2021)
e10_p2_data = [
    ("E10_P2", f_cru21, 3, "3", "Printed page matches", "Introduction", "None",
     "J", "Regulatory directions to System Operators", "issue Directions to the SOs that", "statutory direction", "2021", "Ireland",
     "the CRU considers that it is necessary and proportionate to issue Directions to the SOs that",
     "The CRU issued formal binding directions to EirGrid and ESB Networks to manage data centre connection risks.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P2", f_cru21, 5, "5", "Printed page matches", "Background", "None",
     "A", "Data centres classified as distinct demand class", "distinct class of demand side user", "regulatory customer classification", "2021", "Ireland",
     "system supports the consideration of data centres as a distinct class of demand side user",
     "Due to rapid load scaling and continuous flat demand profiles, data centres are designated as a distinct demand-side user category.",
     "authors' opinion", "EirGrid assessment", "NONE STATED", "[S]"),

    ("E10_P2", f_cru21, 6, "6", "Printed page matches", "Assessment Criteria", "None",
     "H", "Location in constrained grid area criterion", "whether they are within a", "locational grid criterion", "2021", "Ireland",
     "The location of the data centre applicant with respect to whether they are within a",
     "Connection applications are evaluated based on whether the data centre sits in a transmission-constrained or unconstrained geographic zone.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P2", f_cru21, 6, "6", "Printed page matches", "Assessment Criteria", "None",
     "L", "On-site dispatchable generation requirement", "bring onsite dispatchable generation", "on-site generation criterion", "2021", "Ireland",
     "The ability of the data centre applicant to bring onsite dispatchable generation",
     "Applicants must demonstrate the ability to provide on-site dispatchable generation or storage to support grid security during shortages.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P2", f_cru21, 6, "6", "Printed page matches", "Assessment Criteria", "None",
     "E", "Demand flexibility during system constraints", "flexibility in their demand by", "demand flexibility criterion", "2021", "Ireland",
     "The ability of the data centre applicant to provide flexibility in their demand by",
     "Applicants must exhibit operational demand flexibility to curtail power consumption during system constraint events.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_P2", f_cru21, 6, "6", "Printed page matches", "Assessment Criteria", "None",
     "J", "Equal weighting of assessment criteria", "decided not to rank or afford priority to certain criteria over others", "regulatory weighting rule", "2021", "Ireland",
     "The CRU has decided not to rank or afford priority to certain criteria over others",
     "The CRU determined that location, on-site dispatchable power, and demand flexibility would be applied without hierarchical ranking.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

# E11_P (Rajya Sabha Q956)
e11_p_data = [
    ("E11_P", f_mop, 1, "not printed", "locator in my file, not a page of the source", "Ministry Answer (a)", "None",
     "N", "CEA 20th EPS AI data centre demand projection", "26.3 GW from Artificial Intelligence (AI) Data", "GW load projection", "by FY 2031-32", "India",
     "additional load of 26.3 GW from Artificial Intelligence (AI) Data",
     "The Central Electricity Authority's 20th Electric Power Survey midterm review estimates an additional 26.3 GW of AI data centre demand by FY 2031-32.",
     "projection", "Central Electricity Authority (CEA)", "NONE STATED", "[S]"),

    ("E11_P", f_mop, 2, "not printed", "locator in my file, not a page of the source", "Ministry Answer (b)", "None",
     "F", "ISTS transmission capacity under construction", "39,792 ckm of transmission lines and 4,01,510 MVA", "ckm and MVA under construction", "2026", "India",
     "154 Inter-State Transmission System (ISTS) projects are under construction in the country consisting of 39,792 ckm of transmission lines and 4,01,510 MVA",
     "India has 154 ISTS projects under construction totaling 39,792 circuit kilometers of lines and 401,510 MVA of transformation capacity.",
     "measured", "Ministry of Power", "NONE STATED", "[S]"),

    ("E11_P", f_mop, 2, "not printed", "locator in my file, not a page of the source", "Ministry Answer (b)", "None",
     "F", "InSTS state transmission capacity under construction", "30,387 ckm of transmission lines and 1,18,194 MVA", "ckm and MVA under construction", "2026", "India",
     "Intra State Transmission System (InSTS) projects (220 KV & above) comprising of 30,387 ckm of transmission lines and 1,18,194 MVA",
     "Intra-state transmission systems (>=220 kV) under construction comprise 30,387 circuit km and 118,194 MVA of transformation capacity.",
     "measured", "Ministry of Power", "NONE STATED", "[S]"),

    ("E11_P", f_mop, 2, "not printed", "locator in my file, not a page of the source", "Ministry Answer (c)", "None",
     "G", "Renewable vs thermal capacity additions FY24-FY27", "1,16,487 MW RE vs 21,080 MW coal", "MW capacity addition", "FY 2023-24 to 2026-27", "India",
     "coal-based capacity addition from FY 2023-24 to 2026-27 (till June 2026) is about 21,080 MW",
     "Between FY24 and June 2026, India added 116,487 MW of renewable/hydro capacity compared to 21,080 MW of coal-based capacity.",
     "measured", "Ministry of Power", "NONE STATED", "[S]"),

    ("E11_P", f_mop, 3, "not printed", "locator in my file, not a page of the source", "Annexure", "Table",
     "C", "India national peak demand projection FY32", "388", "GW national peak demand", "FY 2031-32", "India",
     "2026-27 289 17.96 2027-28 305 5.54 2028-29 325 6.55 2029-30 345 6.15 2030-31 364 5.51 2031-32 388 6.59",
     "All-India peak electric power demand is projected to grow from 289 GW in FY27 to 388 GW by FY 2031-32.",
     "projection", "Central Electricity Authority (CEA)", "NONE STATED", "[S]")
]

# E16 (CSO Ireland MEC02)
e16_data = [
    ("E16", f_cso, 1, "not printed", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Data centre metered electricity consumption 2025", "7,663 Gigawatt hours (GWh)", "GWh metered electricity", "2025", "Ireland",
     "metered electricity consumption by data centres reached 7,663 Gigawatt hours (GWh) in 2025",
     "Official metered billing records show Irish data centres consumed 7,663 GWh of electricity in 2025.",
     "measured", "ESB Networks / EirGrid meter data", "NONE STATED", "[S]"),

    ("E16", f_cso, 1, "not printed", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Data centre share of national metered electricity", "23%", "% of total national metered electricity", "2025", "Ireland",
     "accounting for 23% of total national metered electricity. Data centre power use increased by 10% in 2025",
     "Data centres accounted for 23% of Ireland's total national metered electricity consumption in 2025, growing 10% year-on-year.",
     "measured", "Central Statistics Office Ireland", "NONE STATED", "[S]"),

    ("E16", f_cso, 1, "not printed", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Historical data centre electricity share surge", "5% in 2015, 22% in 2024, 23% in 2025", "% share trajectory", "2015-2025", "Ireland",
     "% of metered electricity consumed by data centres, 5% in 2015, 22% in 2024, 23% in 2025",
     "Data centre share of Irish electricity surged from 5% in 2015 to 22% in 2024 and 23% in 2025, an increase of over 500%.",
     "measured", "Central Statistics Office Ireland", "NONE STATED", "[S]"),

    ("E16", f_cso, 1, "not printed", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Data centre demand vs urban and rural dwellings", "exceeded the total electricity consumed by all urban dwellings", "sectoral demand comparison", "2025", "Ireland",
     "data centre electricity consumption exceeded the total electricity consumed by all urban dwellings in Ireland (18%), highlighting extreme grid concentration",
     "Irish data centres consumed more electricity (23%) than all urban dwellings in Ireland combined (18%), and nearly triple rural dwellings (9%).",
     "measured", "Central Statistics Office Ireland", "NONE STATED", "[S]")
]

if __name__ == '__main__':
    test_rows(e10_p1_data, "E10_P1")
    test_rows(e10_p2_data, "E10_P2")
    test_rows(e11_p_data, "E11_P")
    test_rows(e16_data, "E16")

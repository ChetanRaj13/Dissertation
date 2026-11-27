import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

# Secondary web/press files
f_kpmg = "Ireland's data centre policy reset (KPMG Ireland).pdf"
f_pinsent = "New Irish data centres must generate power back into national grid (Pinsent Masons Out-Law).pdf"
f_bs = "AI data centres to add 26.3 GW to India's power demand by FY32 (Business Standard).pdf"
f_theprint = "Data centre gold rush risks blackouts - CEA warns states against tripping grids (ThePrint).pdf"
f_dcd_va = "Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf"
f_dcf_va = "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints (Data Center Frontier).pdf"
f_inside = "Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf"
f_dcd_ie = "Data centers in Ireland consumed 23% of national electricity in 2025 (Data Center Dynamics).pdf"
f_mondaq = "Ireland's Data Centre Connections - Back Online (Mondaq).pdf"
f_examiner = "Data centres accounted for 23% of all Ireland's electricity usage (Irish Examiner).pdf"

# E10_S1 (KPMG Ireland)
e10_s1_rows = [
    ("E10_S1", f_kpmg, 2, "2", "locator in my file, not a page of the source", "Policy Updates", "None",
     "F", "EirGrid Fault Ride-Through and LEAP impacts", "substantial near- and longer-term impacts on existing and new data centres", "grid policy impact", "2025", "Ireland",
     "Large Energy User Action Plan, and the CRU's Large Energy Users Connection Policy will have substantial near- and longer-term impacts",
     "EirGrid's Fault Ride-Through solutions and the CRU connection policy impose substantial technical requirements on Irish data centres.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_S1", f_kpmg, 2, "2", "locator in my file, not a page of the source", "Grid Stability", "None",
     "E", "Transient fault risks from data centre disconnections", "one or more data centres will disconnect", "transient fault risk", "2025", "Ireland",
     "The concern is that, following a temporary disturbance on the grid, one or more data centres will disconnect",
     "Grid operators fear temporary grid voltage sags could cause simultaneous disconnection of multiple data centres, threatening total system collapse.",
     "authors' opinion", "EirGrid consultation", "NONE STATED", "[S]"),

    ("E10_S1", f_kpmg, 3, "3", "locator in my file, not a page of the source", "Connection Thresholds", "Table 1",
     "A", "Hyperscale 10 MVA threshold in Ireland", "dominated by the hyperscale market segment which operate large facilities well in excess of 10MVA", "facility scale definition", "2025", "Ireland",
     "Ireland's data centre market is dominated by the hyperscale market segment which operate large facilities well in excess of 10MVA",
     "The Irish market is predominantly composed of hyperscale facilities operating with grid connection requests well exceeding 10 MVA.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E10_S1", f_kpmg, 3, "3", "locator in my file, not a page of the source", "Curtailment Rules", "Table 1",
     "E", "Exemption from Mandatory Demand Curtailment", "data centres will have no requirement for Mandatory Demand Curtailment", "curtailment policy", "2025", "Ireland",
     "the Regulator has confirmed that data centres will have no requirement for Mandatory Demand Curtailment (MDC)",
     "Data centres meeting dispatchable on-site generation rules are exempted from mandatory emergency grid demand curtailment.",
     "authors' opinion", "CRU Decision", "NONE STATED", "[S]")
]

# E10_S2 (Pinsent Masons Out-Law)
e10_s2_rows = [
    ("E10_S2", f_pinsent, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "L", "Power generation contribution requirement", "generate power back into national grid", "regulatory requirement", "2025", "Ireland",
     "requiring newly connecting data centres to contribute generation capacity to the na",
     "New Irish data centre connections must contribute on-site dispatchable generation back to the national transmission grid.",
     "authors' opinion", "CRU Proposed Decision", "NONE STATED", "[S]"),

    ("E10_S2", f_pinsent, 3, "3", "locator in my file, not a page of the source", "Policy Analysis", "None",
     "J", "Green industrialisation policy tension", "tension between overlapping policy areas", "policy conflict", "2025", "Ireland",
     "\"Any green industrialisation strategy naturally creates some tension between overlapping policy areas,\" he explained",
     "Irish industrial expansion creates acute tensions between national digital infrastructure ambitions and statutory carbon emissions limits.",
     "authors' opinion", "Pinsent Masons legal expert", "NONE STATED", "[S]")
]

# E11_S (Business Standard)
e11_s_rows = [
    ("E11_S", f_bs, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "N", "AI data centre 26.3 GW load addition", "projected to add 26.3 GW of additional power demand to India's grid", "GW power projection", "by FY 2031-32", "India",
     "artificial intelligence and data centres are projected to add 26.3 GW of additional power demand to India's grid by FY 2031-32",
     "Business Standard reports Ministry of Power projections that AI data centres will add 26.3 GW to India's electricity grid by FY32.",
     "literature citation", "Ministry of Power / Rajya Sabha UQ 956", "as reported by a secondary source", "[S]"),

    ("E11_S", f_bs, 1, "1", "locator in my file, not a page of the source", "Transmission Plan", "None",
     "F", "National Electricity Plan transmission capex", "envisaging ₹9.16 lakh crore under the National Electricity Plan", "transmission investment capex", "by FY 2031-32", "India",
     "government outlined major transmission planning (envisaging ₹9.16 lakh crore under the National Electricity Plan)",
     "The Government of India outlined ₹9.16 lakh crore in transmission network investments under the National Electricity Plan to support load growth.",
     "literature citation", "Ministry of Power", "as reported by a secondary source", "[S]")
]

# E12 (ThePrint)
e12_rows = [
    ("E12", f_theprint, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "N", "CEA grid tripping warning to states", "warns states against tripping grids", "regulatory blackout warning", "2026", "Maharashtra, Andhra Pradesh, Telangana, Tamil Nadu",
     "Data centre gold rush risks blackouts, central electricity body warns states against tripping grids",
     "ThePrint reports that the Central Electricity Authority warned Maharashtra, Andhra Pradesh, Telangana, and Tamil Nadu of grid tripping risks.",
     "authors' opinion", "Central Electricity Authority (CEA) advisory", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "E", "AI power surges and blackout vulnerability", "sudden, massive power surges from high-density AI data centres risk tripping", "grid stability risk", "2026", "India",
     "warns that sudden, massive power surges from high-density AI data centres risk tripping state electrical grids and causing widespread blackouts",
     "Unregulated load surges from high-density AI data centres risk tripping transmission lines and triggering cascading regional blackouts.",
     "authors' opinion", "CEA National Generation Adequacy Plan (2026-36)", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 2, "2", "locator in my file, not a page of the source", "Capacity Metrics", "None",
     "N", "India operational capacity crossing 1,700 MW", "crossed 1,700 MW, with Andhra Pradesh alone committing 1 GW+", "MW operational capacity", "2026", "India / Andhra Pradesh",
     "\"India's data centre capacity has crossed 1,700 MW, with Andhra Pradesh alone committing 1 GW+.",
     "Industry experts note India's operational data centre capacity has surpassed 1,700 MW, with Andhra Pradesh committing over 1 GW.",
     "stakeholder perspective", "Sridhar Seshadri (Global Forum for Sustainable Development)", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 2, "2", "locator in my file, not a page of the source", "Technology & Energy", "None",
     "D", "Cooling share of data centre energy", "Cooling already consumes about 40 per cent of DC energy", "% of facility energy", "2026", "India",
     "Cooling already consumes about 40 per cent of DC energy. The real question is not expansion, it is efficiency by design",
     "Cooling systems account for approximately 40% of total data centre electricity consumption in Indian facilities.",
     "stakeholder perspective", "Sridhar Seshadri", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 2, "2", "locator in my file, not a page of the source", "Hub Siting", "None",
     "N", "Visakhapatnam Google-Adani AI hub", "Adani-Google, the Asia Pacific region's largest data centre is coming up at Visakhapatnam", "hyperscale hub development", "2026", "Visakhapatnam, Andhra Pradesh, India",
     "Adani-Google, the Asia Pacific region's largest data centre is coming up at Visakhapatnam in Andhra Pradesh",
     "The Adani-Google hyperscale campus in Visakhapatnam is cited as the Asia-Pacific region's largest planned data centre facility.",
     "authors' opinion", "None", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 3, "3", "locator in my file, not a page of the source", "State Regulatory Action", "None",
     "J", "Andhra Pradesh resource adequacy regulations", "APERC has issued draft regulations and amendments-particularly regarding Resource Adequacy", "state regulatory reform", "2024-2026", "Andhra Pradesh, India",
     "Andhra Pradesh Electricity Regulatory Commission (APERC) has issued draft regulations and amendments-particularly regarding Resource Adequacy (2026), Green Energy Open Access",
     "APERC issued regulatory frameworks covering Resource Adequacy, Green Energy Open Access, and BESS to govern data centre power sourcing.",
     "authors' opinion", "APERC regulatory filings", "as reported by a secondary source", "[S]"),

    ("E12", f_theprint, 3, "3", "locator in my file, not a page of the source", "State Targets", "None",
     "N", "Andhra Pradesh 5 GW data centre target", "ambitious 5 GW plan by 2030", "GW state capacity target", "by 2030", "Andhra Pradesh, India",
     "We have dedicated power lines to meet the base load requirements and we are confident of meeting AP's ambitious 5 GW plan by 2030",
     "Andhra Pradesh industry leadership confirmed an ambitious state target of 5 GW of data centre capacity by 2030.",
     "stakeholder perspective", "Chairman, AP Confederation of Indian Industries", "as reported by a secondary source", "[S]")
]

# E13 (DatacenterDynamics - Ashburn)
e13_rows = [
    ("E13", f_dcd_va, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "F", "Dominion Ashburn transmission bottleneck admission", "Dominion Energy admits it can't meet data center power demands", "utility grid constraint", "July 2022", "Ashburn, Virginia, USA",
     "Dominion Energy admits it can't meet data center power demands in Virginia",
     "In July 2022, Dominion Energy acknowledged transmission line constraints prevented it from meeting new data centre power requests in Ashburn.",
     "event report", "Dominion Energy disclosures", "as reported by a secondary source", "[S]"),

    ("E13", f_dcd_va, 2, "2", "locator in my file, not a page of the source", "Connection Pause", "None",
     "F", "Power connection delay timeline until 2025-2026", "halt power delivery for new data center developments until 2025 or 2026", "connection delay horizon", "2022-2026", "Loudoun County, Virginia, USA",
     "Dominion could halt power delivery for new data center developments until 2025 or 2026, according to a warning that emerged",
     "Dominion warned developers that power delivery for new data centre projects in Eastern Loudoun County could be delayed until 2025 or 2026.",
     "event report", "Dominion Energy customer notices", "as reported by a secondary source", "[S]"),

    ("E13", f_dcd_va, 2, "2", "locator in my file, not a page of the source", "Digital Realty Commentary", "None",
     "F", "Transmission bottleneck vs power generation", "transmission, not generation, i.e. the pipes or the power line infrastructure", "root cause identification", "2022", "Ashburn, Virginia, USA",
     "adding that the cause was \"transmission, not generation, i.e. the pipes or the power line infrastructure, not the actual power.\"",
     "Executive commentary clarified that Ashburn's power crisis stemmed from high-voltage transmission bottlenecks rather than power generation shortages.",
     "stakeholder perspective", "Digital Realty CFO / Wells Fargo", "as reported by a secondary source", "[S]")
]

# E14 (Data Center Frontier - Loudoun)
e14_rows = [
    ("E14", f_dcf_va, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "F", "Dominion partial resumption on substation basis", "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints", "grid connection status", "2022", "Loudoun County, Virginia, USA",
     "Dominion Resumes New Connections, But Loudoun Faces Lengthy Power Constraints",
     "Dominion resumed data centre connections in Eastern Loudoun on a restricted, substation-by-substation basis following the 2022 bottleneck.",
     "event report", "Dominion Energy filings", "as reported by a secondary source", "[S]"),

    ("E14", f_dcf_va, 3, "3", "locator in my file, not a page of the source", "Utility Executive Statements", "None",
     "F", "Substation-by-substation engineering analysis", "performing additional in-depth analysis substation by substation", "engineering review", "2022", "Loudoun County, Virginia, USA",
     "Dominion CEO Bob Blue said the company was \"performing additional in-depth analysis substation by substation",
     "Dominion's CEO confirmed the utility was conducting granular substation-level engineering assessments to allocate constrained capacity.",
     "stakeholder perspective", "Bob Blue (Dominion CEO)", "as reported by a secondary source", "[S]")
]

# E15 (Inside the DataCenter - Virginia Directory)
e15_rows = [
    ("E15", f_inside, 2, "2", "locator in my file, not a page of the source", "Market Overview", "None",
     "B", "Northern Virginia colocation inventory and vacancy rate", "inventory at 4,496.5 MW at mid-2026 with another 2,420 MW under construction and a vacancy rate of 0.2 percent", "MW inventory & vacancy %", "mid-2026", "Northern Virginia, USA",
     "colocation inventory at 4,496.5 MW at mid-2026 with another 2,420 MW under construction and a vacancy rate of 0.2 percent",
     "CBRE recorded Northern Virginia colocation inventory at 4,496.5 MW with 2,420 MW under construction and an ultra-low vacancy rate of 0.2%.",
     "literature citation", "CBRE Research (mid-2026)", "as reported by a secondary source", "[S]"),

    ("E15", f_inside, 2, "2", "locator in my file, not a page of the source", "Pipeline Metrics", "None",
     "C", "Dominion contracted pipeline scale", "contracted data center pipeline reached 53.8 GW in July 2026", "GW contracted pipeline", "July 2026", "Dominion Zone, Virginia",
     "contracted data center pipeline reached 53.8 GW in July 2026",
     "Dominion Energy's contracted queue for data centre connections reached 53.8 GW across its service territory in July 2026.",
     "literature citation", "Dominion Energy filings", "as reported by a secondary source", "[S]"),

    ("E15", f_inside, 2, "2", "locator in my file, not a page of the source", "Loudoun Cluster Scale", "None",
     "H", "Loudoun County building count concentration", "most of the operators behind its 233 buildings, including Amazon, CloudHQ, Compass, NTT, CyrusOne", "building count", "2026", "Loudoun County, Virginia, USA",
     "most of the operators behind its 233 buildings, including Amazon, CloudHQ, Compass, NTT, CyrusOne",
     "Loudoun County contains approximately half of Virginia's data centre sites, encompassing 233 operational buildings.",
     "authors' opinion", "County property records", "as reported by a secondary source", "[S]"),

    ("E15", f_inside, 4, "4", "locator in my file, not a page of the source", "Local Zoning Actions", "None",
     "J", "Local government pushback and moratoria", "Loudoun ended by-right data centers in March 2025", "zoning restriction", "2025-2026", "Loudoun & Virginia Beach, USA",
     "The localities moved first. Loudoun ended by-right data centers in March 2025 and on September 16, 2026 voted 7 to 1 to",
     "Virginia localities reacted to infrastructure strain by ending by-right zoning in Loudoun and passing twelve-month moratoria in Virginia Beach.",
     "event report", "County Board voting records", "as reported by a secondary source", "[S]")
]

# E17 (DatacenterDynamics - Ireland 23%)
e17_rows = [
    ("E17", f_dcd_ie, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Ireland 23% national electricity share in 2025", "Data centers in Ireland consumed 23% of national electricity in 2025", "% share of electricity", "2025", "Ireland",
     "Data centers in Ireland consumed 23% of national electricity in 2025 - report",
     "DatacenterDynamics reports on CSO figures showing Irish data centres consumed 23% of national electricity in 2025.",
     "literature citation", "CSO Ireland Table MEC02", "as reported by a secondary source", "[S]"),

    ("E17", f_dcd_ie, 2, "2", "locator in my file, not a page of the source", "Industry Presence", "None",
     "H", "Hyperscale tech operators in Ireland", "Amazon Web Services, Microsoft, Google, and Meta", "multinational presence", "2025", "Ireland",
     "Ireland is home to some of the world's biggest data center firms, including Amazon Web Services, Microsoft, Google, and",
     "Ireland hosts major hyperscale European hubs for Amazon Web Services, Microsoft, Google, and Meta.",
     "authors' opinion", "None", "as reported by a secondary source", "[S]")
]

# E18 (Mondaq / Arthur Cox)
e18_rows = [
    ("E18", f_mondaq, 2, "2", "locator in my file, not a page of the source", "Regulatory Framework", "None",
     "J", "End of Ireland data centre moratorium", "ended the moratorium on new data centre connections", "regulatory transition", "2025", "Ireland",
     "Large Energy User Connection Policy, which ended the moratorium on new data centre connections",
     "Arthur Cox legal analysis explains the CRU Large Energy User policy ended Ireland's de facto data centre connection moratorium in place since 2021.",
     "authors' opinion", "CRU regulatory decisions", "as reported by a secondary source", "[S]"),

    ("E18", f_mondaq, 2, "2", "locator in my file, not a page of the source", "Key Obligations", "None",
     "L", "100% dispatchable generation covering demand", "providing new dispatchable generation capacity large enough to cover 100% of the site's electricity demand", "generation obligation", "2025", "Ireland",
     "providing new dispatchable generation capacity (e.g. gas turbines, battery storage) large enough to cover 100% of the site's electricity demand",
     "Large data centres (>=10 MVA) must provide dispatchable generation or storage covering 100% of maximum demand.",
     "authors' opinion", "CRU decision paper", "as reported by a secondary source", "[S]"),

    ("E18", f_mondaq, 3, "3", "locator in my file, not a page of the source", "Grid Code Requirements", "None",
     "E", "Fault Ride-Through testing and derogation", "remain connected to the grid or reconnect sufficiently quickly when a momentary fault", "FRT technical capability", "2026", "Ireland",
     "This tests whether the data centre can remain connected to the grid or reconnect sufficiently quickly when a momentary fault",
     "Data centres must pass System Stability Assessments verifying Fault Ride-Through (FRT) compliance to prevent tripping during voltage sags.",
     "authors' opinion", "EirGrid Grid Code recommendations", "as reported by a secondary source", "[S]")
]

# E19 (Irish Examiner)
e19_rows = [
    ("E19", f_examiner, 1, "1", "locator in my file, not a page of the source", "Executive Summary", "None",
     "B", "Data centres 23% electricity share and 10% annual surge", "surging 10% to reach 7,663 GWh", "GWh consumption & % share", "2025", "Ireland",
     "consumed 23% of all metered electricity in the country last year, with demand surging 10% to reach 7,663 GWh",
     "Irish Examiner reports data centres consumed 23% of Irish electricity in 2025, surging 10% to reach 7,663 GWh.",
     "literature citation", "CSO Ireland release", "as reported by a secondary source", "[S]"),

    ("E19", f_examiner, 2, "2", "locator in my file, not a page of the source", "Regulatory Policy", "None",
     "J", "CRU 80% renewable PPA lead-in period", "meet at least 80% of their annual energy demand from new renewable electricity projects, but will get a six-year lead-in time", "compliance schedule", "2025", "Ireland",
     "facilities will need to meet at least 80% of their annual energy demand from new renewable electricity projects, but will get a six-year lead-in time",
     "Under the CRU framework, data centres must secure 80% renewable power from new projects, with a six-year implementation runway.",
     "authors' opinion", "CRU policy announcement", "as reported by a secondary source", "[S]")
]

if __name__ == '__main__':
    all_tests = [
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
    total_passed = 0
    total_rows = 0
    for name, r_set in all_tests:
        ok = test_rows(r_set, name)
        if ok:
            total_passed += len(r_set)
        total_rows += len(r_set)
    print(f"\n==========================================")
    print(f"WEB/PRESS VERIFICATION: Total {total_rows} | Passed: {total_passed} | Failed: {total_rows - total_passed}")

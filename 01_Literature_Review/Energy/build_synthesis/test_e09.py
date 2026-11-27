import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

f_e09 = "Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf"

e09_data = [
    ("E09", f_e09, 3, "3", "Printed page matches", "Preface / Regional Developments", "None",
     "N", "Visakhapatnam Google AI Hub and regional commitments", "1 GW data center investment into the Visakhapatnam Economic Region", "GW regional capacity commitment", "2026", "Visakhapatnam, Andhra Pradesh, India",
     "announcement of the \"Google AI Hub\"-which brings a 1 GW data center investment into the Visakhapatnam Economic Region",
     "Google announced a 1 GW data center hub in Visakhapatnam, contributing to over 6 GW of total regional data center commitments.",
     "event report", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 5, "5", "Printed page matches", "Abstract", "None",
     "C", "India data center capacity projection 2030 range", "4-5 GW (conservative) to 12-17 GW (aggressive)", "GW capacity range", "2030", "India",
     "estimates ranging from 4-5 GW (conservative) to 12-17 GW (aggressive). This paper uses an 8-10 GW scenario",
     "India's data centre capacity is projected to expand from 4-5 GW under conservative scenarios to 12-17 GW under aggressive AI-driven uptake by 2030.",
     "projection", "None", "8-10 GW used for analytical scenario.", "[S]"),

    ("E09", f_e09, 7, "7", "Printed page matches", "The Regulatory Window", "None",
     "K", "Investment commitments and long-term design lock-in", "backed by investment commitments exceeding $50 billion", "investment capital and lifetime", "2025-2030", "India",
     "India's data center capacity is projected to reach 8-10 GW by 2030, backed by investment commitments exceeding $50 billion",
     "India's projected 8-10 GW data centre fleet represents over $50 billion in capital commitments operating for 15-20 years.",
     "authors' opinion", "None", "Facilities designed in 2025-2026 lock in electrical choices for 15-20 years.", "[S]"),

    ("E09", f_e09, 8, "8", "Printed page matches", "Regional Distribution", "Figure 2",
     "H", "Mumbai share of India installed capacity", "concentrated in Mumbai (~53% of installed base", "% of national installed capacity", "2024", "Mumbai, Maharashtra, India",
     "Current capacity is concentrated in Mumbai (~53% of installed base [4]); by 2030, growth in Chennai, Hyderabad, and NCR",
     "Currently, 53% of India's operational data centre capacity is clustered in Mumbai, though regional diversification is expanding toward Chennai and Hyderabad.",
     "modelled estimate", "JLL (2024)", "NONE STATED", "[S]"),

    ("E09", f_e09, 8, "8", "Printed page matches", "The Grid Context", "None",
     "F", "Declining grid inertia from renewable penetration", "reduces the grid's natural resistance to frequency deviations", "grid physical inertia", "2026", "India",
     "resources reduces the grid's natural resistance to frequency deviations",
     "The replacement of conventional synchronous thermal generation with inverter-based renewable resources significantly reduces grid rotational inertia.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 10, "10", "Printed page matches", "Load Profile and Power Quality", "None",
     "E", "Data center high load factor and power factor", "load factors above 0.85 (versus 0.5-0.6 for typical industrial loads)", "load factor & power factor", "2026", "India",
     "Data centers maintain load factors above 0.85 (versus 0.5-0.6 for typical industrial loads), with power factors of 0.95-0.99",
     "Data centres exhibit uniquely flat, high load factors above 0.85 compared to standard industrial loads (0.5-0.6), with near-unity power factors.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 12, "12", "Printed page matches", "Rack Power Density", "Figure 5",
     "A", "AI rack power density increase", "40-100 kW per rack", "kW per server rack", "2026", "India",
     "AI workloads are driving rack densities from traditional 5-10 kW to 40-100 kW per rack",
     "Accelerated AI computing pushes data centre rack power densities from conventional 5-10 kW up to 40-100 kW per rack.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 12, "12", "Printed page matches", "UPS Topology and Grid Interface", "None",
     "E", "UPS double-conversion functionality and isolation", "Provide complete isolation from grid disturbances", "UPS operational function", "2026", "India",
     "Provide complete isolation from grid disturbances",
     "Double-conversion UPS architectures isolate sensitive IT loads from grid voltage sags while presenting power quality harmonics back to the grid.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 12, "12", "Printed page matches", "UPS Topology and Grid Interface", "None",
     "E", "Power quality harmonics and power factor", "THD <5% with 12-pulse or active front-end designs", "total harmonic distortion", "2026", "India",
     "THD <5% with 12-pulse or active front-end designs, and no output disturbance during voltage sags",
     "Modern 12-pulse and active front-end rectifiers limit total harmonic distortion (THD) below 5% while eliminating load disturbances during sags.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 14, "14", "Printed page matches", "Steady-State Analysis", "None",
     "B", "Data center share of India electricity 2030", "approximately 2.6-3.3%", "% of total national electricity consumption", "2030", "India",
     "data centers would represent approximately 2.6-3.3% of India's total electricity consumption",
     "At an operational capacity of 8-10 GW by 2030, data centres would account for roughly 2.6% to 3.3% of India's total electricity consumption.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 14, "14", "Printed page matches", "Steady-State Analysis", "None",
     "N", "Mumbai transmission corridor concentration", "2-3 GW concentrated load on Kalwa/Padghe corridor", "GW corridor load", "2030", "Mumbai, Maharashtra, India",
     "Western Region (Mumbai): 2-3 GW concentrated load on Kalwa/Padghe corridor.",
     "In the Western Region, 2 to 3 GW of data centre demand concentrates along the Kalwa/Padghe transmission corridor into Mumbai.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 14, "14", "Printed page matches", "Steady-State Analysis", "None",
     "N", "Southern Region data center load distribution", "2-3 GW distributed across states", "GW regional load", "2030", "Southern Region, India",
     "2-3 GW distributed across states, with Visakhapatnam emerging as a major new corridor (~1.75 GW committed)",
     "In the Southern Region, 2 to 3 GW of data centre demand is distributed across states, with Visakhapatnam securing 1.75 GW in commitments.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 16, "16", "Printed page matches", "Ancillary Services", "None",
     "L", "Limits on IT load participation in ancillary services", "What data center loads cannot provide", "grid service limits", "2026", "India",
     "Much of the optimism around data center grid participation conflates what co-located equipment can do with what the data center load itself can do",
     "Grid flexibility expectations conflate the capabilities of on-site batteries/gensets with IT server loads, which cannot tolerate curtailment.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 20, "20", "Printed page matches", "Frequency Regulation Context", "None",
     "E", "August 2024 solar surplus high-frequency excursions", "Peak 50.39 Hz (26% of time above 50.05 Hz ceiling)", "frequency deviation peak", "August 2024", "National Grid, India",
     "August 4: Peak 50.39 Hz 26% of time above 50.05 Hz ceiling; 226 minutes). August 11: Peak 50.329 Hz",
     "On August 4, 2024, solar generation surplus (~40 GW) pushed national grid frequency to a peak of 50.39 Hz, exceeding statutory ceilings for 226 minutes.",
     "measured", "GRID-INDIA operational reports", "NONE STATED", "[S]"),

    ("E09", f_e09, 20, "20", "Printed page matches", "Frequency Regulation Context", "None",
     "E", "August 25 2024 grid frequency excursion duration", "Peak 50.377 Hz (38% of time above ceiling; 258 minutes)", "frequency deviation duration", "August 2024", "National Grid, India",
     "August 25: Peak 50.377 Hz (38% of time above ceiling; 258 minutes). Root causes included solar generation ~40 GW exceeding demand",
     "On August 25, 2024, national frequency reached 50.377 Hz, spending 38% of the day (258 minutes) above the statutory 50.05 Hz ceiling.",
     "measured", "GRID-INDIA operational reports", "NONE STATED", "[S]"),

    ("E09", f_e09, 24, "24", "Printed page matches", "Interconnection Cost Allocation", "None",
     "I", "Lifecycle commercial behavior and transmission stranding", "shifts to 120 MW grid offtake with open access", "contracted vs actual draw", "2026", "India",
     "facility that connects at 200 MW, draws 200 MW for three years, then progressively shifts to 120 MW grid offtake with",
     "Interconnection planning faces stranded asset risks when facilities connect at 200 MW but later shift significant load to off-grid captive renewables.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E09", f_e09, 26, "26", "Printed page matches", "Technical Standards and Grid Codes", "None",
     "J", "Absence of large electronic load standards in IEGC", "India's IEGC does not currently include provisions for large electronic loads", "grid code gap", "2026", "India",
     "India's IEGC does not currently include provisions for large electronic loads [11]. International frameworks-the",
     "India's Electricity Grid Code (IEGC) currently lacks technical connection and operational standards tailored to multi-hundred-megawatt digital loads.",
     "authors' opinion", "CEA / CERC regulations", "NONE STATED", "[S]"),

    ("E09", f_e09, 10, "10", "Printed page matches", "Grid Modeling Gaps", "None",
     "M", "Absence of dynamic simulation load models for data centers", "Until these models exist, grid impact assessments for", "modelling limitation", "2026", "India",
     "Until these models exist, grid impact assessments for",
     "Grid stability assessments conducted by GRID-INDIA and SLDCs currently lack validated dynamic simulation models representing data center response during faults.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

if __name__ == '__main__':
    test_rows(e09_data, "E09")

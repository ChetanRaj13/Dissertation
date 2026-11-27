import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

f_e07 = "Virginia Data Center Study - Electric Infrastructure and Customer Rate Impacts.pdf"

# Note on E07 pagination:
# In E07, the slide numbers / printed numbers appear in headers/footers (e.g. 16, 17, 18, 19, 23, etc.)
# Let's verify exact text and pages.

e07_data = [
    ("E07", f_e07, 16, "16", "Printed page matches", "Key Findings | Electric Infrastructure", "None",
     "C", "Virginia peak demand projection", "over 60 GW", "GW peak demand", "2040", "Virginia, USA",
     "Peak demand in Virginia could increase to over 60 GW, requiring substantial investments in",
     "System-wide peak electrical demand in Virginia is projected to exceed 60 GW by 2040 under unconstrained data center expansion.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 17, "17", "Printed page matches", "Key Findings | Electric Infrastructure", "None",
     "F", "Required average generation build rate", "3.6 GW/yr needed on average over the next 15 years", "GW/year annual build rate", "2025-2040", "Virginia, USA",
     "compared to recent history (3.6 GW/yr needed on average over the next 15 years, compared to a historical single-year high of 2.2 GW/yr)",
     "Meeting projected load requires an average annual buildout of 3.6 GW/year across 15 years, far exceeding Virginia's historical high of 2.2 GW/year.",
     "modelled estimate", "None", "Scenario build rates represent annual average between 2025-2040.", "[S]"),

    ("E07", f_e07, 18, "18", "Printed page matches", "Key Findings | Electric Infrastructure", "None",
     "F", "Unconstrained infrastructure portfolio scale", "build-out of over 3.8 GW/yr between 2025-2040", "portfolio buildout rate", "2025-2040", "Virginia, USA",
     "require a build-out of over 3.8 GW/yr between 2025-2040, including new",
     "Unconstrained expansion necessitates over 3.8 GW/year of new capacity between 2025 and 2040, including storage, gas CTs, and transmission.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 18, "18", "Printed page matches", "Key Findings | Electric Infrastructure", "None",
     "F", "New transmission capacity buildout", "new transmission capacity (8.7 GW)", "GW transmission transfer capacity", "2025-2040", "Virginia, USA",
     "infrastructure, as well as new transmission capacity (8.7 GW) and a",
     "Unconstrained load growth requires adding 8.7 GW of new high-voltage transmission transfer capacity into Virginia.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 18, "18", "Printed page matches", "Key Findings | Electric Infrastructure", "None",
     "L", "Battery storage and combustion turbine additions", "10 GW battery storage and 31 GW CTs", "GW capacity additions", "2025-2040", "Virginia, USA",
     "capacity (10 GW), hydrogen-capable combustion turbines (31 GW of new",
     "The required infrastructure portfolio includes 10 GW of battery storage and 31 GW of hydrogen-capable combustion turbines.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 19, "19", "Printed page matches", "Key Findings | Retail Rate Equity", "None",
     "I", "Cost of service allocation equity", "Current rates appropriately apportion costs to classes and customers responsible", "rate equity audit", "2024", "Virginia, USA",
     "Current rates appropriately apportion costs to classes and customers responsible for incurring them including large loads like data",
     "Existing embedded utility rates appropriately apportion costs to large load classes based on current system assets.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 19, "19", "Printed page matches", "Key Findings | Retail Rate Equity", "None",
     "I", "Cost shifting risk to captive ratepayers", "cause cost shifts between ratepayers that may be inequitable", "financial ratepayer risk", "2024", "Virginia, USA",
     "cause cost shifts between ratepayers that may be inequitable",
     "Massive generation and transmission investments create severe risks of inequitable cost shifts onto existing residential ratepayers.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 19, "19", "Printed page matches", "Key Findings | Retail Rate Equity", "None",
     "I", "Utility balance sheet and borrowing cost risk", "raise borrowing costs and thus increase costs for existing ratepayers", "capital finance risk", "2024", "Virginia, USA",
     "balance sheets, which has the potential to raise borrowing costs and thus increase costs for existing ratepayers",
     "The unprecedented scale of capital expenditure strains utility balance sheets, potentially downgrading credit ratings and increasing debt borrowing costs.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 19, "19", "Printed page matches", "Key Findings | Retail Rate Equity", "None",
     "I", "Collateral protection requirement", "increased credit or collateral protection for the utility and its ratepayers", "financial risk mitigation", "2024", "Virginia, USA",
     "costs as well as increased credit or collateral protection for the utility and its ratepayers",
     "To protect captive ratepayers from default or stranded costs, utilities require increased credit and collateral commitments from data centers.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 23, "23", "Printed page matches", "Study Background", "None",
     "H", "Northern Virginia share of global internet traffic", "About 70 percent of global internet traffic", "% of global internet traffic", "2024", "Northern Virginia, USA",
     "About 70 percent of global internet traffic flows through northern Virginia, according to certain estimates1",
     "Industry estimates indicate approximately 70% of global internet traffic flows through Northern Virginia data center hubs.",
     "literature citation", "Loudoun County Economic Development", "NONE STATED", "[S]"),

    ("E07", f_e07, 23, "23", "Printed page matches", "Study Background", "None",
     "B", "Dominion data center peak demand forecast", "9 GW", "GW peak demand (25% share)", "forecast horizon", "Dominion Zone, Virginia",
     "Dominion forecasting data center peak demand reaching 9 GW (contributing to a 25%",
     "Dominion Energy forecasts that data center peak demand alone will reach 9 GW, representing 25% of total peak load.",
     "projection", "Dominion Energy IRP", "NONE STATED", "[S]"),

    ("E07", f_e07, 26, "26", "Printed page matches", "VCEA Framework", "None",
     "J", "VCEA public interest clean energy mandates", "16 GW solar/wind, 5 GW offshore wind, 3 GW storage", "clean energy capacity mandates", "2020", "Virginia, USA",
     "16 GW of in-state solar and onshore wind, 5 GW of offshore wind and 3 GW of energy storage",
     "Virginia Clean Economy Act declared 16 GW of solar/onshore wind, 5 GW of offshore wind, and 3 GW of energy storage to be in the public interest.",
     "authors' opinion", "Virginia Clean Economy Act (2020)", "NONE STATED", "[S]"),

    ("E07", f_e07, 26, "26", "Printed page matches", "VCEA Framework", "None",
     "J", "VCEA noncompliance deficiency penalties", "$45 to $75 per MWh", "$/MWh statutory compliance penalty", "2021", "Virginia, USA",
     "Established schedule of noncompliance deficiency payments, starting at $45 to $75 per MWh and increasing by 1% annually after 2021",
     "The VCEA established statutory deficiency penalties for failing to meet clean energy standards, starting at $45 to $75 per MWh.",
     "authors' opinion", "Code of Virginia", "Increases by 1% annually after 2021.", "[S]"),

    ("E07", f_e07, 35, "35", "Printed page matches", "Data Center Load Growth", "None",
     "B", "Dominion zone data center load 2039", "close to 25 GW, which translates to ~215 TWh", "GW peak and TWh annual load", "2039", "Dominion Zone, Virginia",
     "DOM will be close to 25 GW, which translates to ~215 TWh",
     "Under unconstrained growth, data center peak demand in the Dominion zone is projected to reach nearly 25 GW, consuming approximately 215 TWh by 2039.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 35, "35", "Printed page matches", "Data Center Load Growth", "Figure",
     "B", "No Growth baseline data center annual load", "31 TWh", "TWh annual load", "2039", "Dominion Zone, Virginia",
     "WCC No Growth, 31 TWh",
     "In the absence of future data center expansion, annual data center electricity consumption in the Dominion zone remains at 31 TWh.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 10, "10", "Printed page matches", "Grid Impact Analysis Methodology", "None",
     "M", "Loss of Load Probability reliability modeling", "Loss of Load", "probabilistic reliability method", "2024", "PJM Region",
     "Use LOLP model to quantify \"effective load carrying capability,\"",
     "E3 evaluated bulk power system reliability across the entire PJM region using a Loss of Load Probability (LOLP) simulation framework.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 13, "13", "Printed page matches", "Scenario Design", "None",
     "H", "Co-op share of projected data center load", "around 62%", "% served by electric cooperatives", "2045", "Virginia, USA",
     "by 2045 around 62% of the projected data center loads in virginia are served by cooperatives",
     "By 2045, approximately 62% of projected data center load in Virginia is forecasted to locate in electric cooperative service territories.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E07", f_e07, 33, "33", "Printed page matches", "Modeling Assumptions", "None",
     "G", "Dominion PJM market capacity purchase limit", "up to 3 GW", "GW capacity import cap", "2024", "Dominion Zone / PJM",
     "Dominion was assumed to be able to purchase capacity from the PJM market at a fixed price up to 3 GW, after which it would",
     "The grid model assumed Dominion could purchase up to 3 GW of capacity from the PJM market before incurring new generation construction costs.",
     "modelled estimate", "None", "Assumed fixed price up to 3 GW cap.", "[S]")
]

if __name__ == '__main__':
    test_rows(e07_data, "E07")

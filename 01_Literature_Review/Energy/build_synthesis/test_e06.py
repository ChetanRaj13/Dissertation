import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

f_e06 = "Data Centers in Virginia - JLARC Report 598.pdf"

e06_data = [
    ("E06", f_e06, 5, "i", "Printed page matches", "Executive Summary", "None",
     "B", "Virginia share of global and Americas data center capacity", "13 percent of all reported data center operational capacity globally", "% of global/Americas operational capacity", "2024", "Virginia, USA",
     "13 percent of all reported data center operational capacity globally and 25 percent of capacity in the Americas",
     "Virginia hosts 13% of all reported operational data center capacity worldwide and 25% of total capacity in the Americas.",
     "measured", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 6, "ii", "Printed page matches", "Executive Summary", "None",
     "C", "Virginia unconstrained power demand doubling", "unconstrained demand for power in Virginia would double", "demand growth projection", "2024-2035", "Virginia, USA",
     "unconstrained demand for power in virginia would double within the next 10 years, with the data center industry being the main driver",
     "Independent legislative forecasting indicates Virginia's unconstrained electric power demand will double within 10 years, driven by data centers.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 7, "iii", "Printed page matches", "Executive Summary", "Figure ES-1",
     "F", "Infrastructure buildout scale for unconstrained demand", "substantial amount of new power generation and transmission", "infrastructure requirement", "2025-2040", "Virginia, USA",
     "a substantial amount of new power generation and transmission infrastructure will be needed in Virginia to meet unconstrained energy demand",
     "Meeting unconstrained data center demand requires unprecedented capital buildout across power generation and high-voltage transmission.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 7, "iii", "Printed page matches", "Executive Summary", "None",
     "G", "Generation and transmission required for unconstrained demand", "solar facilities, wind generation, natural gas plants, and increased transmission capacity", "generation and grid buildout", "2025-2040", "Virginia, USA",
     "solar facilities, wind generation, natural gas plants, and increased transmission capacity would all be required to meet unconstrained demand",
     "Meeting unconstrained demand requires adding solar facilities, wind generation, natural gas plants, and increased transmission capacity.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 8, "iv", "Printed page matches", "Executive Summary", "None",
     "G", "Gas plant additions for half unconstrained demand", "one large 1,500 MW plant every two years for 15 consecutive years", "gas generation additions", "2025-2040", "Virginia, USA",
     "added at the rate of about one large 1,500 MW plant every two years for 15 consecutive years",
     "Even meeting only half of unconstrained demand requires constructing one 1,500 MW gas plant every two years for 15 straight years.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 8, "iv", "Printed page matches", "Executive Summary", "None",
     "G", "Reliance on unproven nuclear technologies", "both scenarios 1 and 2 would rely on energy from as yet unproven nuclear technologies", "technological risk", "2040-2050", "Virginia, USA",
     "both scenarios 1 and 2 would rely on energy from as yet unproven nuclear technologies",
     "Long-term load balance scenarios depend heavily on unproven advanced nuclear designs to meet firm zero-carbon requirements.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 9, "v", "Printed page matches", "Executive Summary", "None",
     "F", "Utility power to delay load additions for grid reliability", "delay the addition of new large load customers", "reliability governance mechanism", "2024", "Virginia, USA",
     "one of the main ways they can protect grid reliability is by delaying the addition of new large load customers",
     "Utilities retain the regulatory mechanism to delay connecting large data center loads to preserve transmission reliability.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 9, "v", "Printed page matches", "Executive Summary", "None",
     "I", "Residential rate impact estimate", "$14 to $37 monthly", "$/month bill increase", "by 2040", "Virginia, USA",
     "residential customer of Dominion Energy could experience generation- and transmission-related costs increasing by an estimated $14 to $37 monthly",
     "Residential customers face bill increases of $14 to $37 monthly in constant dollars by 2040 to fund data center grid upgrades.",
     "modelled estimate", "E3 grid modeling analysis", "Independent of inflation.", "[S]"),

    ("E06", f_e06, 9, "v", "Printed page matches", "Executive Summary", "None",
     "I", "Cost of service allocation findings", "current rates appropriately allocate costs to the customers responsible", "cost allocation audit", "2024", "Virginia, USA",
     "study found that current rates appropriately allocate costs to the customers responsible for incurring them, including data center customers",
     "Current embedded utility rate designs appropriately allocate existing historical costs, but future expansion drives system cost increases.",
     "modelled estimate", "E3 rate study", "NONE STATED", "[S]"),

    ("E06", f_e06, 10, "vi", "Printed page matches", "Executive Summary", "None",
     "K", "Stranded asset risk for utility ratepayers", "strand utilities with infrastructure costs that would have to be recouped", "financial ratepayer risk", "2024", "Virginia, USA",
     "strand utilities with infrastructure costs that would have to be recouped from their existing customer base",
     "If data center demand drops or relocates after infrastructure is built, fixed capital costs risk being stranded onto existing customers.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 12, "viii", "Printed page matches", "Executive Summary", "None",
     "J", "State sales tax exemption utilization", "about 90 percent of the industry uses the exemption", "% industry participation", "FY23", "Virginia, USA",
     "tax savings in FY23), and about 90 percent of the industry uses the exemption",
     "Approximately 90% of Virginia data centers utilize the state sales and use tax exemption for server hardware purchases.",
     "measured", "Virginia Dept of Taxation", "NONE STATED", "[S]"),

    ("E06", f_e06, 44, "26", "Printed page matches", "Chapter 3: Energy Impacts", "None",
     "A", "PJM regional transmission role", "coordinates generation and transmission operations and operates as a wholesale power market", "regional grid operator", "2024", "Virginia / PJM",
     "PJM is a not-for-profit organization that coordinates generation and transmission operations and operates as a wholesale power market",
     "PJM manages bulk high-voltage transmission operations and operates wholesale electricity markets across Virginia and 12 other states.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 45, "27", "Printed page matches", "Chapter 3: Energy Impacts", "Sidebar",
     "B", "Individual data center power draw scale", "draw up to 18 MW of power", "MW power capacity", "2024", "Virginia, USA",
     "one of the smaller data centers recently constructed in Virginia can draw up to 18 MW of power",
     "Even smaller modern Virginia facilities draw 18 MW (equivalent to 4,500 homes), while mega-facilities draw 100 to 200+ MW.",
     "measured", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 45, "27", "Printed page matches", "Chapter 3: Energy Impacts", "None",
     "B", "Large data center power capacity range", "100 to over 200 MW each", "MW power draw range", "2024", "Virginia, USA",
     "largest new data centers can draw from 100 to over 200 MW each, which is more than most industrial consumers",
     "Premier hyperscale campuses in Northern Virginia require 100 to over 200 MW of dedicated electrical power each.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E06", f_e06, 47, "29", "Printed page matches", "Chapter 3: Energy Impacts", "None",
     "J", "Virginia Clean Economy Act mandate", "phaseout of carbon-emitting generation in the state by 2050", "statutory decarbonization mandate", "2020", "Virginia, USA",
     "VCEA was enacted in 2020 to drive investment in renewable resources and requires the phaseout of carbon-emitting generation in the state by 2050",
     "Virginia statutory law (VCEA) mandates 100% clean power by 2050, constraining fossil additions unless legally exempted.",
     "authors' opinion", "Code of Virginia", "NONE STATED", "[S]"),

    ("E06", f_e06, 50, "32", "Printed page matches", "Chapter 3: Energy Impacts", "None",
     "F", "Required interzonal transmission capacity expansion", "approximately 40 percent", "% interzonal transmission increase", "2025-2040", "Dominion Zone, Virginia",
     "state would have to increase interzonal capacity to the Dominion transmission zone by approximately 40 percent",
     "Interzonal transmission transfer capacity into the Dominion zone must expand by roughly 40% to prevent grid collapse under data loads.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 50, "32", "Printed page matches", "Chapter 3: Energy Impacts", "None",
     "G", "Doubling of out-of-state energy imports", "more than double the amount of energy imported from out of state", "imported power multiple", "2025-2040", "Virginia, USA",
     "state would need to more than double the amount of energy imported from out of state",
     "To satisfy projected data center load, Virginia must more than double its wholesale electrical imports from external PJM states.",
     "modelled estimate", "E3 grid modeling analysis", "NONE STATED", "[S]"),

    ("E06", f_e06, 69, "51", "Printed page matches", "Chapter 4: Energy Costs", "None",
     "K", "Dominion metered load planning methodology", "only build new transmission to serve 1,000 MW if that is the forecasted metered load", "utility planning methodology", "2024", "Virginia, USA",
     "even if data center customers in an area have requested 2,000 MW of capacity, Dominion will only build new transmission to serve 1,000 MW",
     "Dominion Energy mitigates overbuilding risks by engineering transmission for anticipated metered load rather than full nominal capacity requests.",
     "authors' opinion", "Dominion Energy interview", "NONE STATED", "[S]"),

    ("E06", f_e06, 70, "52", "Printed page matches", "Chapter 4: Energy Costs", "None",
     "I", "Electric co-op balance sheet solvency risks", "do not have the same financial resources or reserves", "utility insolvency vulnerability", "2024", "Virginia, USA",
     "Co-ops are much smaller than the state's investor-owned, for-profit utilities-Dominion and APCO-and do not have the same financial resources or reserves",
     "Customer-owned electric co-ops face severe solvency risks if multi-hundred-megawatt data centers default or dispute bills.",
     "authors' opinion", "Co-op utility interviews", "NONE STATED", "[S]"),

    ("E06", f_e06, 72, "54", "Printed page matches", "Chapter 4: Energy Costs", "None",
     "I", "Retail choice stranded cost risk", "fixed cost of any recently built generation is divided among the remaining customers", "cost shifting mechanism", "2024", "Virginia, USA",
     "customer leaves the utility for retail choice, the fixed cost of any recently built generation is divided among the remaining customers",
     "When massive data centers (>90 MW) exercise statutory retail choice to switch suppliers, fixed capital costs are shifted onto captive residential customers.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

if __name__ == '__main__':
    test_rows(e06_data, "E06")

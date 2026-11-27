import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

f_e08 = "Scaling India's Data Centre Ecosystem - Stakeholder Perspectives on Infrastructure, Energy, and Resilience.pdf"

e08_data = [
    ("E08", f_e08, 2, "2", "Printed page matches", "Executive Summary", "None",
     "N", "India Tier-1 data centre market hierarchy", "Mumbai leads the market, followed by Chennai, Hyderabad, and Bengaluru", "market concentration hierarchy", "2024", "India (Tier-1 hubs)",
     "data centres, Mumbai leads the market, followed by Chennai, Hyderabad, and Bengaluru",
     "In India's data centre landscape, Mumbai represents the largest market, followed in order by Chennai, Hyderabad, and Bengaluru.",
     "measured", "JLL / Anarock (2024)", "NONE STATED", "[S]"),

    ("E08", f_e08, 4, "4", "Printed page matches", "Executive Summary", "None",
     "G", "Renewable energy feasibility via solar-wind-BESS", "up to ~80 per cent renewable supply is feasible", "% renewable feasibility", "2026", "India",
     "indicate that up to ~80 per cent renewable supply is feasible through geographically diversified solarwind portfolios combined with battery storage",
     "Renewable developers confirm up to 80% clean power matching is achievable for data centres through diversified solar-wind-battery configurations.",
     "stakeholder perspective", "Renewable energy developers", "NONE STATED", "[S]"),

    ("E08", f_e08, 4, "4", "Printed page matches", "Executive Summary", "None",
     "J", "Influence of power sector incentives in state policies", "Power-sector incentives are the most influential policy lever", "policy effectiveness ranking", "2026", "India",
     "power-sector incentives are the most influential policy lever across states, with the majority of stakeholders identifying them as critical",
     "Subsidized power tariffs and duty waivers represent the most impactful policy instruments driving state data centre investment.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 4, "4", "Printed page matches", "Executive Summary", "None",
     "F", "Grid connectivity regulatory approval lags", "grid connectivity, and fire safety clearances, slowing deployment", "regulatory bottlenecks", "2026", "India",
     "grid connectivity, and fire safety clearances, slowing deployment",
     "Protracted utility grid interconnection approvals and multi-agency clearances significantly retard operational data centre deployment schedules.",
     "stakeholder perspective", "Industry consultations", "NONE STATED", "[S]"),

    ("E08", f_e08, 10, "10", "Printed page matches", "Market Landscape", "None",
     "H", "Submarine cable landing proximity in Mumbai and Chennai", "Mumbai and Chennai, are proximal to landing", "siting infrastructure driver", "2026", "Mumbai & Chennai, India",
     "Mumbai and Chennai, are proximal to landing",
     "Submarine cable landing stations anchor heavy data centre clustering in coastal metros Mumbai and Chennai.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 12, "12", "Printed page matches", "Infrastructure Dimensions", "None",
     "E", "Requirement for 24/7 continuous uninterrupted power", "requires a stable, uninterrupted 24/7 power supply", "reliability standard", "2026", "India",
     "requires a stable, uninterrupted 24/7 power supply",
     "Data centre facilities necessitate perfectly stable, uninterruptible 24/7 electrical supply, tolerating zero downtime.",
     "authors' opinion", "IEA (2025)", "NONE STATED", "[S]"),

    ("E08", f_e08, 12, "12", "Printed page matches", "Infrastructure Dimensions", "None",
     "H", "Power availability as primary siting determinant", "Access to reliable power is the primary siting criterion", "siting prioritization", "2026", "India",
     "Access to reliable power is the primary siting criterion",
     "Grid reliability and immediate power capacity availability outweigh all other considerations when selecting Indian data centre sites.",
     "stakeholder perspective", "Data centre operators", "NONE STATED", "[S]"),

    ("E08", f_e08, 13, "13", "Printed page matches", "Technology Trends", "None",
     "A", "AI-driven rack power density acceleration", "average rack power densities have", "rack density trend", "2026", "India",
     "workloads, average rack power densities have",
     "The proliferation of intensive AI compute has driven substantial increases in average electrical power densities per server rack.",
     "authors' opinion", "Ramboll (2025)", "NONE STATED", "[S]"),

    ("E08", f_e08, 14, "14", "Printed page matches", "Energy Dimensions", "None",
     "I", "Dual sourcing contract structure with DISCOMs", "Dual sourcing from discoms and non-discom", "commercial procurement structure", "2026", "India",
     "Dual sourcing from discoms and non-discom",
     "Operators secure full-capacity standby connections from state DISCOMs while sourcing cheaper power via open-access renewable contracts.",
     "stakeholder perspective", "Operator interviews", "NONE STATED", "[S]"),

    ("E08", f_e08, 14, "14", "Printed page matches", "Energy Dimensions", "None",
     "I", "DISCOM capacity contracting and financial stress", "financial stress for discoms or socialisation of fixed", "utility revenue impact", "2026", "India",
     "financial stress for discoms or socialisation of fixed",
     "When data centres draw open-access power, DISCOMs bear the fixed generation and network costs of contracted standby capacity.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 14, "14", "Printed page matches", "Energy Dimensions", "None",
     "J", "DISCOM resistance to open access renewable procurement", "pressure on discoms to restrict or discourage non-discom renewable procurement", "regulatory barrier", "2026", "India",
     "create pressure on discoms to restrict or discourage non-discom renewable procurement to protect revenue recovery",
     "Revenue erosion incentivizes cash-strapped state DISCOMs to slow-walk or obstruct open-access clean energy wheeling approvals.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 14, "14", "Printed page matches", "Energy Dimensions", "None",
     "L", "BESS integration timeline in Indian facilities", "central to data centre power architecture over the next 3-5 years", "technology adoption timeline", "2026-2031", "India",
     "central to data centre power architecture over the next 3-5 years, enabling firm renewable supply,",
     "Battery energy storage systems (BESS) are projected to become core power architecture in Indian facilities within 3-5 years.",
     "stakeholder perspective", "Stakeholder consensus", "NONE STATED", "[S]"),

    ("E08", f_e08, 15, "15", "Printed page matches", "Energy Dimensions", "None",
     "F", "Physical grid constraints and cluster congestion", "remain bound by physical grid constraints. They high-", "transmission bottlenecks", "2026", "India",
     "remain bound by physical grid constraints. they highlighted evacuation and capacity limitations in major data centre clusters",
     "Despite securing virtual or wheeling renewable contracts, physical transmission line bottlenecks limit real power flow into major hubs.",
     "stakeholder perspective", "Renewable developers", "NONE STATED", "[S]"),

    ("E08", f_e08, 18, "18", "Printed page matches", "Policy Dimensions", "None",
     "J", "Dominance of power concessions in state policies", "Power-related incentives dominate state policy", "state policy architecture", "2026", "India",
     "Power-related incentives dominate state policy",
     "State data centre promotional policies across India overwhelmingly prioritize power subsidies, tariff rebates, and duty exemptions.",
     "authors' opinion", "State policy benchmarking", "NONE STATED", "[S]"),

    ("E08", f_e08, 19, "19", "Printed page matches", "Policy Dimensions", "None",
     "N", "Navi Mumbai peri-urban clustering", "peri-urban clusters, such as Navi Mumbai's", "hub cluster location", "2026", "Navi Mumbai, Maharashtra, India",
     "and peri-urban clusters, such as Navi Mumbai's",
     "Substantial data centre concentration has clustered in peri-urban nodes like Navi Mumbai, straining local high-voltage substation networks.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 19, "19", "Printed page matches", "International Benchmarking", "None",
     "J", "Ireland on-site generation requirement benchmark", "stringent grid-connection rules for large energy users, requiring on-site", "international regulatory model", "2025", "Ireland / Global benchmark",
     "Ireland has introduced stringent grid-connection rules for large energy users, requiring on-site",
     "CEEW highlights Ireland's regulatory policy mandating on-site dispatchable generation for large energy users as a model for grid protection.",
     "literature citation", "CRU Ireland", "NONE STATED", "[S]"),

    ("E08", f_e08, 20, "20", "Printed page matches", "Enabling Ecosystem", "None",
     "J", "Clean energy open access regulatory friction", "Regulatory friction in clean energy procurement", "procurement barriers", "2026", "India",
     "Regulatory friction in clean energy procurement",
     "Complex cross-subsidy surcharges, additional surcharges, and banking restrictions create substantial regulatory friction for clean energy wheeling.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E08", f_e08, 21, "21", "Printed page matches", "Recommendations", "None",
     "L", "Demand response and dynamic grid integration", "participation in dynamic gridservice markets", "grid flexibility mechanism", "2026", "India",
     "participation in dynamic gridservice markets",
     "CEEW recommends establishing regulatory frameworks for data centres to participate in dynamic grid balancing and demand-response programs.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

if __name__ == '__main__':
    test_rows(e08_data, "E08")

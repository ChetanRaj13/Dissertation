import fitz
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from test_harness import test_rows

f_e05 = "The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf"

e05_data = [
    ("E05", f_e05, 1, "not printed", "PDF page only", "Summary", "None",
     "B", "Global AI carbon footprint range 2025", "32.6 and 79.7 million tons", "million tons of CO2 emissions", "2025", "Global",
     "The carbon footprint of AI systems alone could be between 32.6 and 79.7 million tons of CO2 emissions in 2025",
     "The global carbon emissions attributable solely to AI hardware operations are estimated between 32.6 and 79.7 million metric tons of CO2 in 2025.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "B", "AI share of data center electricity 2024", "15%", "% of total data center electricity demand", "2024", "Global",
     "AI systems accounted for 15% of total data center electricity demand (excluding cryptocurrency mining) in 2024",
     "The IEA estimated that AI workloads represented 15% of global data center electricity consumption in 2024.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "B", "AI share of data center power end-2024", "20%", "% of total data center power demand", "2024", "Global",
     "other recent research has suggested that AI systems represented 20% of total data center power demand by the end of 2024",
     "Recent semiconductor supply chain analysis suggested AI systems accounted for 20% of total data center power draw by late 2024.",
     "literature citation", "de Vries-Gao (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "C", "Global AI power demand end-2025", "23 gigawatts", "GW power demand", "2025", "Global",
     "the total power demand of these systems could reach 23 gigawatts by the end of 2025",
     "Driven by chip packaging expansion, worldwide AI hardware power demand is projected to reach 23 GW by late 2025.",
     "literature citation", "de Vries-Gao (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "B", "Total data center average power demand 2024", "47.4 gigawatts", "GW average power demand", "2024", "Global",
     "almost half of the total data center electricity demand (47.4 gigawatts on average in 2024",
     "Total worldwide data center electricity demand averaged approximately 47.4 GW across 2024.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "B", "UK average national power demand benchmark", "30.7 gigawatts", "GW average demand", "2023", "United Kingdom",
     "approaching as much as a country such as the United Kingdom requires (30.7 gigawatts on average in 2023",
     "Projected AI power demand (23 GW) approaches the entire national average electricity demand of the United Kingdom (30.7 GW).",
     "literature citation", "de Vries-Gao (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 1, "not printed", "PDF page only", "Introduction", "None",
     "G", "Global data center carbon emissions 2024", "approximately 182 million tons", "million tons of CO2", "2024", "Global",
     "electricity generation for global data centers could have produced approximately 182 million tons of CO2 emissions",
     "IEA estimates indicate electricity generation powering global data centers generated roughly 182 million tons of CO2 in 2024.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "Operational vs embodied scope", "None",
     "G", "ICT embodied emissions share", "23%", "% of total ICT footprint", "2024", "Global",
     "Embodied emissions represent 23% of the total footprint of ICT in general but less for data centers, specifically due to high electricity use",
     "Embodied manufacturing emissions account for 23% of overall ICT emissions, but form a smaller proportion in data centers due to massive operational electricity use.",
     "literature citation", "Freitag et al. (2021)", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "AI carbon footprint", "None",
     "B", "Implied data center electricity generation 2024", "460 terawatt hours (TWh)", "TWh", "2024", "Global",
     "182 million tons of CO2 associated with 460 terawatt hours (TWh) of electricity generation for global data centers in 2024",
     "Global data center electricity consumption reached 460 TWh in 2024, resulting in 182 million metric tons of CO2 emissions.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "AI carbon footprint", "None",
     "G", "Implied data center carbon intensity 2024", "395.65 g of CO2 (gCO2/kWh)", "gCO2/kWh", "2024", "Global",
     "the implied average carbon intensity per kilowatt hour (kWh) was 395.65 g of CO2 (gCO2/kWh)",
     "The implied carbon intensity of power generation serving global data centers was 395.65 gCO2/kWh in 2024.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "AI carbon footprint", "None",
     "G", "Global grid average emissions intensity 2024", "445 gCO2/kWh", "gCO2/kWh", "2024", "Global",
     "the IEA's 2024 estimate of the global average emissions intensity from general electricity generation of 445 gCO2/kWh",
     "The global average emissions intensity for general grid electricity generation was estimated by the IEA at 445 gCO2/kWh.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "AI carbon footprint", "None",
     "G", "US and Europe grid carbon intensities", "321 and 174 gCO2/kWh", "gCO2/kWh", "2024", "United States & Europe",
     "regional carbon intensity of electricity generation on their power grids is approximately 321 and 174 gCO2/kWh, respectively",
     "Power grid carbon intensity averages approximately 321 gCO2/kWh in the United States and 174 gCO2/kWh across Europe.",
     "literature citation", "IEA (2025)", "NONE STATED", "[S]"),

    ("E05", f_e05, 2, "not printed", "PDF page only", "AI carbon footprint", "None",
     "B", "Historical US data center electricity (Siddik)", "72.15 TWh", "TWh", "2018", "United States",
     "revealing that the total electricity consumption of data centers in the United States was 72.15 TWh",
     "Academic analysis by Siddik et al. determined that US data center electricity consumption totaled 72.15 TWh in 2018.",
     "literature citation", "Siddik et al. (2021)", "NONE STATED", "[S]"),

    ("E05", f_e05, 5, "not printed", "PDF page only", "Corporate data center share", "None",
     "B", "Meta data center share of electricity", "98%", "% of company electricity and carbon", "2024", "Global (Meta)",
     "centers represent most (98%) of the company's electricity consumption and carbon emissions",
     "Data center operations constitute 98% of Meta's total operational electricity consumption and corporate carbon emissions.",
     "literature citation", "Meta ESG Report (2024)", "NONE STATED", "[S]"),

    ("E05", f_e05, 9, "not printed", "PDF page only", "US tech data center electricity", "Table 5",
     "B", "Combined US data center electricity (Meta, Apple, Google)", "31.7 TWh", "TWh", "2023", "United States",
     "the combined United States-based data centers of Meta, Apple, and Google may have caused 31.7 TWh of electricity consumption",
     "In 2023, the US data centers of Meta, Apple, and Google consumed a combined 31.7 TWh of electricity.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E05", f_e05, 10, "not printed", "PDF page only", "Discussion and conclusion", "None",
     "K", "Location transparency policy requirement", "mandatory location disclosure", "policy governance", "2026", "Global",
     "estimation accuracy would greatly improve if companies disclosed the specific locations where AI systems are operated and the magnitudes of these operations",
     "Environmental accounting requires regulatory mandates compelling tech firms to disclose exact facility locations, capacities, and local grid carbon intensities.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

if __name__ == '__main__':
    test_rows(e05_data, "E05")

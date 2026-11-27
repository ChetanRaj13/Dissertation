import os
import fitz
from verifier import check_excerpt_on_page

# Define candidate rows for E01 (Masanet et al. 2020)
# Columns:
# (paper_id, source_file, pdf_page, printed_page, page_flag, section, table_or_figure,
#  variable_category, variable_name, value_as_printed, unit, year_or_period, geography,
#  excerpt, paraphrase, statement_type, cited_from_other_source, author_caveat, tag)

e01_rows = [
    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Introduction", "None",
     "B", "Global data center electricity share", "around 1%", "% of worldwide electricity use", "2018", "Global",
     "estimated to account for around 1% of worldwide electricity use",
     "Global data centers are estimated to consume approximately one percent of total global electricity supply.",
     "modelled estimate", "None", "NONE STATED", "[S]"),
     
    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Introduction", "None",
     "B", "Historical global data center electricity use 2005", "153", "TWh", "2005", "Global",
     "worldwide energy use of data centers had grown from 153 terawatt-hours (TWh) in 2005 to between 203 and 273 TWh by 2010",
     "Worldwide data center energy consumption increased from 153 TWh in 2005 to between 203 and 273 TWh in 2010.",
     "literature citation", "Koomey (2011)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Introduction", "None",
     "B", "Historical global electricity share 2010", "1.1 to 1.5%", "% of global electricity use", "2010", "Global",
     "totaling 1.1 to 1.5% of global electricity use",
     "In 2010, global data center energy consumption represented between 1.1% and 1.5% of global electricity demand.",
     "literature citation", "Koomey (2011)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Service demand growth", "Figure 1",
     "B", "Workload and compute instance growth", "more than sixfold", "multiple of 2010 baseline", "2010-2018", "Global",
     "workloads and compute instances had increased more than sixfold, whereas data center internet protocol (IP) traffic had increased by more than 10-fold",
     "Between 2010 and 2018, data center compute instances increased by over 600% and IP traffic grew tenfold.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Service demand growth", "None",
     "B", "Data center storage capacity expansion", "25", "factor increase", "2010-2018", "Global",
     "Data center storage capacity has also grown rapidly, increasing by an estimated factor of 25 over the same time period",
     "Installed storage capacity in data centers expanded by an estimated factor of 25 from 2010 to 2018.",
     "modelled estimate", "Cisco (2018); Shehabi et al. (2016)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Hardware efficiency", "Figure 1",
     "D", "Volume server energy efficiency gain", "dropped by a factor of four", "electricity use per computation", "2010-2018", "Global",
     "electricity use per computation of a typical volume server-the workhorse of the data center-has dropped by a factor of four",
     "Average electricity required per computational unit in volume servers declined by a factor of four due to processor efficiency.",
     "measured", "Wagner / Dell (2018)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Storage efficiency", "Figure 1",
     "D", "Storage energy intensity reduction", "dropped by an estimated factor of nine", "watts per terabyte", "2010-2018", "Global",
     "the watts per terabyte of installed storage has dropped by an estimated factor of nine owing to storage-drive density and efficiency gains",
     "Power requirements per terabyte of storage decreased ninefold because of rising drive storage density and drive efficiency.",
     "modelled estimate", "Shehabi et al. (2016)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Virtualization efficiency", "Figure 1",
     "D", "Server compute instances density", "fivefold increase", "compute instances hosted per server", "2010-2018", "Global",
     "growth in the number of servers has slowed considerably owing to a fivefold increase in the average number of compute instances hosted per server",
     "Virtualization enabled a fivefold increase in compute instances per physical server, moderating physical server growth.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 1, "984", "Printed page matches", "Definitions", "None",
     "A", "Power Usage Effectiveness definition", "PUE", "ratio (total energy / IT energy)", "2020", "Global",
     "PUE, the total amount of energy used by a data center divided by the energy used by its IT equipment",
     "PUE is defined as the total facility energy consumption divided by the electricity consumed by IT hardware.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Recalibrated estimates", "Figure 2",
     "B", "Global data center energy use 2018", "~205", "TWh", "2018", "Global",
     "we estimate that global data center energy use reached ~205 TWh in 2018, or ~1% of global electricity consumption",
     "The recalibrated bottom-up model indicates global data center energy consumption reached ~205 TWh in 2018 (~1% of global electricity).",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Historical comparison", "None",
     "D", "Decoupling of compute growth and energy use", "6% increase", "% energy growth vs 550% compute growth", "2010-2018", "Global",
     "represents a 6% increase compared with 2010, despite a 550% increase in compute instances",
     "Data center electricity use grew only 6% between 2010 and 2018 despite a 550% expansion in computational workloads.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Projections and scenarios", "Figure 2",
     "C", "Doubled compute demand projection", "271", "TWh", "Scenario under doubled compute demand", "Global",
     "total energy use is projected to increase to 271 TWh in a scenario where compute demand doubles",
     "Under a scenario where computational demand doubles relative to 2018, continuing efficiency trends limit total energy use to 271 TWh.",
     "scenario", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Data center typology shift", "Figure 2",
     "H", "Traditional data center share collapse", "79% down to 11%", "% of compute instances", "2010-2018", "Global",
     "traditional data centers accounted for 79% of compute instances in 2010 but only 11% in 2018",
     "Traditional enterprise data centers fell from hosting 79% of global compute instances in 2010 to just 11% in 2018.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Data center typology shift", "Figure 2",
     "H", "Hyperscale market dominance", "more than 50%", "% of compute instances", "2018", "Global",
     "hyperscale data centers, which have typical PUEs of ~1.1 to 1.2, accounted for more than 50% of compute instances in 2018",
     "Hyperscale facilities running at PUEs of 1.1-1.2 captured over 50% of global compute instances by 2018.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Efficiency limits", "None",
     "D", "Future efficiency limits and rebound", "efficiency gains cannot outpace demand indefinitely", "qualitative assessment", "Future", "Global",
     "efficiency gains cannot outpace demand indefinitely; eventually, physical and thermodynamic limits will be reached",
     "The authors warn that efficiency improvements cannot indefinitely offset compute growth due to approaching thermodynamic limits.",
     "authors' opinion", "None", "The authors note efficiency gains cannot outpace demand indefinitely.", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Policy recommendations", "None",
     "J", "Information-based policy mechanisms", "three key strategies", "policy framework", "2020", "Global",
     "policy-makers can accelerate progress through three key strategies: (i) information-based policies such as energy-efficiency labeling",
     "The authors highlight energy-efficiency labeling, mandatory disclosure, and dynamic standards as key policy mechanisms.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Transparency", "None",
     "K", "Lack of bottom-up data", "dearth of knowledge", "transparency critique", "2020", "Global",
     "dearth of knowledge on their energy use and the mixed signals given to policy-makers by contradictory findings are unacceptable",
     "Lack of public data on data center energy use and conflicting extrapolations have hindered informed policymaking.",
     "authors' opinion", "None", "Historical dearth of knowledge creates mixed signals for policymakers.", "[S]"),

    ("E01", "Recalibrating global data center energy-use estimates.pdf", 2, "985", "Printed page matches", "Methods", "None",
     "M", "Bottom-up modeling necessity", "cannot wait another decade", "methodological imperative", "2020", "Global",
     "we cannot wait another decade for the next reliable bottom-up estimates",
     "The authors argue that ongoing bottom-up modeling is critical to avoid reliance on simplistic top-down extrapolations.",
     "authors' opinion", "None", "NONE STATED", "[S]")
]

print(f"E01 candidate rows: {len(e01_rows)}")
# Verify all E01 rows
e01_failed = []
for idx, r in enumerate(e01_rows):
    pdf = r[1]
    pg = r[2]
    exc = r[13]
    ok, msg = check_excerpt_on_page(pdf, pg, exc)
    if not ok:
        e01_failed.append((idx, pg, exc, msg))

print(f"E01 verification: {len(e01_rows) - len(e01_failed)} passed, {len(e01_failed)} failed")
if e01_failed:
    for f in e01_failed:
        print("FAILED:", f)

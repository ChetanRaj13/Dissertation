import fitz
from test_harness import test_rows

f_e01 = "Recalibrating global data center energy-use estimates.pdf"
e01_data = [
    ("E01", f_e01, 1, "984", "Printed page matches", "Introduction", "None",
     "B", "Global data center electricity share", "around 1%", "% of worldwide electricity use", "2018", "Global",
     "estimated to account for around 1% of worldwide electricity use",
     "Global data centers are estimated to account for approximately one percent of global electricity consumption.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Historical literature", "None",
     "B", "Historical data center energy 2005", "153", "TWh", "2005", "Global",
     "worldwide energy use of data centers had grown from 153 terawatt-hours (TWh) in 2005 to between 203 and 273 TWh by 2010",
     "Global data center electricity consumption grew from 153 TWh in 2005 to 203-273 TWh in 2010.",
     "literature citation", "Koomey (2011)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Historical literature", "None",
     "B", "Global electricity share 2010", "1.1 to 1.5%", "% of global electricity use", "2010", "Global",
     "totaling 1.1 to 1.5% of global electricity use",
     "In 2010, data centers consumed between 1.1% and 1.5% of worldwide electricity generation.",
     "literature citation", "Koomey (2011)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Service demand indicators", "Figure 1",
     "B", "Compute instances growth", "more than sixfold", "factor increase", "2010-2018", "Global",
     "global data center workloads and compute instances had increased more than sixfold",
     "Global compute instances and workloads grew by more than six times between 2010 and 2018.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Service demand indicators", "Figure 1",
     "B", "IP traffic growth", "more than 10-fold", "factor increase", "2010-2018", "Global",
     "data center internet protocol (IP) traffic had increased by more than 10-fold",
     "Global data center IP network traffic expanded by more than ten times between 2010 and 2018.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Hardware efficiency", "Figure 1",
     "D", "Volume server efficiency gain", "dropped by a factor of four", "electricity use per computation", "2010-2018", "Global",
     "electricity use per computation of a typical volume server-the workhorse of the data center-has dropped by a factor of four",
     "Electricity consumption per computation in typical volume servers fell by a factor of four from 2010 to 2018.",
     "measured", "Wagner / Dell (2018)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Storage efficiency", "Figure 1",
     "D", "Storage energy intensity reduction", "dropped by an estimated factor of nine", "watts per terabyte", "2010-2018", "Global",
     "the watts per terabyte of installed storage has dropped by an estimated factor of nine owing to storage-drive density and efficiency gains",
     "Power requirements per terabyte of installed data center storage fell by ninefold due to density and hardware improvements.",
     "modelled estimate", "Shehabi et al. (2016)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Virtualization", "Figure 1",
     "D", "Server virtualization density", "fivefold increase", "compute instances per server", "2010-2018", "Global",
     "fivefold increase in the average number of compute instances hosted per server (owing to virtualization)",
     "Virtualization increased average compute instances hosted per physical server by five times.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", f_e01, 1, "984", "Printed page matches", "Efficiency definitions", "None",
     "A", "PUE metric definition", "PUE", "ratio of total energy to IT energy", "2020", "Global",
     "PUE, the total amount of energy used by a data center divided by the energy used by its IT equipment",
     "Power usage effectiveness (PUE) is defined as total facility energy divided by IT equipment energy.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Recalibrated global energy use", "Figure 2",
     "B", "Global data center energy 2018", "205", "TWh", "2018", "Global",
     "In 2018, we estimated that global data center energy use rose to 205 TWh, or around 1% of global electricity consumption",
     "The authors estimate that global data center electricity use rose to 205 TWh in 2018, approximately 1% of world electricity.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Historical trend comparison", "None",
     "D", "Decoupling of energy from compute", "6% increase", "% growth vs 550% compute instances", "2010-2018", "Global",
     "This represents a 6% increase compared with 2010, whereas global data center compute instances increased by 550% over the same time period",
     "Electricity consumption increased only 6% from 2010 to 2018 despite a 550% surge in compute instances.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Typology shift", "Figure 2",
     "H", "Traditional data center share drop", "79%", "% of compute instances in 2010", "2010", "Global",
     "shifts in servers away from smaller traditional data centers (79% of compute instances in 2010)",
     "Traditional enterprise data centers accounted for 79% of global compute instances in 2010 before migrating toward cloud.",
     "modelled estimate", "Cisco (2018)", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Hyperscale efficiency", "Figure 2",
     "D", "Hyperscale PUE performance", "1.1 or lower", "PUE", "2018", "Global",
     "hyperscale data centers are already operating with PUEs of 1.1 or lower, which is close to the practical minimum value",
     "World-class hyperscale facilities operate at highly efficient PUE levels of 1.1 or lower, approaching physical limits.",
     "measured", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Policy strategies", "None",
     "J", "Efficiency standards policy", "Energy Star for servers", "policy mechanism", "2020", "Global",
     "promotion of efficiency standards such as Energy Star for servers, storage, and network devices",
     "Policymakers can accelerate efficiency by strengthening mandatory and voluntary standards like Energy Star.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 3, "986", "Printed page matches", "Policy strategies", "None",
     "J", "Cloud migration incentives", "procurement standards and utility rebates", "policy incentives", "2020", "Global",
     "incentivize shifts to cloud services when economically and institutionally feasible-for example, through procurement standards and utility rebates",
     "Governments can promote cloud migration through public procurement rules and targeted utility rebates.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 2, "985", "Printed page matches", "Efficiency limits", "None",
     "D", "Thermodynamic efficiency limits", "cannot rest on their laurels", "qualitative caveat", "2020", "Global",
     "the IT industry, data center operators, and policy-makers can't rest on their laurels; diligent efforts will be required",
     "Industry cannot assume past efficiency trends will continue without deliberate policy intervention and engineering effort.",
     "authors' opinion", "None", "Diligent efforts required to maintain energy plateau.", "[S]"),

    ("E01", f_e01, 3, "986", "Printed page matches", "Renewable energy integration", "None",
     "G", "Renewable adoption incentives", "low-carbon procurement standards and corporate tax credits", "policy incentives", "2020", "Global",
     "accelerate the pace of renewable energy adoption by data centers, including low-carbon procurement standards and corporate tax credits",
     "Policymakers should encourage data center renewable procurement via low-carbon standards and corporate tax credits.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E01", f_e01, 3, "986", "Printed page matches", "Scenarios", "Figure 2 caption",
     "C", "Doubled computing demand scenario", "Doubled demand (relative to 2018)", "scenario definition", "Scenario", "Global",
     "Doubled demand (relative to 2018) reflects current efficiency trends continuing alongside predicted growth in compute instances",
     "The doubled compute scenario models continuing efficiency progress alongside doubled computational instances.",
     "scenario", "None", "NONE STATED", "[S]")
]

print("Testing E01 revised...")
test_rows(e01_data, "E01")

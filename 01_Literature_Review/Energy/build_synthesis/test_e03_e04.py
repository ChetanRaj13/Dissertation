import fitz
from test_harness import test_rows

f_e03 = "Energy and AI - IEA.pdf"
f_e04 = "Artificial intelligence - Supply chain constraints and energy implications.pdf"

e03_data = [
    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "B", "Global data center electricity consumption 2024", "around 1.5%", "% of world electricity consumption (415 TWh)", "2024", "Global",
     "Data centres accounted for around 1.5% of the world's electricity consumption in 2024, or 415 terawatt-hours (TWh)",
     "Data centers consumed approximately 415 TWh in 2024, representing roughly 1.5% of total worldwide electricity consumption.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "H", "Geographic shares of global data center electricity", "45% US, 25% China, 15% Europe", "% of global data center electricity", "2024", "Global",
     "The United States accounted for the largest share of global data centre electricity consumption in 2024 (45%), followed by China (25%) and Europe (15%)",
     "The United States represents 45% of world data center electricity demand, followed by China at 25% and Europe at 15%.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "B", "Data center demand annual growth rate", "around 12% per year", "annual growth rate", "2017-2024", "Global",
     "Globally, data centre electricity consumption has grown by around 12% per year since 2017, more than four times faster than the rate",
     "Global data center electricity use expanded at ~12% annually from 2017 to 2024, four times faster than overall electricity demand.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "H", "Clustering in US markets", "five regional clusters", "regional concentration", "2024", "United States",
     "Nearly half of data centre capacity in the United States is in five regional clusters",
     "Close to 50% of total US data center electrical capacity is concentrated within five major metropolitan/regional hubs.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "C", "Global data center demand projection 2030", "around 945 TWh", "TWh", "2030", "Global",
     "Data centre electricity consumption is set to more than double to around 945 TWh by 2030",
     "Worldwide data center electricity consumption is projected to more than double from 415 TWh to roughly 945 TWh by 2030.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "C", "Global data center demand Base Case 2035", "around 1 200 TWh", "TWh", "2035", "Global",
     "our Base Case sees global data centre electricity consumption rising to around 1 200 TWh by 2035",
     "Under the IEA Base Case scenario, global data center electricity consumption rises to approximately 1,200 TWh by 2035.",
     "scenario", "None", "Uncertainties widen further after 2030.", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "G", "Renewables share of incremental data center demand", "Half of the global growth", "share of generation growth", "2024-2035", "Global",
     "Half of the global growth in data centre demand is met by renewables, supported by storage and the broader electricity grid",
     "Renewable energy generation, backed by storage, is projected to meet 50% of the net growth in data center electricity demand.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "G", "Renewables generation growth for data centers", "over 450 TWh", "TWh", "2024-2035", "Global",
     "Renewables generation is projected to grow by over 450 TWh to meet data centre demand to 2035",
     "Dedicated renewable electricity generation is forecasted to expand by more than 450 TWh to supply expanding data center loads by 2035.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 14, "14", "Printed page matches", "Executive Summary", "None",
     "G", "Natural gas expansion for data centers", "175 TWh", "TWh", "2024-2035", "United States / Global",
     "Natural gas expands by 175 TWh to meet growing data centre demand, notably in the United States",
     "Natural gas generation expands by 175 TWh to provide dispatchable capacity for data centers, predominantly in the US.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 15, "15", "Printed page matches", "Executive Summary", "None",
     "B", "Developing economies data center demand share", "around 5%", "% of electricity demand increase to 2030", "2024-2030", "Developing Economies",
     "In these countries, data centres account for around 5% of the increase in electricity demand to 2030",
     "In emerging and developing economies, data centers represent about 5% of incremental electricity demand growth to 2030.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 15, "15", "Printed page matches", "Executive Summary", "None",
     "B", "Advanced economies data center demand share", "more than 20%", "% of demand growth to 2030", "2024-2030", "Advanced Economies",
     "In this group of countries, data centres account for more than 20% of demand growth to 2030",
     "In advanced economies with historically stagnant load, data centers account for over 20% of net electricity demand growth to 2030.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 15, "15", "Printed page matches", "Executive Summary", "None",
     "F", "Risk of data center project grid delays", "around 20%", "% of planned projects at risk", "2025-2030", "Global",
     "we estimate that unless these risks are addressed, around 20% of planned data centre projects could be at risk of delays",
     "The IEA estimates that roughly 20% of planned data center projects face commissioning delays due to grid connection bottlenecks.",
     "modelled estimate", "None", "Unless grid infrastructure and connection risks are addressed.", "[S]"),

    ("E03", f_e03, 15, "15", "Printed page matches", "Executive Summary", "None",
     "F", "Transmission line construction lead times", "four to eight years", "lead time in years", "2025", "Advanced Economies",
     "Building new transmission lines can take four to eight years in advanced economies and wait times for critical grid components",
     "New high-voltage transmission lines require four to eight years to construct in advanced economies, creating grid delivery lags.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 15, "15", "Printed page matches", "Executive Summary", "None",
     "F", "Supply chain lead times for grid equipment", "doubled in the past three years", "equipment lead time trend", "2022-2025", "Global",
     "wait times for critical grid components such as transformers and cables have doubled in the past three years",
     "Procurement wait times for power transformers and high-voltage cabling have doubled over the past three years.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 16, "16", "Printed page matches", "Executive Summary", "None",
     "L", "AI energy savings in industry", "equivalent to more than the total energy consumption of Mexico", "potential efficiency savings", "2025-2035", "Global",
     "Widespread adoption of existing AI applications to optimise processes in industry can lead to energy savings equivalent to more than the total",
     "Deploying AI process optimization across industrial manufacturing could yield energy savings exceeding Mexico's total national energy use.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 17, "17", "Printed page matches", "Executive Summary", "None",
     "K", "Critical mineral supply concentration (Gallium)", "around 99% of global refined gallium", "% of global supply from China", "2024", "Global",
     "China currently accounts for around 99% of global refined gallium supply",
     "China controls 99% of global refined gallium, a critical mineral for high-efficiency AI power semiconductor components.",
     "literature citation", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 17, "17", "Printed page matches", "Executive Summary", "None",
     "K", "Gallium data center demand projection", "over 10% of today's supply", "% of current supply", "2030", "Global",
     "in 2030, demand for gallium for data centres could reach over 10% of today's supply",
     "Data center hardware manufacturing could consume over 10% of current global gallium production by 2030.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E03", f_e03, 17, "17", "Printed page matches", "Executive Summary", "None",
     "F", "Utility cyberattack surge", "tripled in the past four years", "frequency growth factor", "2021-2025", "Global",
     "Cyberattacks on energy utilities have tripled in the past four years and have become more sophisticated because of AI",
     "Cyberattacks targeting electrical power utilities have tripled over four years, exacerbated by AI-assisted attack vectors.",
     "literature citation", "None", "NONE STATED", "[S]")
]

e04_data = [
    ("E04", f_e04, 1, "1", "Printed page matches", "Introduction", "None",
     "B", "Google AI energy share 2019-2021", "10%-15%", "% of Google's total energy use", "2019-2021", "Global (Google)",
     "machine learning training and inference represented \"10%-15% of Google's total energy use\" from 2019 to 2021",
     "Historical disclosures indicated machine learning workloads comprised 10% to 15% of Google's total operational energy.",
     "literature citation", "Patterson et al. (2022)", "NONE STATED", "[S]"),

    ("E04", f_e04, 1, "1", "Printed page matches", "Introduction", "None",
     "E", "Inference dominance in AI energy", "accounted for most", "workload phase energy share", "2019-2021", "Global (Google)",
     "inference accounted for most of Google's AI electricity costs from 2019 to 2021",
     "Model inference represented the dominant share of Google's AI electricity consumption compared to initial model training.",
     "literature citation", "Patterson et al. (2022)", "NONE STATED", "[S]"),

    ("E04", f_e04, 1, "1", "Printed page matches", "Introduction", "None",
     "K", "Tech opacity on AI workloads", "Google stopped providing these insights", "corporate reporting critique", "2024", "Global",
     "Now, Google has stopped providing these insights. With useful information regarding AI's power demand becoming increasingly scarce",
     "Major tech companies have ceased disaggregating AI energy consumption from general cloud services in corporate sustainability disclosures.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 2, "2", "Printed page matches", "AI hardware supply constraints", "None",
     "M", "TSMC CoWoS packaging as key proxy", "one small but crucial piece of information", "methodological proxy", "2024", "Global",
     "one small but crucial piece of information that can be used to obtain insights into AI's growing power demand",
     "TSMC's CoWoS packaging allocation serves as a reliable supply-chain bottleneck proxy to model aggregate AI hardware delivery.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 2, "2", "Printed page matches", "AI hardware supply constraints", "None",
     "A", "CoWoS definition and role", "advanced packaging technology", "hardware packaging definition", "2024", "Global",
     "(CoWoS) packaging capacity of Taiwan Semiconductor Manufacturing Company (TSMC)",
     "TSMC CoWoS packaging integrates logic chips with high-bandwidth memory and represents the ultimate generative AI manufacturing bottleneck.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 3, "3", "Printed page matches", "AI hardware supply constraints", "None",
     "D", "NVIDIA CoWoS-L wafer demand 2024", "at most 43,000 wafers", "wafers (13% of total CoWoS)", "2024", "Global",
     "estimated that NVIDIA's demand for CoWoS-L wafers in 2024 was at most 43,000 wafers in total",
     "NVIDIA's CoWoS-L wafer requirements for Blackwell GPUs in 2024 reached at most 43,000 wafers, representing 13% of TSMC capacity.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 4, "4", "Printed page matches", "AI power demand estimates", "None",
     "C", "NVIDIA and AMD AI systems TDP", "6.8 GW", "GW thermal design power", "2025", "Global",
     "increase the total estimated TDP for NVIDIA and AMD AI systems to 6.8 GW",
     "Projected hardware deployments for NVIDIA and AMD AI systems correspond to an estimated 6.8 GW of thermal design power.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 4, "4", "Printed page matches", "AI power demand estimates", "None",
     "C", "Total AI hardware TDP potential", "12.0 GW", "GW thermal design power", "2025", "Global",
     "with the potential total TDP-including other AI systems-rising to 12.0 GW",
     "Including custom ASICs and competing AI hardware, global AI accelerator TDP could reach 12.0 GW by end-2025.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 4, "4", "Printed page matches", "Operational parameters", "None",
     "E", "AI accelerator utilization rates", "60% to 70%", "capacity utilization rate", "2024", "Global",
     "utilization rates, which typically range from 60% to 70% for AI workloads",
     "AI hardware utilization typically ranges from 60% to 70%, reflecting differences between continuous training and bursty inference.",
     "literature citation", "TrendForce (2024)", "NONE STATED", "[S]"),

    ("E04", f_e04, 4, "4", "Printed page matches", "Operational parameters", "None",
     "A", "PUE definition in AI facilities", "PUE", "ratio of facility power to IT power", "2024", "Global",
     "power usage effectiveness (PUE), which reflects the ratio of total data center facility power demand to IT equipment power demand",
     "PUE reflects the total facility power requirement divided by the direct power draw of the IT equipment.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E04", f_e04, 5, "5", "Printed page matches", "Emerging models and efficiency", "None",
     "D", "Algorithmic efficiency (DeepSeek R1)", "less advanced hardware and innovative software", "software optimization", "2025", "China / Global",
     "large language model may achieve performance comparable to that of OpenAI's ChatGPT, but it was claimed to do so using less advanced hardware",
     "Architectural and algorithmic optimizations (demonstrated by DeepSeek R1) can reduce computational costs using less advanced hardware.",
     "literature citation", "Mills and Whittle (2025)", "NONE STATED", "[S]"),

    ("E04", f_e04, 5, "5", "Printed page matches", "Rebound effects", "None",
     "D", "Jevons paradox / bigger is better dynamic", "bigger is better dynamic", "rebound phenomenon", "2025", "Global",
     "this does not necessarily change the \"bigger is better\" dynamic that has driven AI models to unprecedented sizes in recent years",
     "Efficiency improvements may not lower net power demand due to the prevailing paradigm prioritizing ever-larger model scale.",
     "authors' opinion", "Ananthaswamy (2023)", "NONE STATED", "[S]"),

    ("E04", f_e04, 5, "5", "Printed page matches", "Fossil fuel lock-in", "None",
     "G", "Gas power for AI data centers (Crusoe / Stargate)", "4.5 GW", "GW natural gas capacity", "2025", "United States",
     "Crusoe has reportedly secured 4.5 GW of natural gas power capacity for AI data centers, with Stargate as one of its potential customers",
     "Developers like Crusoe have secured 4.5 GW of dedicated natural gas generation capacity to power new AI infrastructure clusters.",
     "literature citation", "Gooding (2025)", "NONE STATED", "[S]")
]

print("Testing E03...")
test_rows(e03_data, "E03")
print("\nTesting E04...")
test_rows(e04_data, "E04")

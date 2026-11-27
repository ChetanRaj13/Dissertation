import openpyxl
import re

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)

# =========================================================================
# 1. AUTHOR NAME: Alex de Vries-Gao (single author, hyphenated surname)
# =========================================================================
# Source_Register
ws_sr = wb["Source_Register"]
ws_sr.cell(5, 3).value = (
    "de Vries-Gao, A. (2026). The carbon and water footprints of data centers and what this could mean "
    "for artificial intelligence. Patterns, 7(1), 100278. https://doi.org/10.1016/j.patter.2025.100278"
)

# Replace any occurrence of "de Vries & Gao" or "de Vries and Gao" across all sheets
for sname in wb.sheetnames:
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            val = ws.cell(r, c).value
            if val and isinstance(val, str):
                if "de Vries & Gao" in val:
                    ws.cell(r, c).value = val.replace("de Vries & Gao", "de Vries-Gao")
                elif "de Vries and Gao" in val:
                    ws.cell(r, c).value = val.replace("de Vries and Gao", "de Vries-Gao")

# =========================================================================
# 2. DATES: Publication date only if printed; otherwise DATE NOT PRINTED
# =========================================================================
# P05: DATE NOT PRINTED
ws_sr.cell(6, 5).value = "DATE NOT PRINTED"

# P06: DATE NOT PRINTED (studies reviewed up to 15 September 2026, pdf p. 61)
ws_sr.cell(7, 5).value = "DATE NOT PRINTED (studies reviewed up to 15 September 2026, pdf p. 61)"

# P08: March 2025 (printed on pdf p. 1)
ws_sr.cell(9, 5).value = "March 2025"

# Across citations in Patterns, Variable_Matrix, Definitions_Compared, Evidence_Quality:
# Ensure P05 is "Rosa et al. (DATE NOT PRINTED)" and P06 is "Masanet (DATE NOT PRINTED)"
for sname in ["Patterns", "Variable_Matrix", "Definitions_Compared", "Evidence_Quality", "Contradictions_and_Gaps", "Link_to_My_Dataset"]:
    ws = wb[sname]
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            val = ws.cell(r, c).value
            if val and isinstance(val, str):
                if "Rosa et al. (2026)" in val:
                    ws.cell(r, c).value = val.replace("Rosa et al. (2026)", "Rosa et al. (DATE NOT PRINTED)")
                if "Masanet (2026)" in val:
                    ws.cell(r, c).value = val.replace("Masanet (2026)", "Masanet (DATE NOT PRINTED)")
                if "2026 (pub)" in val:
                    ws.cell(r, c).value = val.replace("2026 (pub)", "DATE NOT PRINTED")

# =========================================================================
# 3, 4, 5, 6. PATTERNS SHEET UPDATES
# =========================================================================
ws_pat = wb["Patterns"]

# PAT-01 (Row 6)
ws_pat.cell(6, 2).value = (
    "Indirect water consumption from electricity generation substantially exceeds direct on-site cooling water "
    "consumption across empirical and macro-models: direct cooling water is 1.30e8 m3 in P02 (pdf p. 8, EXT-033) "
    "and 140 billion L in P04 (pdf p. 5, EXT-070); off-site electricity-embedded water is 3.83e8 m3 in P02 (pdf p. 8, "
    "EXT-034) and 1,225 billion L in P04 (pdf p. 9, EXT-076). The resulting ratios are derived [I], calculated from "
    "EXT-033 and EXT-034 for P02 as: (3.83e8 m3 / 1.30e8 m3 = 2.95x), and derived [I], calculated from EXT-070 and "
    "EXT-076 for P04 as: (1,225B L / 140B L = 8.75x [roughly 9x]). In the IEA baseline cited by P04, the ratio is "
    "derived [I], calculated from EXT-070 and EXT-075 as: (373B L / 140B L = 2.66x, pdf p. 7). (Note: P02 and P04 report "
    "the underlying volumes; the multiplier ratios are derived [I] and not printed findings of the papers)."
)

ws_pat.cell(6, 16).value = (
    "P01 (Mytton, Perspective) cites Torcellini and US DOE; P09 cites Mytton for 2.18 L/kWh so P09 is not counted "
    "independently. Only 3 independent primary modeling efforts counted: P02 (Siddik et al., 2018 US fleet subbasin model, "
    "indirect 3.83e8 m3 vs direct 1.30e8 m3, EXT-033, EXT-034; derived ratio [I] = 2.95x), P04 (de Vries-Gao, 2023 global "
    "macro-model, indirect 1,225B L vs direct 140B L, EXT-070, EXT-076; derived ratio [I] = 8.75x), and P06 (Masanet, "
    "engineering review, EXT-110, EXT-116)."
)

ws_pat.cell(6, 18).value = (
    "EXT-011 (pdf p. 2, P01) notes that a dry-air cooled natural gas combined cycle plant consumes only 0.00-0.02 L/kWh "
    "of indirect water, and EXT-137 (pdf p. 2, P09) notes that moving to wind and solar energy could reduce water withdrawals "
    "by 25% in the US, meaning indirect water dominance diminishes if data centers are powered by non-thermal renewables."
)

# PAT-02 (Row 7)
ws_pat.cell(7, 2).value = (
    "Data centre exposure to water stress varies significantly by geographical scale and hydrological metric, comprising "
    "four distinct empirical findings (thresholds reported only where printed in the paper):\n"
    "(1) AWARE share of direct water: ~20% of direct data centre water footprint comes from watersheds experiencing moderate "
    "to high water stress (P02, Siddik et al., pdf p. 3, EXT-022; EXT-023; Year: 2018 fleet model; Geography: United States, "
    "2,118 subbasins, EXT-028; Metric: ISO 14046 AWARE characterization factor, EXT-030; numerical CF threshold not stated in the paper).\n"
    "(2) Share of facilities in stressed areas by study:\n"
    "  - Global facilities: 25% of data centers experience at least 1 month of water gap annually under baseline hydrologic "
    "conditions (P05, Rosa et al., pdf p. 1, EXT-082; evaluated across all 9,347 data centers identified globally, EXT-081; "
    "Publication date: DATE NOT PRINTED; Data year: 2025, pdf p. 1; Metric: process-based monthly water gaps where demand exceeds "
    "available renewable supply, EXT-093; numerical percentage threshold not stated in the paper). Under future hydrologic conditions, "
    "affected facilities rise to 33% (pdf p. 1, EXT-083).\n"
    "  - US facilities: 32% of data centres are within areas of high or extremely high water stress (P09, Planet Tracker, pdf p. 3, "
    "EXT-147; evaluated across >2,500 data centres in the USA, EXT-148; Publication date: September 2024, pdf p. 1; Metric: WRI Aqueduct "
    "water stress categories, EXT-148; numerical percentage threshold not stated in the paper; NOTE: strictly US data centres, not global).\n"
    "(3) Asia-specific share: 41% of Asian data centres are located in areas of extremely high water stress, and a further 22% in the high "
    "category (P08, Planet Tracker, pdf p. 2, EXT-182; Publication date: March 2025, pdf p. 1; Data year: DataCenterMap accessed 2 March "
    "2025, pdf p. 2; Metric: WRI Aqueduct 4.0 ratio of total water demand to available renewable supply, EXT-181; numerical percentage "
    "threshold not stated in the paper; P08 notes 'risk thresholds fall into 5 categories from low to extremely high', pdf p. 2, EXT-181).\n"
    "(4) Share of hubs in stressed metros: 52% of global data centre hubs are located in high water-stress regions, rising to 58% by "
    "2050 (P10, Baringa, pdf p. 3, EXT-158; Publication date: November 2025, pdf p. 1; Geography: Global data centre market hubs; "
    "Metric: Baringa Market Attractiveness Index with Aqueduct WRI overlays; numerical percentage threshold not stated in the paper)."
)

ws_pat.cell(7, 16).value = (
    "P08 and P09 share Planet Tracker lineage (both use WRI Aqueduct) but examine distinct scopes (P08 is Asia-Pacific, P09 "
    "is United States; no global 32% exists in P09); P02 uses AWARE; P05 uses global GIS hydrological water gaps; P10 uses "
    "Baringa market hubs. Grouping P08/P09 as one lineage yields 4 strictly independent institutional sources."
)

ws_pat.cell(7, 18).value = (
    "EXT-183 (pdf p. 2, P08) notes that only 25% of Asian data centres are located in water stress areas classified as low "
    "or low/medium, and EXT-039 (pdf p. 10, P02) notes that in certain regions (e.g. US Pacific Northwest and parts of the Northeast), "
    "data centers operate in watersheds with abundant freshwater where evaporative cooling creates negligible scarcity stress."
)

ws_pat.cell(7, 19).value = (
    "Data centre capacity in India is concentrated in four metropolitan markets: Mumbai leads, followed by Chennai, Hyderabad, "
    "and Bengaluru, where competing urban water demands are already high (P07, pdf pp. 2, 15, EXT-189, EXT-207). Future empirical "
    "research question for dissertation dataset: Does this metropolitan clustering intersect with local groundwater overdraft (CGWB "
    "Stage of Extraction > 100%) in surrounding districts?"
)

# PAT-03 (Row 8)
ws_pat.cell(8, 19).value = (
    "Do Indian state data centre policies consider water constraints? P07 documents that state policies heavily focus on power "
    "tariff subsidies and infrastructure incentives while water efficiency and cooling standards are largely absent or emerging "
    "(P07, pdf pp. 18–19, EXT-209, EXT-213). Siting continues to prioritize electrical grid capacity and fiber landing infrastructure "
    "(17 international subsea cables at 14 landing stations, EXT-198) rather than water availability (P07, pdf pp. 2, 10, EXT-188, EXT-198)."
)

# PAT-05 (Row 10) - Split into Qualitative Trade-off (Row 10) and SSF-06
ws_pat.cell(10, 2).value = (
    "Thermodynamic water-energy trade-off: transitioning from evaporative cooling to dry air cooling eliminates on-site "
    "water consumption but incurs an operational electricity penalty (increased facility power consumption to drive airflow "
    "fans and cooling compressors), shifting environmental burdens to off-site power generation and indirect grid water "
    "consumption (P02, pdf p. 10, EXT-040; P06, pdf pp. 4, 18, EXT-110, EXT-116; P10, pdf pp. 4, 5, 8, EXT-164, EXT-165, EXT-171). "
    "(Note: The specific 20% to 40% numerical penalty is a single-source finding from P10 only, reported in SSF-06)."
)

ws_pat.cell(10, 19).value = (
    "Would mandating dry cooling in India's hot climate increase electricity consumption and off-site power grid water use? "
    "Not modeled in P01–P14. The literature establishes the qualitative thermodynamic trade-off (P02, EXT-040; P06, EXT-110; P10, EXT-164), "
    "but the resulting grid water trade-off across India's regional power grids remains an unaddressed empirical question."
)

# PAT-06 (Row 11) - Show figures as separate values with own unit, source, page; no single range
ws_pat.cell(11, 2).value = (
    "Hyperscale facilities achieve significantly superior nominal water and power efficiency compared to enterprise facilities, "
    "but their massive absolute capacity creates severe localized hydrological point-source pressure. The literature reports "
    "two separate modeling benchmarks for a 100-MW facility (not a single range):\n"
    "  (1) Daily benchmark: ~2 million litres of water per day for a typical 100-MW hyperscale facility (cited from IEA by P07, "
    "CEEW, pdf pp. 8, 13, EXT-197, EXT-201). In annual terms, this equates to derived [I], calculated from EXT-197 as: "
    "(2,000,000 L/day * 365 days) / 10^9 = 0.73 billion L/year.\n"
    "  (2) Annual benchmark: 2.5 billion litres of water each year for a single 100-MW hyperscale facility using evaporative cooling—"
    "enough to supply more than 80,000 people (P10, Baringa, pdf p. 3, EXT-156; pdf p. 8, EXT-160).\n"
    "These figures contrast with a medium 15-MW facility using water equivalent to 3 average hospitals or two 18-hole golf courses "
    "(P01, Mytton, pdf p. 1, EXT-007; Masanet, P06, pdf pp. 5, 12, EXT-111, EXT-114)."
)

ws_pat.cell(11, 19).value = (
    "A 100-MW hyperscale facility consumes ~2 million litres of water per day (cited from IEA by P07, pdf p. 8, EXT-197; derived [I]: "
    "0.73 billion L/year) or 2.5 billion litres annually under evaporative cooling (enough to supply more than 80,000 people, P10, "
    "pdf p. 3, EXT-156). In Indian metropolitan clusters, this creates localized point-source competition with municipal supplies "
    "and private tankers (P07, pdf pp. 8, 15, EXT-197, EXT-207)."
)

# Add SSF-06 to Single-Source Findings in Patterns (Row 21)
ws_pat.cell(21, 1).value = "SSF-06"
ws_pat.cell(21, 2).value = "P10"
ws_pat.cell(21, 3).value = "EXT-164 (pdf p. 4), EXT-165 (pdf p. 5), EXT-171 (pdf p. 8)"
ws_pat.cell(21, 4).value = (
    "Dry air cooling electricity penalty: cuts water use close to zero but increases data centre energy consumption by "
    "20% to 40% compared to evaporative systems (rising to ~40% in hot, arid climates; P10, Baringa 2025, pdf p. 4, EXT-164; "
    "pdf p. 8, EXT-171). This specific 20% to 40% numerical range is a single-source finding from P10 only, unconfirmed by other "
    "papers in the corpus."
)
ws_pat.cell(21, 5).value = "P10 (Baringa 2025) provides the only quantified 20% to 40% electricity uplift factor for dry cooling."
ws_pat.cell(21, 6).value = (
    "Commercial advisory report; provides engineering rule-of-thumb estimate rather than empirical metered operational telemetry "
    "across diverse facility designs."
)

# =========================================================================
# 7. CONTRADICTIONS_AND_GAPS MECHANICAL NUMBER FIXES
# =========================================================================
ws_cg = wb["Contradictions_and_Gaps"]

# DIS-01: Row 6
ws_cg.cell(6, 3).value = "140 billion L direct water consumption globally in 2023 (P04, EXT-070, pdf p. 5 citing IEA 2024)"
ws_cg.cell(6, 4).value = ">560 billion L in 2024 (P10, EXT-155, pdf p. 3; P07, EXT-195, pdf p. 7 citing IEA 2025)"
ws_cg.cell(6, 5).value = (
    "IEA 2024 estimated 140 billion L direct water on 360 TWh electricity demand (P04, EXT-070, pdf p. 5); Baringa (P10, EXT-155) "
    "reports >560 billion L globally in 2024, rising to 1.2 trillion L by 2030."
)

# DIS-02: Row 7
ws_cg.cell(7, 3).value = "AWS direct site WUE = 0.12 L/kWh, Meta = 0.19 L/kWh, Microsoft = 0.27 L/kWh (P14, PRS-024, pdf p. 2 citing Rystad Energy 2026)"
ws_cg.cell(7, 4).value = "Google average direct WUE = 1.04 L/kWh (P04, EXT-075, pdf p. 7); Equinix direct WUE = 0.91 L/kWh (P14, PRS-024, pdf p. 2)"
ws_cg.cell(7, 5).value = (
    "Conflation of system boundaries (withdrawal vs consumption), distinct climate zones of data centre fleets, and differing "
    "cooling architectures (direct evaporative vs chilled water vs air-cooled chillers). Masanet notes studies frequently fail to "
    "disclose WUE sources (P06, EXT-129, EXT-130, pdf p. 117)."
)

# DIS-03: Row 8
ws_cg.cell(8, 3).value = "20% of US data centre direct water from stressed subbasins (P02, EXT-022, pdf p. 3 using AWARE); 25% of global data centres face water gaps (P05, EXT-082, pdf p. 1)"
ws_cg.cell(8, 4).value = "32% of US facilities in high/extremely high stress (P09, EXT-147, pdf p. 3; explicitly United States, not global); 41% of Asian data centres in extremely high stress (P08, EXT-182, pdf p. 2); 52% of global hubs in water-stressed regions (P10, EXT-158, pdf p. 3)"

# DIS-04: Row 9
ws_cg.cell(9, 6).value = (
    "Conflating withdrawal and consumption distorts water footprint evaluations because withdrawal includes recirculated or "
    "returned volumes (P01, pdf p. 1, EXT-008; P06, pdf p. 1, EXT-106). Studies emphasize that consumption (evaporative loss) "
    "is the critical parameter for local watershed stress, whereas withdrawal metrics overstate on-site depletion while "
    "obscuring actual hydrological balance (P02, pdf p. 4, EXT-026; P06, pdf pp. 1, 18, EXT-106, EXT-116)."
)

# =========================================================================
# 8. LINK_TO_MY_DATASET MECHANICAL NUMBER FIXES
# =========================================================================
ws_lmd = wb["Link_to_My_Dataset"]

# IND-06: Row 11 (G11)
ws_lmd.cell(11, 7).value = (
    "Measured identically: IT load in MW is the universal engineering scaling metric in both the dissertation dataset and "
    "literature models. Literature establishes that a 100-MW facility requires ~2 million litres of cooling water daily (cited from "
    "IEA by P07, EXT-197, pdf p. 8; derived [I]: 0.73 billion L/year) or 2.5 billion litres annually under evaporative cooling "
    "(P10, EXT-156, pdf p. 3). Facility electricity consumption scales as derived [I], calculated as 100 MW * 24 h * 1,000 kW/MW = 2,400,000 kWh/day."
)

# Table 3 R24: E24
ws_lmd.cell(24, 5).value = (
    "Apply literature benchmarks (such as Google 1.04 L/kWh from P04, EXT-075, or CEEW benchmark 0.83 L/kWh derived [I] from P07, "
    "EXT-197 as: 2,000,000 L/day / (100 MW * 24 h * 1,000 kW/MW)) across operational MW capacity to model estimated district cooling water demand [I]."
)

# Table 4 Q-02: Col 3 (C34) and Col 5 (E34)
ws_lmd.cell(34, 3).value = (
    "Literature establishes that a 100-MW facility requires ~2 million litres of water per day (cited from IEA by P07, EXT-197, "
    "pdf p. 8; converted to 0.73 million m3/year as derived [I], calculated from EXT-197: 2,000,000 * 365 / 10^6) or 2.5 billion "
    "litres annually under evaporative cooling (P10, EXT-156, pdf p. 3; equivalent to 2.5 million m3/year), which can compete with "
    "local industrial water allocations in non-industrial districts."
)
ws_lmd.cell(34, 5).value = (
    "Compute modelled data centre annual cooling water demand using CEEW derived benchmark (0.83 L/kWh derived [I] from P07, EXT-197) "
    "multiplied by MW capacity and 8760 h/year, and divide by CGWB Annual Industrial Groundwater Draft (converted from Ham to MCM) [I]."
)

# Table 4 Q-06: E38
ws_lmd.cell(38, 5).value = (
    "Examine the thermal vs renewable generation profile of the regional power grid serving the district; evaluate off-site "
    "water intensity using literature ranges (derived [I] multiplier: 2.95x direct water in P02, EXT-033, EXT-034; 8.75x in P04, "
    "EXT-070, EXT-076; Masanet, P06, EXT-116) [I]."
)

# Table 4 Q-08: E40
ws_lmd.cell(40, 5).value = (
    "Compare modelled district data centre water consumption against direct literature human-scale benchmarks: a 100-MW "
    "facility equates to the annual water consumption of over 80,000 people (P10, pdf p. 3, EXT-156), or a 15-MW facility "
    "consumes as much water as 3 hospitals (P01, pdf p. 1, EXT-007) [I]."
)

# =========================================================================
# 9. EVIDENCE_QUALITY NUMBER CITATION FIXES
# =========================================================================
ws_eq = wb["Evidence_Quality"]

# Update Table 2 cells containing numbers to include exact Extraction citations
# P01
ws_eq.cell(20, 6).value = "Synthesizes corporate CSR disclosures and Shehabi secondary data (EXT-002, EXT-006)"
ws_eq.cell(21, 6).value = "Transparent mathematical formulas for WUE and PUE provided in text (EXT-017, EXT-018)"
ws_eq.cell(22, 6).value = "Exemplary distinction between direct cooling (57% potable, EXT-001) and indirect electricity water (EXT-009)"
ws_eq.cell(23, 6).value = "National US average (1.7 billion L/day, EXT-002) and corporate global figures, lacks subbasin spatial modeling"
# P02
ws_eq.cell(28, 6).value = "Primary bottom-up engineering model connecting 2,118 subbasins with power plants and water utilities (EXT-028)"
ws_eq.cell(31, 6).value = "Watershed-level resolution across 2,118 subbasins (EXT-028) with ISO 14046 AWARE characterization (EXT-030)"
# P03
ws_eq.cell(36, 6).value = "Primary experimental measurement of AI model training and prompt inference (500 mL per 10-50 queries, EXT-050)"
ws_eq.cell(38, 6).value = "Formal taxonomy defining 3 scopes of AI water use (EXT-051, EXT-055)"
# P04
ws_eq.cell(44, 6).value = "Synthesizes public IEA data (140 billion L direct, EXT-070) and corporate reports (1,225 billion L indirect, EXT-076)"
# P05
ws_eq.cell(52, 6).value = "Bottom-up spatial modeling of all 9,347 operational data centers globally (EXT-081)"
ws_eq.cell(55, 6).value = "Global watershed resolution evaluating monthly water gaps (25% baseline, EXT-082; 33% future, EXT-083)"
# P06
ws_eq.cell(60, 6).value = "Critical review and meta-analysis synthesizing 31 published studies (EXT-106)"
ws_eq.cell(61, 6).value = "Comprehensive 14 best-practice criteria and 10 critical evaluation questions (EXT-106)"
# P07
ws_eq.cell(68, 6).value = "Primary qualitative field study with 24 Indian data centre stakeholders (EXT-190)"
ws_eq.cell(75, 6).value = "Direct empirical relevance to Indian metropolitan data centre clusters and state policies (EXT-189, EXT-207)"
# P08
ws_eq.cell(76, 6).value = "Secondary analysis based on DataCenterMap and WRI Aqueduct data (EXT-181)"
ws_eq.cell(79, 6).value = "Regional Asia-Pacific analysis (41% extremely high water stress, EXT-182)"
# P09
ws_eq.cell(87, 6).value = "Focus on US data centres (>2,500 facilities mapped; 32% in high/extremely high stress, EXT-147, EXT-148)"
# P10
ws_eq.cell(92, 6).value = "Commercial advisory report analyzing 100-MW facility demand (2.5 billion L/year, EXT-156) and 52% hubs in stress (EXT-158)"

wb.save(wb_path)
print("Updated all sheets with author name, dates, thresholds, derived labels, PAT-05 split, PAT-06 disaggregation, and mechanical number fixes.")

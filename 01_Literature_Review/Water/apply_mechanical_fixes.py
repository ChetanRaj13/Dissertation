import openpyxl

wb_path = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\01_Literature_Review\Water\water_datacentre_literature_synthesis_v1.xlsx"
wb = openpyxl.load_workbook(wb_path)

ws_pat = wb["Patterns"]
ws_eq = wb["Evidence_Quality"]
ws_lmd = wb["Link_to_My_Dataset"]

# 1, 2, 3: Patterns B7
ws_pat.cell(7, 2).value = (
    "Data centre exposure to water stress varies significantly by geographical scale and hydrological metric, comprising "
    "four distinct empirical findings (thresholds reported only where printed in the paper):\n"
    "(1) AWARE share of direct water: ~20% of direct data centre water footprint comes from watersheds experiencing moderate "
    "to high water stress (P02, Siddik et al., pdf p. 3, EXT-022; EXT-023; Year: 2018 fleet model; Geography: United States "
    "subbasins, EXT-028; Metric: ISO 14046 AWARE characterization factor, EXT-030; numerical CF threshold not stated in the paper).\n"
    "(2) Share of facilities in stressed areas by study:\n"
    "  - Global facilities: 25% of data centers experience at least 1 month of water gap annually under baseline hydrologic "
    "conditions (P05, Rosa et al., pdf p. 1, EXT-082; evaluated across all 9,347 data centers identified globally, EXT-081; "
    "Publication date: DATE NOT PRINTED; Data year: 2025, pdf p. 1; Metric: process-based monthly water gaps where demand exceeds "
    "available renewable supply, EXT-093; numerical percentage threshold not stated in the paper). Under future hydrologic conditions, "
    "affected facilities rise to 33% (pdf p. 1, EXT-083).\n"
    "  - US facilities: 32% of data centres are within areas of high or extremely high water stress (P09, Planet Tracker, pdf p. 3, "
    "EXT-147; evaluated across US data centres mapped across river basins, EXT-148; Publication date: September 2024, pdf p. 1; "
    "Metric: WRI Aqueduct water stress categories, EXT-148; numerical percentage threshold not stated in the paper; NOTE: strictly US data centres, not global).\n"
    "(3) Asia-specific share: 41% of Asian data centres are located in areas of extremely high water stress, and a further 22% in the high "
    "category (P08, Planet Tracker, pdf p. 2, EXT-182; Publication date: March 2025, pdf p. 1; Data year: DataCenterMap accessed 2 March "
    "2025, pdf p. 2; Metric: WRI Aqueduct ratio of total water demand to available renewable supply, EXT-181; numerical percentage "
    "threshold not stated in the paper; P08 notes 'risk thresholds fall into 5 categories from low to extremely high', pdf p. 2, EXT-181).\n"
    "(4) Share of hubs in stressed metros: 52% of global data centre hubs are located in high water-stress regions, rising to 58% by "
    "2050 (P10, Baringa, pdf p. 3, EXT-158; Publication date: November 2025, pdf p. 1; Geography: Global data centre market hubs; "
    "Metric: Baringa Market Attractiveness Index with Aqueduct WRI overlays; numerical percentage threshold not stated in the paper)."
)

# 4: Patterns S7
ws_pat.cell(7, 19).value = (
    "Data centre capacity in India is concentrated in four metropolitan markets: Mumbai leads, followed by Chennai, Hyderabad, "
    "and Bengaluru, where competing urban water demands are already high (P07, pdf pp. 2, 15, EXT-189, EXT-207). Future empirical "
    "research question for dissertation dataset: Does this metropolitan clustering intersect with localized groundwater overdraft "
    "in surrounding districts?"
)

# 5: Patterns R10
ws_pat.cell(10, 18).value = (
    "EXT-140 (pdf p. 3, P09) and EXT-019 (pdf p. 4, P01) highlight that advanced two-phase immersion cooling and underwater "
    "data centres eliminate evaporative water consumption without cooling fan energy penalties, achieving high thermal efficiency without water loss."
)

# 6: Patterns R11
ws_pat.cell(11, 18).value = (
    "EXT-161 (pdf p. 3, P10) notes that over 40% of newly announced hyperscale capacity since 2023 is shifting toward low- or "
    "no-water cooling designs, meaning future 100-MW campuses will not all rely on traditional evaporative cooling towers."
)

# 7, 8: Evidence_Quality F28, F31
ws_eq.cell(28, 6).value = "Primary bottom-up engineering model connecting US subbasins with power plants and water utilities (EXT-028)"
ws_eq.cell(31, 6).value = "Watershed-level resolution across US subbasins (EXT-028) with ISO 14046 AWARE characterization (EXT-030)"

# 9, 10: Evidence_Quality F60, F61
ws_eq.cell(60, 6).value = "Critical review and meta-analysis evaluating data center water estimation literature against best practices (EXT-106)"
ws_eq.cell(61, 6).value = "Comprehensive best-practice criteria and critical evaluation questions for evaluating studies (EXT-106, EXT-123)"

# 11: Evidence_Quality F87
ws_eq.cell(87, 6).value = "Focus on US data centres mapped across river basins; 32% in high/extremely high stress (EXT-147, EXT-148)"

# 12: Link_to_My_Dataset E40
ws_lmd.cell(40, 5).value = (
    "Compare modelled district data centre water consumption against direct literature human-scale benchmarks: a 100-MW "
    "facility equates to the annual water consumption of over 80,000 people (P10, pdf p. 3, EXT-156), or a 15-MW facility "
    "consumes as much water as three hospitals (P01, pdf p. 1, EXT-007) [I]."
)

wb.save(wb_path)
print("Applied all 12 exact mechanical fixes.")

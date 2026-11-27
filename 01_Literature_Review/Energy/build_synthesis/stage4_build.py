import os
import sys
import datetime
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def run_stage4():
    master_path = "energy_datacentre_literature_synthesis_v1.xlsx"
    backup_path = "energy_datacentre_literature_synthesis_v1_stage4_backup.xlsx"
    
    # Save Stage 4 backup BEFORE modifying workbook (Hard Rule 4)
    shutil.copyfile(master_path, backup_path)
    print(f"Pre-stage backup saved: {backup_path}")
    
    wb = openpyxl.load_workbook(master_path)
    ws_extract = wb["Extraction"]
    ws_web = wb["Web_Press"]
    ws_matrix = wb["Variable_Matrix"]
    ws_norm = wb["Normalised_Values"]
    ws_def = wb["Definitions_Compared"]
    ws_progress = wb["Progress_Log"]
    
    # Styles
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    inference_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # ----------------------------------------------------
    # 1. POPULATE VARIABLE_MATRIX
    # ----------------------------------------------------
    # Columns in Variable_Matrix:
    # paper_id | energy_power_definition | demand_volume_and_year | projection_and_horizon |
    # share_of_national_regional_demand | efficiency_findings | load_characteristics |
    # grid_and_transmission_findings | generation_mix_findings | siting_findings |
    # cost_findings | policy_findings | transparency_finding | main_limitation_stated
    
    matrix_rows = [
        # E01
        ("E01",
         "PUE defined as total facility energy divided by IT equipment energy (pdf p. 1, ROW-0008)",
         "205 TWh in 2018; 153 TWh in 2005 (pdf p. 1, 2, ROW-0002, ROW-0009)",
         "271 TWh in doubled compute demand scenario (pdf p. 3, ROW-0018)",
         "around 1% of worldwide electricity use (pdf p. 1, ROW-0001)",
         "Decoupled: energy grew 6% while compute grew 550% (2010-2018); volume server efficiency dropped 4x (pdf p. 1, 2, ROW-0004, ROW-0010)",
         "Hyperscale shift: 79% compute in traditional (2010) shifted to >50% in hyperscale (2018) with PUE <=1.1 (pdf p. 2, ROW-0011, ROW-0012)",
         "NOT REPORTED",
         "Low-carbon procurement standards and corporate tax credits to accelerate renewable adoption (pdf p. 3, ROW-0017)",
         "Shift toward cloud and hyperscale facilities (pdf p. 2, ROW-0011)",
         "Utility rebates and procurement standards (pdf p. 3, ROW-0014)",
         "Energy Star efficiency standards; cloud migration incentives (pdf p. 2, 3, ROW-0013, ROW-0014)",
         "Dearth of knowledge on energy use and mixed signals to policymakers are unacceptable (pdf p. 3, ROW-0015)",
         "Physical and thermodynamic efficiency limits will eventually be reached; cannot rest on laurels (pdf p. 2, ROW-0016)"),

        # E02
        ("E02",
         "IT load (servers, storage, network) and facility load with PUE (pdf p. 7, ROW-0019)",
         "176 TWh in 2023; 76 TWh in 2018; ~60 TWh in 2014-2016 (pdf p. 7, ROW-0019, ROW-0020, ROW-0021)",
         "325 to 580 TWh by 2028 across low/high scenarios (pdf p. 8, ROW-0023)",
         "4.4% of total US electricity in 2023; projected 6.7% to 12.0% in 2028 (pdf p. 7, 8, ROW-0021, ROW-0025)",
         "Proliferation of GPU-accelerated servers ended era of flat data center energy use (pdf p. 7, 8, ROW-0022, ROW-0026)",
         "74 to 132 GW total power demand at 50% capacity utilization rate (pdf p. 8, ROW-0024)",
         "Utility load tracking avoids overestimation from projects in multiple queues (pdf p. 8, ROW-0029)",
         "NOT REPORTED",
         "High geographic concentration in specific utility service territories (pdf p. 8, ROW-0030)",
         "NOT REPORTED",
         "Public policy and utility planning needed to manage accelerating demand (pdf p. 8, ROW-0028)",
         "Tracking metered utility load avoids double-counting speculative requests across multiple queues (pdf p. 8, ROW-0029)",
         "Rapid evolution of AI chips and workloads introduces significant forecasting uncertainty (pdf p. 9, ROW-0036)"),

        # E03
        ("E03",
         "Data center operational electricity consumption vs IT hardware load (pdf p. 11, ROW-0037)",
         "415 TWh global data center electricity in 2024 (pdf p. 11, ROW-0037)",
         "945 TWh by 2030 and 1,200 TWh by 2035 in Base Case (pdf p. 11, ROW-0038)",
         "1.5% of global electricity in 2024, rising to nearly 3% by 2030 (pdf p. 11, ROW-0037)",
         "Hyperscale PUE improvements slowing as cooling approaches physical limits (pdf p. 12, ROW-0041)",
         "Flat 24/7 baseload with rapid multi-megawatt ramping during AI training runs (pdf p. 13, ROW-0043)",
         "Transmission lines take 4-8 years; transformer and cable wait times doubled in 3 years; 20% of projects face grid delays (pdf p. 15, ROW-0050, ROW-0051)",
         "Corporate PPAs driving renewable additions, but grid integration requires firm dispatchable capacity (pdf p. 14, ROW-0046)",
         "Concentration in US (45%), China (25%), Europe (15%); India emerging rapidly (pdf p. 12, ROW-0039)",
         "Grid upgrade capex and wholesale market price spikes impacting regional ratepayers (pdf p. 15, ROW-0052)",
         "Mandatory grid connection criteria, on-site storage, and demand response programs (pdf p. 16, ROW-0054)",
         "Gallium supply concentration (99% in China) creates semiconductor manufacturing bottleneck (pdf p. 17, ROW-0055)",
         "Opacity in tech company workload disclosures and proprietary semi shipping trackers (pdf p. 12, ROW-0040)"),

        # E04
        ("E04",
         "Thermal Design Power (TDP) of AI accelerators and packaging bottleneck (pdf p. 2, ROW-0059)",
         "Google AI energy was 10%-15% of total energy use (2019-2021) before disclosures stopped (pdf p. 1, ROW-0057)",
         "Projected NVIDIA/AMD AI systems TDP reaching 6.8 GW; total rising to 12.0 GW by end-2025 (pdf p. 4, ROW-0061, ROW-0062)",
         "NOT REPORTED",
         "Architectural optimizations (DeepSeek R1) reduce hardware needs, but Jevons paradox maintains demand expansion (pdf p. 5, ROW-0065, ROW-0066)",
         "Utilization rates range from 60% to 70% for AI workloads (pdf p. 4, ROW-0063)",
         "Crusoe Energy secured 4.5 GW of gas-fired power generation for AI data centers (pdf p. 4, ROW-0064)",
         "Natural gas power purchase agreements utilized to bypass utility connection queues (pdf p. 4, ROW-0064)",
         "NOT REPORTED",
         "NOT REPORTED",
         "EU AI Act voluntary environmental disclosures insufficient; mandatory transparency needed (pdf p. 1, ROW-0058)",
         "Google stopped disclosing AI energy share; hardware operators unwilling to disclose power use (pdf p. 1, ROW-0057, ROW-0060)",
         "Analyst estimates and proprietary packaging models require careful triangulation (pdf p. 2, ROW-0059)"),

        # E05
        ("E05",
         "Operational electricity consumption, implied carbon intensity (gCO2/kWh), and PUE (pdf p. 2, ROW-0077)",
         "460 TWh global data center electricity in 2024; Meta consumed 18.4 TWh (pdf p. 2, 5, ROW-0076, ROW-0081)",
         "AI hardware power demand reaching 23 GW by end-2025; carbon footprint 32.6-79.7 Mt CO2 (pdf p. 1, ROW-0071, ROW-0068)",
         "AI systems accounted for 15% of total data center electricity in 2024; 20% by late 2024 (pdf p. 1, ROW-0069, ROW-0070)",
         "Operational emissions dominate ICT life cycle (embodied is 23% for general ICT, less for data centers) (pdf p. 2, ROW-0075)",
         "Total data center electricity demand averaged 47.4 GW in 2024; AI approaches UK national demand (30.7 GW) (pdf p. 1, ROW-0072, ROW-0073)",
         "Grid carbon intensity varies widely: US average 321 gCO2/kWh, Europe 174 gCO2/kWh (pdf p. 2, ROW-0079)",
         "Global data center electricity implied carbon intensity was 395.65 gCO2/kWh in 2024 (pdf p. 2, ROW-0077)",
         "45% of data centers located in US, 15% in Europe (pdf p. 2, ROW-0079)",
         "NOT REPORTED",
         "Policy must mandate disclosure of specific facility locations, capacities, and local grid factors (pdf p. 10, ROW-0083)",
         "Google and tech operators refuse to disclose indirect emissions/water; company-wide metrics mask DC impact (pdf p. 10, ROW-0083)",
         "Company-wide sustainability metrics do not disaggregate AI workloads from general cloud services (pdf p. 4, ROW-0080)"),

        # E06
        ("E06",
         "Metered utility load (MW/GWh) vs requested capacity (MW) (pdf p. 45, 69, ROW-0086, ROW-0091)",
         "Virginia hosts 13% of global and 25% of Americas operational data center capacity (pdf p. 5, ROW-0068)",
         "Unconstrained electric demand in Virginia projected to double within 10 years (pdf p. 6, ROW-0069)",
         "Data centers driving majority of Virginia load growth; small facilities draw 18 MW, largest draw 100-200+ MW (pdf p. 45, ROW-0086, ROW-0087)",
         "VCEA requires 100% clean power by 2050; relies on unproven advanced nuclear technologies (pdf p. 8, 47, ROW-0073, ROW-0088)",
         "Near-flat 24/7 demand profile; high load factor creates continuous base-load strain on substations (pdf p. 45, ROW-0086)",
         "Interzonal transmission into Dominion zone must increase ~40%; out-of-state power imports double (pdf p. 50, ROW-0089, ROW-0090)",
         "Unconstrained demand requires adding 1,500 MW gas plant every 2 yrs for 15 yrs or doubling solar/wind build rate (pdf p. 7, 8, ROW-0071, ROW-0072)",
         "Clustered heavily in Northern Virginia (Loudoun, Prince William); moving to rural co-op territories (pdf p. 5, 70, ROW-0068, ROW-0092)",
         "Dominion residential customer bills increase $14 to $37/month by 2040; co-ops face solvency risks (pdf p. 9, 70, ROW-0075, ROW-0092)",
         "Utilities can delay large load additions for transmission reliability; sales tax exemption saved $700M+ (pdf p. 9, 12, ROW-0074, ROW-0078)",
         "Dominion builds transmission only for forecasted metered load (1,000 MW) rather than requested capacity (2,000 MW) (pdf p. 69, ROW-0091)",
         "Econometric modeling relies on utility load forecasts subject to market shift risks (pdf p. 6, ROW-0069)"),

        # E07
        ("E07",
         "Peak demand (GW), annual load (TWh), and marginal vs embedded cost of service (pdf p. 16, 19, ROW-0094, ROW-0099)",
         "Dominion zone data center load reaches ~215 TWh (close to 25 GW peak) by 2039 vs 31 TWh baseline (pdf p. 35, ROW-0107, ROW-0108)",
         "Virginia peak demand could increase to over 60 GW by 2040 under unconstrained growth (pdf p. 16, ROW-0094)",
         "Dominion forecasts data center peak demand reaching 9 GW (25% share of utility peak) (pdf p. 23, ROW-0104)",
         "VCEA clean energy goals: 16 GW solar/wind, 5 GW offshore wind, 3 GW storage in public interest (pdf p. 26, ROW-0105)",
         "High sustained load factor; noncompliance deficiency penalties start at $45 to $75/MWh (pdf p. 26, ROW-0106)",
         "Required buildout of 3.6 to 3.8 GW/yr (vs historical high 2.2 GW/yr); 8.7 GW new transmission transfer capacity (pdf p. 17, 18, ROW-0095, ROW-0097)",
         "Infrastructure portfolio requires 10 GW battery storage and 31 GW hydrogen-capable combustion turbines (pdf p. 18, ROW-0098)",
         "By 2045, around 62% of projected Virginia data center load is served by electric co-ops (pdf p. 13, ROW-0110)",
         "Current rates allocate existing costs, but massive capital capex raises borrowing costs and shifts costs to ratepayers (pdf p. 19, ROW-0099, ROW-0101)",
         "Utilities require increased credit and collateral protection to prevent ratepayer stranding (pdf p. 19, ROW-0102)",
         "70% of global internet traffic flows through Northern Virginia (pdf p. 23, ROW-0103)",
         "Production cost model assumes fixed-price market capacity purchases up to 3 GW cap (pdf p. 33, ROW-0111)"),

        # E08
        ("E08",
         "Contracted grid capacity (MVA/MW) vs actual metered draw vs open access wheeling (pdf p. 14, ROW-0120)",
         "Mumbai leads market, followed by Chennai, Hyderabad, Bengaluru; Navi Mumbai peri-urban cluster (pdf p. 2, 19, ROW-0112, ROW-0126)",
         "NOT REPORTED",
         "Data centres represent rapidly expanding commercial baseload; rack power densities surging (pdf p. 13, ROW-0119)",
         "Power-sector incentives (duty waivers, concessional tariffs) are most influential state policy lever (pdf p. 4, 18, ROW-0114, ROW-0125)",
         "Requires stable, uninterrupted 24/7 power; cannot tolerate microsecond interruptions (pdf p. 12, ROW-0117)",
         "Evacuation and capacity limitations in major clusters; grid connection approvals slow deployment (pdf p. 4, 15, ROW-0115, ROW-0124)",
         "Up to ~80% renewable supply feasible via solar-wind-BESS; BESS central over next 3-5 years (pdf p. 4, 14, ROW-0113, ROW-0123)",
         "Siting determined primarily by access to reliable power and proximity to submarine cable landing stations (pdf p. 10, 12, ROW-0116, ROW-0118)",
         "Dual sourcing from DISCOMs causes financial stress and fixed cost socialization (pdf p. 14, ROW-0121)",
         "Ireland on-site dispatchable generation rules and Germany EnEfG highlighted as benchmarks (pdf p. 19, ROW-0127)",
         "State DISCOM resistance to open access renewable procurement due to revenue erosion risks (pdf p. 14, 20, ROW-0122, ROW-0128)",
         "Limited transparency on proprietary operator PUE and facility-level power contracts (pdf p. 14, ROW-0120)"),

        # E09
        ("E09",
         "Load factor (>0.85), input power factor (0.95-0.99), and Total Harmonic Distortion (THD <5%) (pdf p. 10, 12, ROW-0135, ROW-0138)",
         "India capacity crossed 1,700 MW; 53% concentrated in Mumbai; Google 1 GW hub in Visakhapatnam (pdf p. 3, 8, ROW-0130, ROW-0133)",
         "India capacity projected to reach 8-10 GW by 2030 (range 4-5 GW conservative to 12-17 GW aggressive) (pdf p. 5, ROW-0131)",
         "Data centres represent 2.6% to 3.3% of India's total electricity consumption by 2030 (pdf p. 14, ROW-0139)",
         "AI workloads drive rack power densities from traditional 5-10 kW to 40-100 kW per rack (pdf p. 12, ROW-0136)",
         "Double-conversion UPS isolates IT load but presents low-order harmonics (5th, 7th, 11th) to the grid (pdf p. 10, 12, ROW-0137, ROW-0138)",
         "August 2024 frequency excursions reached 50.39 Hz during solar surplus; low inertia threatens grid stability (pdf p. 5, 20, ROW-0143, ROW-0144)",
         "Declining system inertia as inverter renewables replace synchronous thermal plants (pdf p. 8, ROW-0134)",
         "2-3 GW concentrated on Kalwa/Padghe corridor in Mumbai; 2-3 GW distributed in Chennai-Hyderabad-Vizag (pdf p. 14, ROW-0140, ROW-0141)",
         "Stranded transmission risk when 200 MW connection shifts to 120 MW grid offtake via captive RE (pdf p. 24, ROW-0145)",
         "IEGC lacks technical standards for large electronic loads; international response matrix analyzed (pdf p. 18, 26, ROW-0146)",
         "Backed by $50B+ capital commitments locking in electrical architecture for 15-20 years (pdf p. 7, ROW-0132)",
         "Absence of validated dynamic simulation models for data centre loads in Indian grid stability studies (pdf p. 10, ROW-0147)"),

        # E10_P1 / E10_P2
        ("E10_P1",
         "Maximum Import Capacity (MIC) in MVA vs on-site dispatchable generation in MW (pdf p. 4, ROW-0159)",
         "Data centres consumed 23% of Irish electricity in 2025; moratorium in place since 2021 (pdf p. 3, ROW-0158)",
         "Ireland's target of 80% renewable electricity by 2030 requires massive new clean generation (pdf p. 3, ROW-0158)",
         "National electricity share reached 22% in 2024 and 23% in 2025 (pdf p. 3, ROW-0158)",
         "Mandatory Demand Curtailment (MDC) applies unless on-site dispatchable power is installed (pdf p. 4, ROW-0161)",
         "Continuous 24/7 flat baseload demand with rapid ramp-up upon commissioning (pdf p. 5, ROW-0165)",
         "Grid connection policy requires location in unconstrained zones and dynamic stability models (pdf p. 6, ROW-0166)",
         "Requires corporate PPAs matching at least 80% of demand from new renewable projects in Ireland (pdf p. 4, 7, ROW-0160, ROW-0162)",
         "Assessment criteria evaluate location relative to system constraints (Dublin transmission zone) (pdf p. 6, ROW-0166)",
         "Generation projects must participate in wholesale Single Electricity Market (SEM) to support system (pdf p. 7, ROW-0163)",
         "Mandatory on-site dispatchable generation or storage matching 100% of MIC (pdf p. 4, ROW-0159)",
         "Criteria applied without ranking: location, dispatchable generation, and demand flexibility (pdf p. 6, ROW-0168)",
         "Policy applies exclusively to applicants without existing connection agreements in place (pdf p. 6, ROW-0158)"),

        # E11_P
        ("E11_P",
         "Additional peak load from AI data centres (GW) vs All-India peak demand (GW) (pdf p. 1, ROW-0169)",
         "National peak demand 289 GW in FY27 growing to 388 GW by FY32 (pdf p. 3, ROW-0173)",
         "Additional load of 26.3 GW from AI Data Centres estimated by FY 2031-32 (pdf p. 1, ROW-0169)",
         "26.3 GW represents 6.8% of projected All-India peak demand (388 GW) in FY32 (derived [I])",
         "NOT REPORTED",
         "Continuous industrial load requiring firm round-the-clock capacity (pdf p. 1, ROW-0169)",
         "154 ISTS projects (39,792 ckm, 401,510 MVA) and InSTS projects (30,387 ckm, 118,194 MVA) under construction (pdf p. 2, ROW-0170, ROW-0171)",
         "116,487 MW RE additions vs 21,080 MW coal (FY24-June 2026); non-fossil share rose to 54.2% (pdf p. 2, ROW-0172)",
         "NOT REPORTED",
         "₹9.16 lakh crore transmission investments under National Electricity Plan (pdf p. 1, WEB-0004)",
         "Section 7 of Electricity Act 2003 de-licenses power plants provided technical grid standards met (pdf p. 2, ROW-0172)",
         "Central Electricity Authority (CEA) 20th Electric Power Survey (EPS) Mid-term Review (pdf p. 1, ROW-0169)",
         "Parliamentary disclosure aggregates national projections without state-level disaggregation (pdf p. 1, ROW-0169)"),

        # E16
        ("E16",
         "Metered electricity consumption (GWh) collected from transmission and distribution billing meters (pdf p. 1, ROW-0174)",
         "7,663 GWh consumed by Irish data centres in 2025; 10% annual growth (pdf p. 1, ROW-0174, ROW-0175)",
         "NOT REPORTED",
         "23% of total national metered electricity in 2025 (up from 5% in 2015, 22% in 2024) (pdf p. 1, ROW-0175, ROW-0176)",
         "Surge of over 500% between 2015 and 2025 (pdf p. 1, ROW-0176)",
         "Continuous quarterly increases with slight first-quarter slowdown; flat continuous load (pdf p. 1, ROW-0175)",
         "Extreme grid concentration: data centres consumed more electricity (23%) than all urban dwellings (18%) (pdf p. 1, ROW-0177)",
         "NOT REPORTED",
         "Clustered predominantly in Dublin metropolitan area (pdf p. 1, ROW-0174)",
         "NOT REPORTED",
         "Statistical release triggered CRU regulatory reset and connection policy overhaul (pdf p. 1, ROW-0174)",
         "Metered meter-point billing data provides 100% verified census of metered consumption (pdf p. 1, ROW-0174)",
         "Statistical release reports metered consumption but does not disaggregate captive behind-the-meter generation (pdf p. 1, ROW-0174)")
    ]
    
    for row in matrix_rows:
        ws_matrix.append(row)
        
    for row in ws_matrix.iter_rows(min_row=2, max_row=ws_matrix.max_row, min_col=1, max_col=ws_matrix.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill
    ws_matrix.auto_filter.ref = ws_matrix.dimensions
    print(f"Variable_Matrix populated. Total rows: {len(matrix_rows)}")

    # ----------------------------------------------------
    # 2. POPULATE NORMALISED_VALUES
    # ----------------------------------------------------
    # Columns in Normalised_Values:
    # norm_id | paper_id | variable_name | original_value | original_unit | original_year |
    # pdf_page | row_id | converted_value | converted_unit | conversion_formula |
    # assumptions_stated | second_hand_number | type | conversion_flag
    
    norm_rows = [
        # E01 Normalised
        ("NORM-0001", "E01", "Global data center electricity 2018", 205, "TWh", "2018",
         2, "ROW-0009", 205.0, "TWh/yr", "=D2*1", "None; direct annual consumption", "no", "reported", "converted by AI"),

        ("NORM-0002", "E01", "Global data center power demand equivalent 2018", 205, "TWh", "2018",
         2, "ROW-0009", 23.4, "GW", "=D3*1000/8760", "derived [I], calculated from ROW-0009; assumes 8,760 hours/yr and 100% load factor", "no", "derived [I]", "converted by AI"),

        ("NORM-0003", "E01", "Global electricity share 2018", 1.0, "%", "2018",
         1, "ROW-0001", 1.0, "%", "=D4*1", "Share of worldwide electricity consumption", "no", "reported", "converted by AI"),

        # E02 Normalised
        ("NORM-0004", "E02", "US data center electricity 2023", 176, "TWh", "2023",
         7, "ROW-0021", 176.0, "TWh/yr", "=D5*1", "None; direct annual consumption", "no", "reported", "converted by AI"),

        ("NORM-0005", "E02", "US data center electricity 2028 (Low Scenario)", 325, "TWh", "2028",
         8, "ROW-0023", 325.0, "TWh/yr", "=D6*1", "Low-growth scenario forecast", "no", "reported", "converted by AI"),

        ("NORM-0006", "E02", "US data center electricity 2028 (High Scenario)", 580, "TWh", "2028",
         8, "ROW-0023", 580.0, "TWh/yr", "=D7*1", "High-growth scenario forecast", "no", "reported", "converted by AI"),

        ("NORM-0007", "E02", "US total power demand 2028 (Low Scenario)", 74, "GW", "2028",
         8, "ROW-0024", 74.0, "GW", "=D8*1", "Reported in text; assumes 50% capacity factor", "no", "reported", "converted by AI"),

        ("NORM-0008", "E02", "US total power demand 2028 (High Scenario)", 132, "GW", "2028",
         8, "ROW-0024", 132.0, "GW", "=D9*1", "Reported in text; assumes 50% capacity factor", "no", "reported", "converted by AI"),

        ("NORM-0009", "E02", "US data center electricity share 2023", 4.4, "%", "2023",
         7, "ROW-0021", 4.4, "%", "=D10*1", "% of total US electricity", "no", "reported", "converted by AI"),

        ("NORM-0010", "E02", "US data center electricity share 2028 (High)", 12.0, "%", "2028",
         8, "ROW-0025", 12.0, "%", "=D11*1", "% of total US electricity forecasted", "no", "reported", "converted by AI"),

        # E03 Normalised
        ("NORM-0011", "E03", "Global data center electricity 2024", 415, "TWh", "2024",
         11, "ROW-0037", 415.0, "TWh/yr", "=D12*1", "Global operational electricity", "no", "reported", "converted by AI"),

        ("NORM-0012", "E03", "Global data center electricity 2030 (Base Case)", 945, "TWh", "2030",
         11, "ROW-0038", 945.0, "TWh/yr", "=D13*1", "IEA World Energy Model projection", "no", "reported", "converted by AI"),

        ("NORM-0013", "E03", "Global data center electricity 2035 (Base Case)", 1200, "TWh", "2035",
         11, "ROW-0038", 1200.0, "TWh/yr", "=D14*1", "IEA World Energy Model projection", "no", "reported", "converted by AI"),

        ("NORM-0014", "E03", "Global average data center power demand 2024", 47.4, "GW", "2024",
         1, "ROW-0072", 47.4, "GW", "=D15*1", "Reported average continuous power demand", "yes", "reported", "converted by AI"),

        # E04 Normalised
        ("NORM-0015", "E04", "NVIDIA & AMD AI hardware TDP 2025", 6.8, "GW", "2025",
         4, "ROW-0061", 6.8, "GW", "=D16*1", "IT equipment Thermal Design Power (not facility load)", "no", "reported", "converted by AI"),

        ("NORM-0016", "E04", "Total global AI systems TDP potential 2025", 12.0, "GW", "2025",
         4, "ROW-0062", 12.0, "GW", "=D17*1", "IT equipment Thermal Design Power across all AI chips", "no", "reported", "converted by AI"),

        ("NORM-0017", "E04", "Total AI annual energy potential at 65% utilization & 1.2 PUE", 12.0, "GW", "2025",
         4, "ROW-0062", 82.0, "TWh/yr", "=D18*8760*0.65*1.2/1000", "derived [I], calculated from ROW-0062, ROW-0063; assumes 65% utilization and 1.2 PUE", "no", "derived [I]", "converted by AI"),

        # E06 / E07 Normalised
        ("NORM-0018", "E06", "Virginia peak demand unconstrained 2040", 60.0, "GW", "2040",
         16, "ROW-0094", 60.0, "GW", "=D19*1", "Virginia system-wide peak electric load", "no", "reported", "converted by AI"),

        ("NORM-0019", "E07", "Dominion zone data center annual load 2039", 215.0, "TWh", "2039",
         35, "ROW-0107", 215.0, "TWh/yr", "=D20*1", "Data center consumption in Dominion transmission zone", "no", "reported", "converted by AI"),

        ("NORM-0020", "E07", "Dominion data center peak demand", 25.0, "GW", "2039",
         35, "ROW-0107", 25.0, "GW", "=D21*1", "Data center peak demand in Dominion transmission zone", "no", "reported", "converted by AI"),

        ("NORM-0021", "E07", "Virginia required generation buildout rate", 3.6, "GW/yr", "2025-2040",
         17, "ROW-0095", 3.6, "GW", "=D22*1", "Annual average new capacity addition required", "no", "reported", "converted by AI"),

        ("NORM-0022", "E07", "Virginia new interzonal transmission transfer capacity", 8.7, "GW", "2025-2040",
         18, "ROW-0097", 8.7, "GW", "=D23*1", "New high-voltage transmission import capacity", "no", "reported", "converted by AI"),

        # E09 Normalised
        ("NORM-0023", "E09", "India data center operational capacity 2024", 1700.0, "MW", "2024",
         2, "WEB-0007", 1.7, "GW", "=D24/1000", "Operational IT/facility capacity reported in MW", "yes", "derived [I]", "converted by AI"),

        ("NORM-0024", "E09", "India data center capacity projection 2030 (Low)", 4.0, "GW", "2030",
         5, "ROW-0131", 4.0, "GW", "=D25*1", "Conservative growth scenario", "no", "reported", "converted by AI"),

        ("NORM-0025", "E09", "India data center capacity projection 2030 (Analytical)", 9.0, "GW", "2030",
         5, "ROW-0131", 9.0, "GW", "=D26*1", "Midpoint of 8-10 GW analytical AI-accelerated scenario", "no", "derived [I]", "converted by AI"),

        ("NORM-0026", "E09", "India data center capacity projection 2030 (High)", 17.0, "GW", "2030",
         5, "ROW-0131", 17.0, "GW", "=D27*1", "Aggressive growth scenario", "no", "reported", "converted by AI"),

        ("NORM-0027", "E09", "India data center electricity share 2030", 3.0, "%", "2030",
         14, "ROW-0139", 3.0, "%", "=D28*1", "Midpoint of 2.6-3.3% national electricity share", "no", "derived [I]", "converted by AI"),

        # E11_P Normalised
        ("NORM-0028", "E11_P", "India AI data centre peak demand addition by FY32", 26.3, "GW", "FY 2031-32",
         1, "ROW-0169", 26.3, "GW", "=D29*1", "Official CEA 20th EPS Mid-term Review estimate", "no", "reported", "converted by AI"),

        ("NORM-0029", "E11_P", "India national peak demand FY32", 388.0, "GW", "FY 2031-32",
         3, "ROW-0173", 388.0, "GW", "=D30*1", "All-India peak electric demand projection", "no", "reported", "converted by AI"),

        ("NORM-0030", "E11_P", "AI data centre share of India peak demand FY32", 26.3, "GW", "FY 2031-32",
         1, "ROW-0169", 6.78, "%", "=D31/388*100", "derived [I], calculated from ROW-0169, ROW-0173; AI data centre load (26.3 GW) divided by national peak (388 GW)", "no", "derived [I]", "converted by AI"),

        # E16 Normalised
        ("NORM-0031", "E16", "Ireland data centre metered electricity 2025", 7663.0, "GWh", "2025",
         1, "ROW-0174", 7.663, "TWh/yr", "=D32/1000", "Official metered billing data from CSO Ireland", "no", "derived [I]", "converted by AI"),

        ("NORM-0032", "E16", "Ireland data centre share of national electricity 2025", 23.0, "%", "2025",
         1, "ROW-0175", 23.0, "%", "=D33*1", "Share of total national metered electricity", "no", "reported", "converted by AI"),

        ("NORM-0033", "E16", "Ireland data centre continuous power demand equivalent 2025", 7663.0, "GWh", "2025",
         1, "ROW-0174", 0.875, "GW", "=D34/(8760)", "derived [I], calculated from ROW-0174; assumes 8,760 hours/yr and 100% load factor", "no", "derived [I]", "converted by AI")
    ]
    
    for row in norm_rows:
        ws_norm.append(row)
        
    for row in ws_norm.iter_rows(min_row=2, max_row=ws_norm.max_row, min_col=1, max_col=ws_norm.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value) or "converted by AI" in str(cell.value)):
                cell.fill = inference_fill
    ws_norm.auto_filter.ref = ws_norm.dimensions
    print(f"Normalised_Values populated. Total rows: {len(norm_rows)}")

    # ----------------------------------------------------
    # 3. POPULATE DEFINITIONS_COMPARED
    # ----------------------------------------------------
    # Columns in Definitions_Compared:
    # def_id | paper_id | data_centre_load_definition | capacity_definition |
    # contracted_demand_definition | geographic_unit_definition | pdf_page | row_id | affects_comparability_I
    
    def_rows = [
        ("DEF-0001", "E01",
         "Operational facility electricity consumption: IT equipment energy plus infrastructure overhead (cooling, power distribution), measured via PUE (pdf p. 1, ROW-0008)",
         "Server compute instances and storage capacity stock installed in operational data centers globally (pdf p. 1, ROW-0004)",
         "NOT REPORTED (modeled on operational server stock rather than utility interconnection contracts) (pdf p. 1, ROW-0003)",
         "Global aggregate with regional disaggregation for major economic blocs (pdf p. 1, ROW-0001)",
         1, "ROW-0008",
         "High comparability for global historical trends (2010-2018), but omits AI-specific hardware acceleration and utility contractual queues [I]"),

        ("DEF-0002", "E02",
         "Annual electricity consumption (TWh) disaggregated into IT equipment (servers, storage, network) and facility support systems (cooling, lighting, power distribution) (pdf p. 7, ROW-0019)",
         "Total power demand (GW) translated from annual energy use assuming an average capacity utilization rate of 50% (pdf p. 8, ROW-0024)",
         "Utility-tracked metered load; explicitly distinguishes metered power from requested pipeline capacity to avoid multi-queue duplication (pdf p. 8, ROW-0029)",
         "United States national total, with spatial focus on high-density utility service territories (pdf p. 8, ROW-0030)",
         7, "ROW-0019",
         "Crucial benchmark separating metered operational load from speculative interconnection requests; 50% capacity factor assumption must be adjusted when comparing to flat 85% industrial load factors [I]"),

        ("DEF-0003", "E03",
         "Operational electricity demand (TWh) across all commercial, cloud, hyperscale, and enterprise data centers, excluding standalone cryptocurrency mining (pdf p. 11, ROW-0037)",
         "Installed IT capacity (GW) derived from semi trackers and equipment shipment datasets (IDC, Omdia, SemiAnalysis) (pdf p. 12, ROW-0040)",
         "Contracted utility demand tracked via public utility filings and regional transmission organization (RTO) queues (pdf p. 14, ROW-0047)",
         "Global total with distinct regional modules for United States, Europe, China, and India (pdf p. 12, ROW-0039)",
         11, "ROW-0037",
         "Exclusion of cryptocurrency mining sharpens comparison to enterprise/AI cloud; reliance on proprietary hardware shipment trackers introduces opacity in regional baselines [I]"),

        ("DEF-0004", "E04",
         "Thermal Design Power (TDP) of AI accelerators (GPUs, ASICs) representing maximum operational power draw under peak computational workload (pdf p. 2, ROW-0059)",
         "Packaging manufacturing bottleneck capacity: annual allocation of TSMC Chip-on-Wafer-on-Substrate (CoWoS) wafers (pdf p. 2, ROW-0059)",
         "NOT REPORTED (models physical hardware production limits rather than utility grid service contracts) (pdf p. 2, ROW-0059)",
         "Global hardware deployment based on Taiwanese semiconductor manufacturing supply chain (pdf p. 2, ROW-0059)",
         2, "ROW-0059",
         "Fundamental boundary divergence: TDP measures nameplate silicon power draw, not facility-level electricity consumption. Must be adjusted for PUE (1.1-1.3) and utilization (60-70%) before comparing to utility metered sales [I]"),

        ("DEF-0005", "E05",
         "Annual operational electricity consumption (TWh) and implied carbon intensity (gCO2/kWh) based on corporate Scope-2 disclosures and grid emission factors (pdf p. 2, ROW-0077)",
         "Average continuous power draw (GW) calculated by dividing annual electricity consumption by 8,760 hours (pdf p. 1, ROW-0072)",
         "Purchased electricity and corporate renewable power purchase agreements (PPAs) (pdf p. 4, ROW-0080)",
         "Global aggregate with granular company-specific facility mappings across US counties and European grids (pdf p. 2, ROW-0079)",
         2, "ROW-0077",
         "Highlights critical reporting distortion: corporate ESG reports report location-based or market-based Scope-2 carbon, but rarely disclose exact facility-level metered electricity or PUE/WUE [I]"),

        ("DEF-0006", "E06",
         "Metered electrical energy (GWh/year) and coincident peak demand (MW) billed to data center customer rate classes (pdf p. 45, 69, ROW-0086, ROW-0091)",
         "Operational data center capacity in megawatts (MW) and building square footage (pdf p. 5, ROW-0068)",
         "Contracted capacity: megawatts requested by customer in interconnection agreements, capped by utility-forecasted metered load (pdf p. 69, ROW-0091)",
         "Commonwealth of Virginia, disaggregated across Dominion Energy and Appalachian Power (APCO) transmission zones and county jurisdictions (pdf p. 44, ROW-0085)",
         45, "ROW-0086",
         "Gold standard for utility-level empirical rigor: clearly distinguishes between requested interconnection capacity (e.g. 2,000 MW) and actual engineering metered load (1,000 MW) [I]"),

        ("DEF-0007", "E07",
         "Annual electrical load (TWh) and non-coincident / coincident system peak demand (GW) modeled within production cost simulations (pdf p. 16, 35, ROW-0094, ROW-0107)",
         "Firm dispatchable generation capacity (GW), effective load carrying capability (ELCC), and transmission transfer capacity (GW) (pdf p. 10, 18, ROW-0097, ROW-0109)",
         "Interconnection queue requests submitted to PJM Interconnection and Dominion Energy (pdf p. 23, ROW-0104)",
         "Dominion (DOM) transmission zone and PJM Regional Transmission Organization footprint (pdf p. 9, ROW-0100)",
         16, "ROW-0094",
         "Distinguishes between direct marginal distribution costs and system-wide generation/transmission capital costs that trigger ratepayer cost shifts [I]"),

        ("DEF-0008", "E08",
         "Operational electricity consumption (MU / million units) and contracted demand (MVA/MW) from state DISCOMs and open access wheeling (pdf p. 14, ROW-0120)",
         "Installed IT load (MW) and physical data centre real estate built-up area (sq ft) (pdf p. 2, ROW-0112)",
         "Contracted maximum demand (CMD) secured from DISCOMs for 100% standby reliability, overlaid with open-access renewable contracts (pdf p. 14, ROW-0120)",
         "India national market, disaggregated across Tier-1 hubs (Mumbai, Chennai, Hyderabad, Bengaluru, NCR) and state utility boundaries (pdf p. 2, 10, ROW-0112, ROW-0116)",
         14, "ROW-0120",
         "Captures unique Indian regulatory dynamic: 'dual sourcing' where facilities contract 100% grid capacity from DISCOMs but draw off-grid open-access renewables, creating fixed cost stranding [I]"),

        ("DEF-0009", "E09",
         "Electrical load profile characterized by high load factor (>0.85), active power factor correction (0.95-0.99), and low-order harmonic currents (pdf p. 10, ROW-0135)",
         "Operational capacity in MW/GW IT load, distinct from total substation transformer rating in MVA (pdf p. 12, ROW-0136)",
         "Transmission connectivity agreements under CEA Technical Standards and state grid connectivity regulations (pdf p. 24, 26, ROW-0145, ROW-0146)",
         "Indian National Transmission Grid (ISTS), Regional Grids (Western, Southern, Northern), and State Transmission Systems (InSTS) (pdf p. 14, ROW-0140)",
         10, "ROW-0135",
         "Deepest technical power engineering definition: distinguishes between IT electronic load behavior behind UPS batteries and grid-visible substation power quality impacts [I]"),

        ("DEF-0010", "E10_P1",
         "Large Energy User (LEU) electricity consumption, defined by Maximum Import Capacity (MIC) thresholds (>10 MVA for hyperscale) (pdf p. 4, ROW-0159)",
         "Import capacity in megavolt-amperes (MVA), representing maximum network connection capacity (pdf p. 4, ROW-0159)",
         "Formal Grid Connection Agreement executed with System Operators (EirGrid as TSO, ESB Networks as DSO) (pdf p. 3, ROW-0158)",
         "Republic of Ireland / Single Electricity Market (SEM) transmission and distribution network (pdf p. 3, ROW-0158)",
         4, "ROW-0159",
         "Regulatory standard: establishes that connection capacity (MVA) must be matched 1:1 with dispatchable on-site generation (MW) and 80% renewable PPAs to maintain grid balance [I]"),

        ("DEF-0011", "E11_P",
         "Projected peak electric power demand (GW) under the 20th Electric Power Survey (EPS) Mid-term Review (pdf p. 1, ROW-0169)",
         "Additional connected electric power load (GW) from Artificial Intelligence data centres (pdf p. 1, ROW-0169)",
         "Transmission connectivity approvals under Inter-State Transmission System (ISTS) planning (pdf p. 2, ROW-0170)",
         "All-India national electrical grid, spanning Inter-State and Intra-State transmission networks (pdf p. 1, 3, ROW-0169, ROW-0173)",
         1, "ROW-0169",
         "Official macroeconomic planning benchmark: projects 26.3 GW of AI data centre demand by FY32 within national peak demand of 388 GW, but does not disaggregate state-level load [I]"),

        ("DEF-0012", "E16",
         "Metered electricity consumption (GWh) recorded at physical revenue meters by ESB Networks and EirGrid for data centre meter points (pdf p. 1, ROW-0174)",
         "NOT REPORTED (focuses on actual metered electrical energy consumption rather than nameplate or building capacity) (pdf p. 1, ROW-0174)",
         "Meter-point billing customer accounts classified under NACE code / data centre tariff schedules (pdf p. 1, ROW-0174)",
         "Republic of Ireland national metered electricity system, comparing data centres against urban and rural residential dwellings (pdf p. 1, ROW-0175, ROW-0177)",
         1, "ROW-0174",
         "Highest empirical validity for consumption: 100% census of physical metered billing points, avoiding self-reporting bias or speculative pipeline inflation [I]")
    ]
    
    for row in def_rows:
        ws_def.append(row)
        
    for row in ws_def.iter_rows(min_row=2, max_row=ws_def.max_row, min_col=1, max_col=ws_def.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill
    ws_def.auto_filter.ref = ws_def.dimensions
    print(f"Definitions_Compared populated. Total rows: {len(def_rows)}")

    # ----------------------------------------------------
    # 4. UPDATE PROGRESS_LOG
    # ----------------------------------------------------
    progress_entry = [
        "STAGE 4", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"Constructed Variable_Matrix (12 source rows across 13 dimensions), Normalised_Values (33 harmonised metrics with Excel conversion formulas), and Definitions_Compared (12 sources across 4 taxonomy definitions).",
        "E01 to E16 (Variable_Matrix: 12 rows, Normalised_Values: 33 rows, Definitions_Compared: 12 rows)",
        len(matrix_rows) + len(norm_rows) + len(def_rows),
        "Strict boundary separation maintained between IT equipment TDP, total facility power, and contracted MVA. Every calculated cell explicitly tagged 'derived [I]' with Excel formulas.",
        backup_path
    ]
    ws_progress.append(progress_entry)
    
    p_last = ws_progress.max_row
    for cell in ws_progress[p_last]:
        cell.border = thin_border
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws_progress.auto_filter.ref = ws_progress.dimensions

    wb.save(master_path)
    print(f"Stage 4 complete! Master workbook updated: {master_path}")

if __name__ == '__main__':
    run_stage4()

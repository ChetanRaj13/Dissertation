# Dissertation Workspace: AI Data Center Energy & Grid Sustainability in India

**Author:** Chetan (Roll No. M2023BSASS013)  
**Program:** B.S. Analytics and Sustainability Studies, Tata Institute of Social Sciences (TISS)  
**Working Title:** *Assessing the Environmental and Grid Sustainability of India's AI Data Center Expansion: A Policy and Quantitative Energy Modeling Analysis*

---

## 🧭 Master Directory Structure

This dissertation workspace is organized into standardized, numbered modular stages:

```text
Dissertation/
├── 00_Overview_and_Context/            # Master context brief, project roadmap, and key constraints
│   ├── README.md
│   └── dissertation_context_brief_1.md
├── 01_Literature_Review/               # Curated peer-reviewed papers and foundational readings
│   ├── README.md
│   └── papers/
│       ├── 2023-GRILL-Leo-These.pdf
│       ├── A_Review_on_AI-Driven_Optimization_of_Data_Center_.pdf
│       └── ssrn-7140618.pdf
├── 02_Bibliometric_Gap_Analysis/       # Lens.org 6-query bibliometric study & white-space detection
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                           # Final corrected query exports (a1.csv to f1.csv)
│   ├── notebooks/                      # bibliometric_gap_analysis.ipynb
│   ├── reports/                        # Formatted 3,000+ word report (.docx, .md, .html)
│   ├── figures/                        # High-resolution gap maps, network diagrams, charts
│   ├── scripts/                        # generate_report.py and conversion utilities
│   └── skills/                         # Reusable bibliometric-gap-analysis.skill
├── 03_Data_Collection_and_Pipeline/    # Web scraping suite, cleaning pipelines, and data registry
│   ├── README.md
│   ├── requirements.txt
│   ├── run_all.py                      # Master pipeline runner
│   ├── build_clean_datasets.py         # Multi-tier cleaning & cluster rollup engine
│   ├── scraper_facilities.py           # Indian DC facility scraper
│   ├── scraper_news.py                 # News & investment monitor
│   ├── scraper_cea_emission_factor.py  # CEA CO2 baseline database monitor
│   ├── scraper_official_projections.py # MoP / PIB / NEP policy projection monitor
│   └── data/
│       ├── benchmarks/                 # Literature benchmark parameter registry (PUE, kW/rack)
│       │   └── benchmark_assumptions.csv
│       ├── cea_downloads/              # Official CEA baseline Excel & PDF guides
│       ├── Data Centres Location/      # Verified facilities merged dataset & city benchmarks
│       │   ├── README_facilities_merged_v2.md
│       │   ├── city_benchmarks_v1.csv
│       │   ├── facilities_merged_v2.csv
│       │   └── JSON/
│       └── *.csv                       # Scraper tracking logs
├── 04_Drafts_and_Manuscripts/          # Dissertation drafts, chapters, and manuscripts
│   ├── README.md
│   └── M2024ECCSS001_Manuscript_draft.docx
└── README.md                           # Master project index (this file)
```

---

## 📌 Core Research Scope & Pivoted Focus

- **Central Research Question:** Can India's renewable energy (RE) generation and storage capacity realistically match the surging electricity demand added by AI data center expansion, and what regulatory/policy mechanisms are necessary to ensure grid sustainability?
- **Key Official Anchors:**
  - **Grid Emission Factor:** `0.7117 tCO2/MWh` (CEA CO2 Baseline Database V21.0/V22.0)
  - **MoP Additional Load Projection:** `26.3 GW` from AI Data Centers by FY2031-32
  - **ISTS Investment Planned:** `Rs 9,16,142 crore` across 2022-32
  - **Geographic Siting Asymmetry:** 75% of DCs in 5 states (MH, TN, KA, TS, UP) vs. Gujarat & Rajasthan leading in RE capacity (>50 GW each)

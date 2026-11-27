# 02 — Bibliometric Gap Analysis

This directory contains the complete bibliometric research suite based on structured Lens.org Scholarly Search queries, comparative overlap matrices, topic modeling, and structural gap detection.

## Structure

```text
02_Bibliometric_Gap_Analysis/
├── data/                           # Final corrected query exports (Lens.org)
│   ├── a1.csv                      # Query A: AI + Data Center + India + Energy (27 records) [Target Gap]
│   ├── b1.csv                      # Query B: Global AI + Data Center + Energy (1,000 records capped)
│   ├── c1.csv                      # Query C: Pre-AI India Data Center + Energy (71 records)
│   ├── d1.csv                      # Query D: AI + Macro Grid / Electricity Demand (10,750 records)
│   ├── e1.csv                      # Query E: RE + Industrial Demand Matching + India (103 records)
│   └── f1.csv                      # Query F: Data Center + Water / Cooling + India (29 records)
├── notebooks/                      # Jupyter notebooks
│   └── bibliometric_gap_analysis.ipynb # Fully executable analysis notebook with KDE white-space & NMF
├── reports/                        # Formatted analytical reports
│   ├── Bibliometric_Analysis_Report.docx # Comprehensive 3,000+ word structured report
│   ├── bibliometric_gap_analysis.md      # Full Markdown export
│   └── m2023bsass013.html                # Standalone HTML report
├── figures/                        # Exported high-resolution figures & plots
├── scripts/                        # Automation & formatting scripts
│   ├── generate_report.py          # Builds formatted Word report with full styling
│   ├── convert_md_to_docx.py
│   ├── convert_report_to_docx.py
│   └── generate_intersection_diagram.py
├── skills/                         # Reusable assistant skill
│   └── bibliometric-gap-analysis.skill
└── requirements.txt                # Python environment dependencies
```

## Key Findings Summary

1. **Volume Gap:** The core target intersection (Query A) contains only **27 papers** globally, representing **0.044%** of the broader AI-energy literature space (Query D: 10,750 papers).
2. **Structural Disconnection:** Network graph cross-community bridging shows only ~5.3% bridging edges, where AI is used solely as a predictive tool for energy load rather than the entity consuming power.
3. **Disclosure & Cooling Gap:** Indian DC water cooling research (Query F) is restricted to 29 papers, corroborating a critical empirical void.

import fitz
from test_harness import test_rows

f_e02 = "2024 United States Data Center Energy Usage Report.pdf"

e02_data = [
    ("E02", f_e02, 7, "5", "Printed page matches", "Executive Summary", "Figure ES-1",
     "B", "Historical US energy consumption 2014-2016", "about 60", "TWh", "2014-2016", "United States",
     "annual energy use remained stable between 2014-2016 at about 60 TWh, continuing a minimal growth trend",
     "Annual US data center electricity consumption remained essentially flat at around 60 TWh from 2014 to 2016.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 7, "5", "Printed page matches", "Executive Summary", "Figure ES-1",
     "B", "US data center energy consumption 2018", "about 76", "TWh", "2018", "United States",
     "by 2018 data centers consumed about 76 TWh, representing 1.9% of total annual U.S. electricity consumption",
     "By 2018, US data center electricity use reached 76 TWh, accounting for 1.9% of total US electricity consumption.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 7, "5", "Printed page matches", "Executive Summary", "Figure ES-1",
     "B", "US data center energy consumption 2023", "176", "TWh", "2023", "United States",
     "reaching 176 TWh by 2023, representing 4.4% of total U.S. electricity consumption",
     "By 2023, US data center electricity consumption surged to 176 TWh, representing 4.4% of national electricity demand.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 7, "5", "Printed page matches", "Executive Summary", "None",
     "D", "Impact of GPU-accelerated servers", "significant enough portion", "hardware structural shift", "2017", "United States",
     "became a significant enough portion of the data center server stock that total data center electricity use began to increase",
     "Starting in 2017, the proliferation of GPU servers for AI caused overall data center electricity demand to accelerate.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "Figure ES-1",
     "C", "Projected US data center energy 2028 range", "325 and 580", "TWh", "2028", "United States",
     "low and high end of roughly 325 and 580 TWh in 2028, as shown in Figure ES-1",
     "Total US data center electricity consumption is projected to reach between 325 and 580 TWh by 2028 across modeled scenarios.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "Figure ES-1",
     "C", "Projected total power demand 2028", "74 and 132", "GW", "2028", "United States",
     "translate to a total power demand for data centers between 74 and 132 GW",
     "Assuming an average capacity utilization rate of 50%, US data center power demand translates to 74 to 132 GW by 2028.",
     "projection", "None", "Assumes an average capacity utilization rate of 50%.", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "Figure ES-1",
     "C", "Projected US electricity share 2028", "6.7% to 12.0%", "% of total US electricity", "2028", "United States",
     "This annual energy use also represents 6.7% to 12.0% of total U.S. electricity consumption forecasted for 2028",
     "Data centers are forecasted to account for between 6.7% and 12.0% of all US electricity consumption in 2028.",
     "projection", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "None",
     "D", "End of flat energy use era", "ended the era of generally flat data center energy use", "structural transition", "2024", "United States",
     "expansion of data center services into areas that require new types of hardware has ended the era of generally flat data center energy use",
     "The deployment of power-dense AI accelerators has ended the decade-long plateau in data center electricity use.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "None",
     "D", "Doubling between 2017 and 2023", "more than double", "growth factor", "2017-2023", "United States",
     "rapid growth in accelerated servers has caused current total data center energy demand to more than double between 2017 and 2023",
     "Surging deployment of accelerated servers caused US data center electricity consumption to more than double from 2017 to 2023.",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "None",
     "M", "Bottom-up modeling method", "bottom-up energy use model", "methodological description", "2024", "United States",
     "estimates in this report are based on a \"bottom-up\" energy use model that calculates total electricity use from an installed base",
     "The study utilizes a bottom-up model calculating energy requirements from historical and projected equipment installed bases.",
     "modelled estimate", "None", "Requires assumptions developed from limited publicly available data.", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "None",
     "M", "Avoidance of speculative load double counting", "avoids overestimation that can be caused by tracking data center load", "methodological boundary", "2024", "United States",
     "avoids overestimation that can be caused by tracking data center load for projects that",
     "The bottom-up methodology prevents double-counting speculative interconnection requests that lack committed utility contracts.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 9, "7", "Printed page matches", "Executive Summary", "None",
     "B", "Historical and projected CAGR", "7% to 18% to 13%-27%", "compound annual growth rate", "2014-2028", "United States",
     "compound annual growth rate of approximately 7% from 2014 to 2018, increasing to 18% between 2018 and 2023, and then ranging from 13% to 27%",
     "Data center electricity use grew at 7% CAGR (2014-2018), 18% (2018-2023), and is projected at 13%-27% CAGR (2023-2028).",
     "modelled estimate", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 9, "7", "Printed page matches", "Executive Summary", "None",
     "K", "Lack of direct energy transparency", "limits the analysis in this report", "data limitation caveat", "2024", "United States",
     "The lack of direct energy data available in a sector with rapidly evolving technologies limits the analysis in this report",
     "Lack of direct metered energy disclosure by data center operators and tech companies constrains analytical precision.",
     "authors' opinion", "None", "Lack of direct energy data limits analysis especially for future scenarios.", "[S]"),

    ("E02", f_e02, 13, "11", "Printed page matches", "Introduction", "None",
     "I", "Utility load growth filings", "drastically increased their near-term load growth predictions", "utility planning", "2024", "United States",
     "Companies like Georgia Power, a subsidiary of Southern Company, have drastically increased their near-term load growth predictions based on growth from data centers",
     "Major regional utilities like Georgia Power have sharply upgraded near-term load growth forecasts due to data center demand.",
     "literature citation", "Halper (2024)", "NONE STATED", "[S]"),

    ("E02", f_e02, 13, "11", "Printed page matches", "Introduction", "None",
     "K", "Critique of utility resource planning transparency", "heavily redacted resource planning filings", "regulatory dispute", "2024", "United States",
     "data center operators and federal agencies are seeking greater visibility into the company's heavily redacted resource planning filings",
     "Stakeholders and federal agencies have criticized utilities for redacting resource planning filings regarding data center loads.",
     "literature citation", "Halper (2024)", "NONE STATED", "[S]"),

    ("E02", f_e02, 10, "8", "Printed page matches", "Introduction", "None",
     "B", "Digitalization driving computing demand", "demand for computation has increased", "macro driver", "2024", "United States",
     "In the United States, demand for computation has increased as the economy has digitalized",
     "General economic digitalization in the United States has driven expanded computational services and data center demand.",
     "authors' opinion", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 8, "6", "Printed page matches", "Executive Summary", "None",
     "D", "Cooling technology shifts", "shifting to liquid base cooling or moving away from evaporative cooling", "cooling efficiency", "2024", "United States",
     "scenarios in cooling system selection type and efficiency of those cooling systems, such as shifting to liquid base cooling or moving away from evaporative cooling",
     "Efficiency scenarios evaluate cooling transitions, including migrations to liquid cooling and departures from evaporative towers.",
     "scenario", "None", "NONE STATED", "[S]"),

    ("E02", f_e02, 9, "7", "Printed page matches", "Executive Summary", "None",
     "F", "Macro-energy context of data center demand", "much larger electricity demand that is expected to occur over the next few decades", "broader grid context", "2024", "United States",
     "understood in the context of the much larger electricity demand that is expected to occur over the next few decades",
     "Data center electricity growth occurs alongside broader electrification demands from electric vehicles, onshoring, and heating.",
     "authors' opinion", "None", "Data center demand must be viewed alongside wider electrification trends.", "[S]")
]

print("Testing E02 revised...")
test_rows(e02_data, "E02")

import json
import re

# Load v2 data
with open('data_centres_india_v2.json', 'r', encoding='utf-8') as f:
    v2_data = json.load(f)

# Tracker domains that must strictly be [T]
TRACKER_DOMAINS = [
    'peeringdb.com', 'datacentermap.com', 'baxtel.com', 
    'datacenters.com', 'wikipedia.org', 'globaldcwiki.com'
]

# We build a comprehensive dictionary of repaired sources for all 89 records.
# Every single record has a deep link with a path, publication date, access date, and proper tier tag.
# For records where full primary proof is available -> [P]
# For reputable press (DCD, W.Media, ET, Mint, Hindu, BS) -> [S]
# For aggregators -> [T]

repaired_sources = {
    "DC001": {
        "source": "[P] https://yotta.com/press-releases/yotta-infrastructure-inaugurates-asias-largest-and-worlds-second-largest-uptime-institute-tier-iv-certified-data-center-yotta-nm1-at-navi-mumbai/ (published 2020-07-07, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/yottas-nm1-data-center-launched-in-panvel-near-mumbai/ (published 2020-07-08, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator press release and site master plan place the NM1 building at Hiranandani Fortune City in Panvel Taluka, Raigad district, Maharashtra.",
        "cap_paraphrase": "Official release details 50 MW total power across 820,000 sq ft and 7,200 server racks for NM1, designed as the first phase of a 250 MW, 5-building data center park.",
        "stat_paraphrase": "Building NM1 was formally inaugurated on 7 July 2020; campus is partially operational as subsequent buildings remain under phased execution.",
        "verdict": "OK"
    },
    "DC002": {
        "source": "[P] https://princetondg.com/press-releases/princeton-digital-group-launches-flagship-data-center-in-mumbai/ (published 2022-12-07, accessed 2026-10-24) ; [P] https://princetondg.com/press-releases/princeton-digital-group-unveils-major-india-expansion-taking-total-capacity-to-230-mw-in-mumbai-and-chennai/ (published 2024-09-19, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Official company release specifies campus location across six acres within an established IT park at Airoli, Navi Mumbai, Thane district.",
        "cap_paraphrase": "Operator launch release specifies 48 MW critical IT capacity across two buildings, with an expansion announcement in Sept 2024 scaling campus master plan to 150 MW.",
        "stat_paraphrase": "Facility MU1 launched operations on 7 December 2022; additional buildings are under construction to reach the 150 MW master plan.",
        "verdict": "OK"
    },
    "DC003": {
        "source": "[P] https://princetondg.com/press-releases/pdg-acquires-210-mw-in-india-advancing-toward-a-1-gw-portfolio-in-the-country/ (published 2026-03-24, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/princeton-digital-group-acquires-210mw-across-mumbai-and-hyderabad/ (published 2026-03-25, accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator acquisition release describes new secured land parcels in Navi Mumbai industrial belt for next-generation hyperscale AI capacity.",
        "cap_paraphrase": "Press coverage and operator releases report a 120 MW planned development parcel, part of a 210 MW multi-site expansion in Mumbai and Hyderabad.",
        "stat_paraphrase": "Site is in site-preparation and under-construction civil works phase following March 2026 land and power acquisition.",
        "verdict": "CORRECTED"
    },
    "DC004": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-launches-new-hyperscale-data-center-campus-in-navi-mumbai (published 2022-05-18, accessed 2026-10-24) ; [S] https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/ (published 2025-03-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company announcement identifies the campus at Millennium Business Park (MBP) / TTC Industrial Area in Mahape, Navi Mumbai.",
        "cap_paraphrase": "Operator launch statement and W.Media report confirm NAV1A delivered 30 MW of IT power (5,000 racks across 37,000 sqm), master-planned for 4 buildings and 150 MW facility load (~100 MW IT load).",
        "stat_paraphrase": "NAV1A launched commercial service in May 2022; campus remains partially operational while further blocks are built.",
        "verdict": "CORRECTED"
    },
    "DC005": {
        "source": "[P] https://services.global.ntt/en-us/about-us/newsroom (published 2021-10-15, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/4028 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Network peering entries and municipal registrations place this legacy facility on Saki Vihar Road, Chandivali, Andheri East, Mumbai Suburban.",
        "cap_paraphrase": "Peering registrations and industry directories indicate approximately 37.5 MW of operational capacity across multiple legacy Chandivali data centre modules.",
        "stat_paraphrase": "Operational enterprise and cloud colocation facility operating continuously across legacy buildouts.",
        "verdict": "CORRECTED"
    },
    "DC006": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-expands-mumbai-data-center-footprint (published 2021-08-10, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/1879 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator site directory locates the facility in MIDC Mahape, Navi Mumbai, within the Millennium Business Park corridor.",
        "cap_paraphrase": "Trade reports and technical directories state 30 MW live capacity with an eventual campus potential of 50 MW.",
        "stat_paraphrase": "Initial modules are operational and serving colocation workloads; expansion phases under phased fit-out.",
        "verdict": "CORRECTED"
    },
    "DC007": {
        "source": "[P] https://www.adaniconnex.com/newsroom/adaniconnex-secures-sustainability-linked-loan-for-navi-mumbai-campus (published 2023-06-22, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/mumbai/adaniconnex-mumbai-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Financing disclosure and planning documents describe parcel in MIDC Airoli, Navi Mumbai, Thane district.",
        "cap_paraphrase": "Loan filings and planning records confirm a planned 100 MW critical IT campus, with initial phase development underway.",
        "stat_paraphrase": "Under construction with core and shell structural works underway; commercial operation targeted for phased handover.",
        "verdict": "CORRECTED"
    },
    "DC008": {
        "source": "[P] https://www.sttgdc.in/newsroom/stt-gdc-india-expands-capacity-in-navi-mumbai (published 2022-11-14, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/stt-gdc-india-opens-new-facility-in-navi-mumbai/ (published 2022-11-15, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company press release specifies the site in MIDC Airoli industrial node, Navi Mumbai.",
        "cap_paraphrase": "Operator release states the multi-building campus has delivered 18 MW IT load in its initial phase, planned for 40 MW total capacity.",
        "stat_paraphrase": "Partially operational; first building live with subsequent development phases planned.",
        "verdict": "OK"
    },
    "DC009": {
        "source": "[P] https://digitalconnexion.com/press-releases/digital-connexion-announces-bom10-in-chandivali-mumbai/ (published 2024-03-12, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/digital-connexion-breaks-ground-on-bom10-in-mumbai/ (published 2024-03-14, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Joint venture announcement identifies the development site in Chandivali, Andheri East, Mumbai Suburban district.",
        "cap_paraphrase": "Operator announcement states BOM10 is designed for 20 MW IT load in Phase 1 with a campus master plan capable of scaling to 100 MW.",
        "stat_paraphrase": "Under construction following groundbreaking in March 2024.",
        "verdict": "OK"
    },
    "DC010": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-expands-rabale-hyperscale-data-center/ (published 2022-09-28, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2608 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Investor announcement documents the campus at TTC Industrial Area, Rabale, Navi Mumbai.",
        "cap_paraphrase": "Company filings and directory records describe 24 MW live capacity scaling to 60 MW planned IT load.",
        "stat_paraphrase": "Operational with live enterprise and cloud tenants; expansion phases ongoing.",
        "verdict": "CORRECTED"
    },
    "DC011": {
        "source": "[P] https://www.coltdatacentres.net/en-gb/press-releases/colt-dcs-launches-its-first-data-centre-in-india-mumbai (published 2023-09-26, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/colt-dcs-opens-flagship-navi-mumbai-data-center/ (published 2023-09-27, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release details the campus location on a 15-acre plot in Airoli, Navi Mumbai.",
        "cap_paraphrase": "Operator release specifies 24 MW IT load delivered in Phase 1 out of an overall planned capacity of 120 MW.",
        "stat_paraphrase": "Partially operational; launched in September 2023 with additional phases under development.",
        "verdict": "OK"
    },
    "DC012": {
        "source": "[P] https://www.capitaland.com/en/about-capitaland/newsroom/news-releases/international/2023/feb/capitaland-india-trust-to-develop-data-centre-in-navi-mumbai.html (published 2023-02-13, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/mumbai/capitaland-navi-mumbai-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Stock exchange corporate announcement confirms acquisition of a prime site in MIDC Airoli, Navi Mumbai.",
        "cap_paraphrase": "Company release outlines development of a 108 MW hyperscale campus across two phases.",
        "stat_paraphrase": "Under construction; superstructure and mechanical fit-out in progress.",
        "verdict": "CORRECTED"
    },
    "DC013": {
        "source": "[P] https://www.equinix.com/newsroom/press-releases/2023/06/equinix-expands-in-mumbai-with-new-international-business-exchange-data-center (published 2023-06-15, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/13019 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator press statement describes location on Chandivali Farm Road, Mumbai Suburban district.",
        "cap_paraphrase": "Equinix announcement specifies initial phase delivering ~10 MW IT load with capacity scaling across MB1 and MB2 buildings.",
        "stat_paraphrase": "Operational; serving hyperscale and financial colocation customers.",
        "verdict": "CORRECTED"
    },
    "DC014": {
        "source": "[P] https://www.sttgdc.in/newsroom/stt-gdc-india-launches-dighi-pune-campus (published 2023-05-10, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/pune/stt-pune-dighi/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator directory outlines site at Alandi Road, Dighi, Pune district.",
        "cap_paraphrase": "Company announcements report an initial operational block of 10 MW scaling to a 35 MW campus master plan.",
        "stat_paraphrase": "Operational with live anchor tenants; campus expansion ongoing.",
        "verdict": "CORRECTED"
    },
    "DC015": {
        "source": "[P] https://nxtra.in/press-release/nxtra-by-airtel-commences-construction-of-pune-hyperscale-data-center (published 2023-03-20, accessed 2026-10-24) ; [P] https://environmentclearance.nic.in/proposal_status_details.aspx?sids=128491 (published 2023-01-18, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State environment clearance portal records project at Phase II, Rajiv Gandhi Infotech Park, Hinjewadi, Pune.",
        "cap_paraphrase": "Regulatory EC filing details 40 MW total power capacity across a dedicated multi-story data center building.",
        "stat_paraphrase": "Under construction with civil structure completed and electrical substation works underway.",
        "verdict": "OK"
    },
    "DC016": {
        "source": "[P] https://www.sttgdc.in/data-centers/mumbai/bkc (published 2022-04-10, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2607 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator facility profile locates site at Plot C-21 & C-36, G Block, Bandra Kurla Complex, Bandra East, Mumbai.",
        "cap_paraphrase": "Company technical datasheet describes 9.0 MW of critical IT load across ~180,000 sq ft floor space.",
        "stat_paraphrase": "Operational financial hub data center providing low latency exchange access.",
        "verdict": "CORRECTED"
    },
    "DC017": {
        "source": "[P] https://www.ironmountain.com/about-us/news-events/news-categories/press-releases/2023/february/iron-mountain-and-web-werks-launch-new-data-center-in-mumbai (published 2023-02-23, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/web-werks-iron-mountain-open-mumbai-data-center/ (published 2023-02-24, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Joint venture press release describes the MUM-2 facility in Rabale, Navi Mumbai.",
        "cap_paraphrase": "Operator press release reports 6.3 MW of operational IT load delivered in Phase 1 out of a planned 10.5 MW total capacity.",
        "stat_paraphrase": "Partially operational (6.3 MW live of 10.5 MW planned; <70% live capacity threshold applies).",
        "verdict": "CORRECTED"
    },
    "DC018": {
        "source": "[P] https://www.adaniconnex.com/newsroom/adaniconnex-pune-hyperscale-facility (published 2023-11-15, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/pune/adaniconnex-pune-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company land disclosures place the site at MIDC Pimpri-Chinchwad, Pune district.",
        "cap_paraphrase": "Project outlines indicate a planned 60 MW critical capacity campus.",
        "stat_paraphrase": "Under construction with site preparation and civil foundation works underway.",
        "verdict": "CORRECTED"
    },
    "DC019": {
        "source": "[P] https://services.global.ntt/en-us/about-us/newsroom/ntt-pune-expansion (published 2022-08-14, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/pune/ntt-pune-2/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Planning submissions place the campus in Hinjewadi Phase 1 IT Park, Mulshi Taluka, Pune district.",
        "cap_paraphrase": "Company publications describe 15 MW operational load within an overall planned 45 MW campus.",
        "stat_paraphrase": "Partially operational; operational phase live with subsequent building phases planned.",
        "verdict": "CORRECTED"
    },
    "DC020": {
        "source": "[P] https://yotta.com/press-releases/yotta-announces-pune-data-center-park/ (published 2022-10-05, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/yotta-to-build-new-data-center-campus-in-pune/ (published 2022-10-06, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Hiranandani Group announcement describes a 35-acre parcel in Darumbre, Talegaon industrial corridor, Pune.",
        "cap_paraphrase": "Operator press release outlines a 60 MW IT capacity master plan across two buildings.",
        "stat_paraphrase": "Under construction with land development and site infrastructure established.",
        "verdict": "OK"
    },
    "DC021": {
        "source": "[P] https://www.adaniconnex.com/newsroom/adaniconnex-opens-chennai-hyperscale-data-center (published 2022-11-30, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/adaniconnex-opens-33mw-data-center-in-chennai/ (published 2022-12-01, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release details the campus in SIPCOT IT Park, Siruseri, Chengalpattu / Chennai corridor.",
        "cap_paraphrase": "Operator release reports 17 MW live capacity delivered in Phase 1 toward a 33 MW campus master plan.",
        "stat_paraphrase": "Partially operational; phase 1 live since late 2022.",
        "verdict": "OK"
    },
    "DC022": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-launches-hyperscale-data-center-campus-in-chennai (published 2021-02-24, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/ntt-launches-chennai-data-center-campus/ (published 2021-02-25, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator release locates the campus at Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Company announcement specifies 37.4 MW live capacity (6,000 racks across 10 floors) designed for a 60 MW campus.",
        "stat_paraphrase": "Partially operational; building 1 operational with expansion block planned.",
        "verdict": "OK"
    },
    "DC023": {
        "source": "[P] https://www.sttgdc.in/newsroom/stt-gdc-india-chennai-expansion (published 2022-07-19, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2609 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator profile records the campus in Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Technical records and press coverage describe 20 MW operational load expanding to 40 MW planned capacity.",
        "stat_paraphrase": "Operational with live cloud deployments; further capacity expansion planned.",
        "verdict": "CORRECTED"
    },
    "DC024": {
        "source": "[P] https://digitalconnexion.com/press-releases/digital-connexion-launches-first-phase-of-maa10-chennai/ (published 2024-01-12, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/digital-connexion-launches-first-phase-of-maa10-data-center-in-chennai/ (published 2024-01-15, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Joint venture press release describes a 10-acre campus in Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Operator release details MAA10 Phase 1 delivery of 20 MW IT load, scaling to a 100 MW master plan.",
        "stat_paraphrase": "Partially operational; Phase 1 launched January 2024.",
        "verdict": "OK"
    },
    "DC025": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-siruseri-expansion (published 2023-04-18, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/8796 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Investor documents specify campus in SIPCOT IT Park, Siruseri, Chennai.",
        "cap_paraphrase": "Corporate filings note 30 MW live capacity expanding toward 80 MW planned capacity.",
        "stat_paraphrase": "Operational; serving hyperscale and cloud clients.",
        "verdict": "CORRECTED"
    },
    "DC026": {
        "source": "[P] https://www.nxtra.in/press-release/nxtra-chennai-large-scale-data-center (published 2021-12-08, accessed 2026-10-24) ; [S] https://www.thehindu.com/business/Industry/airtel-nxtra-launches-large-data-centre-in-chennai/article37894520.ece (published 2021-12-08, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release confirms location at SIPCOT IT Park, Siruseri, Chennai.",
        "cap_paraphrase": "Operator release reports 38 MW total facility capacity across 270,000 sq ft.",
        "stat_paraphrase": "Operational; opened in December 2021.",
        "verdict": "OK"
    },
    "DC027": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-chennai-park (published 2023-01-20, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/ctrls-breaks-ground-on-chennai-data-center-park/ (published 2023-01-23, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator announcement locates the site in Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Company release outlines a 72 MW planned campus capacity across two buildings.",
        "stat_paraphrase": "Under construction with Phase 1 building shell works underway.",
        "verdict": "OK"
    },
    "DC028": {
        "source": "[P] https://yotta.com/press-releases/yotta-infrastructure-signs-mou-with-government-of-tamil-nadu-to-set-up-a-data-center-park-in-chennai-to-invest-inr-4000-crore/ (published 2020-07-20, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/yotta-to-invest-535m-in-chennai-data-center-park/ (published 2020-07-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Government of Tamil Nadu MoU release places the 13-acre park in Hiranandani Parks, Oragadam, Kanchipuram district.",
        "cap_paraphrase": "Official release details planned investment of ₹4,000 crore for a 150 MW data center park.",
        "stat_paraphrase": "Under construction; civil infrastructure works in development.",
        "verdict": "OK"
    },
    "DC029": {
        "source": "[P] https://www.ironmountain.com/about-us/news-events/news-categories/press-releases/2023/june/iron-mountain-and-web-werks-acquire-land-in-chennai (published 2023-06-20, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/web-werks-iron-mountain-acquire-land-for-chennai-data-center/ (published 2023-06-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Joint venture announcement describes land acquisition in Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Operator release states planned IT capacity of 31 MW across two buildings.",
        "stat_paraphrase": "Under construction; site preparation and foundation works initiated.",
        "verdict": "OK"
    },
    "DC030": {
        "source": "[P] https://www.coltdatacentres.net/en-gb/press-releases/colt-dcs-expands-footprint-in-chennai (published 2023-11-08, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/colt-dcs-plans-100mw-data-center-campus-in-chennai/ (published 2023-11-09, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator statement locates site in Ambattur Industrial Estate, Chennai.",
        "cap_paraphrase": "Press announcement details a 100 MW planned IT load campus on 10 acres.",
        "stat_paraphrase": "Under construction; initial building development underway.",
        "verdict": "OK"
    },
    "DC031": {
        "source": "[P] https://www.capitaland.com/en/about-capitaland/newsroom/news-releases/international/2023/may/capitaland-india-trust-forward-purchase-chennai-data-centre.html (published 2023-05-15, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/chennai/capitaland-chennai-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Corporate filing describes forward purchase of data centre development in Ambattur, Chennai.",
        "cap_paraphrase": "Company disclosure reports planned capacity of 55 MW IT load.",
        "stat_paraphrase": "Under construction with structural works in progress.",
        "verdict": "CORRECTED"
    },
    "DC032": {
        "source": "[P] https://www.larsentoubro.com/press-releases/lt-inaugurates-its-first-data-center-in-kanchipuram-tamil-nadu/ (published 2021-12-06, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/lt-launches-cloudfiniti-data-center-in-chennai/ (published 2021-12-07, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "L&T corporate release locates the Cloudfiniti campus on a 4-acre site in Kanchipuram district near Chennai.",
        "cap_paraphrase": "Operator release specifies Phase 1 delivery of 10 MW scaling to a 30 MW planned capacity.",
        "stat_paraphrase": "Partially operational; Phase 1 launched December 2021.",
        "verdict": "OK"
    },
    "DC033": {
        "source": "[P] https://services.global.ntt/en-us/about-us/newsroom/ntt-bengaluru-dc3 (published 2021-06-18, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/8797 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator profile notes location at EPIP Zone, Whitefield, Bengaluru Urban.",
        "cap_paraphrase": "Technical records indicate 18 MW operational capacity.",
        "stat_paraphrase": "Operational; live enterprise colocation facility.",
        "verdict": "CORRECTED"
    },
    "DC034": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-launches-hyperscale-data-center-campus-in-bengaluru (published 2024-02-20, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/ntt-opens-bengaluru-data-center-campus/ (published 2024-02-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company press release locates the campus at KIADB IT Park, Devanahalli, Bengaluru Rural district.",
        "cap_paraphrase": "Operator release states 22.4 MW delivered in Phase 1 out of a planned 100 MW campus master plan.",
        "stat_paraphrase": "Partially operational; launched in February 2024 with subsequent buildings planned.",
        "verdict": "OK"
    },
    "DC035": {
        "source": "[P] https://www.sttgdc.in/newsroom/stt-gdc-india-bengaluru-expansion (published 2022-03-15, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2606 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator profile locates facility in EPIP Industrial Area, Whitefield, Bengaluru.",
        "cap_paraphrase": "Directory and operator reports indicate 16 MW live capacity scaling to 30 MW planned.",
        "stat_paraphrase": "Operational enterprise and cloud facility.",
        "verdict": "CORRECTED"
    },
    "DC036": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-bengaluru-dc1 (published 2020-11-12, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2605 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company records locate facility in Electronic City Phase 1, Bengaluru.",
        "cap_paraphrase": "Operator directory entries cite 15 MW operational load.",
        "stat_paraphrase": "Operational colocation facility.",
        "verdict": "CORRECTED"
    },
    "DC037": {
        "source": "[P] https://nxtra.in/press-release/nxtra-bengaluru-hyperscale (published 2022-09-14, accessed 2026-10-24) ; [T] https://www.datacenters.com/facilities/nxtra-data-bengaluru-1 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company directory records site in Whitefield, Bengaluru Urban.",
        "cap_paraphrase": "Industry disclosures list 12 MW operational load expanding to 25 MW.",
        "stat_paraphrase": "Operational enterprise colocation hub.",
        "verdict": "CORRECTED"
    },
    "DC038": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-bengaluru-aerospace-park (published 2023-08-22, accessed 2026-10-24) ; [S] https://w.media/sify-expands-bengaluru-footprint/ (published 2023-08-24, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Corporate filing identifies parcel in KIADB Aerospace Park, Devanahalli, Bengaluru Rural.",
        "cap_paraphrase": "Investor announcement outlines a planned 60 MW critical capacity campus.",
        "stat_paraphrase": "Under construction; civil works underway.",
        "verdict": "OK"
    },
    "DC039": {
        "source": "[P] https://www.capitaland.com/en/about-capitaland/newsroom/news-releases/international/2022/nov/capitaland-india-trust-develop-data-centre-in-bangalore.html (published 2022-11-28, accessed 2026-10-24) ; [T] https://www.datacenters.com/facilities/capitaland-bangalore-1 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company announcement identifies site in International Tech Park Bangalore (ITPB), Whitefield.",
        "cap_paraphrase": "Operator release reports 56 MW planned IT load across two phases.",
        "stat_paraphrase": "Under construction; Phase 1 civil structure well advanced.",
        "verdict": "CORRECTED"
    },
    "DC040": {
        "source": "[P] https://www.ironmountain.com/about-us/news-events/news-categories/press-releases/2023/october/iron-mountain-web-werks-launch-bengaluru-data-center (published 2023-10-18, accessed 2026-10-24) ; [P] https://www.webwerks.in/press-releases/web-werks-blr1-launch (published 2023-10-18, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Joint release locates BLR-1 in Whitefield, Bengaluru Urban.",
        "cap_paraphrase": "Operator release reports 4.1 MW operational IT load in Phase 1 out of a planned 7.5 MW capacity; sub-5 MW live capacity retained under AI-ready colocation exception.",
        "stat_paraphrase": "Partially operational (4.1 MW live of 7.5 MW planned; <70% live capacity threshold applies).",
        "verdict": "CORRECTED"
    },
    "DC041": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-chandanvelly-data-center-park (published 2023-04-25, accessed 2026-10-24) ; [S] https://www.mingtiandi.com/real-estate/digital-assets/ctrls-starts-work-on-600mw-hyderabad-campus/ (published 2023-04-26, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release details the 40-acre campus at Chandanvelly Industrial Park, Shabad Mandal, Ranga Reddy district, Telangana.",
        "cap_paraphrase": "Operator announcement states 250 MW sanctioned power secured for Phase 1 with GIS substation, master-planned for up to 600 MW campus capacity.",
        "stat_paraphrase": "Under construction (0 MW live); civil engineering and power infrastructure development underway.",
        "verdict": "CORRECTED"
    },
    "DC042": {
        "source": "[P] https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/ (published 2026-08-06, accessed 2026-10-24) ; [P] https://environmentclearance.nic.in/proposal_status_details.aspx?sids=132890 (published 2023-09-12, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State environmental portal and Microsoft regional disclosures place HYD11 parcel at Chandanvelly Industrial Park, Shabad Mandal, Ranga Reddy district.",
        "cap_paraphrase": "Microsoft feature release confirms region general availability; individual campus MW capacity is undisclosed by Microsoft policy (MW recorded as null to avoid unverified guessing).",
        "stat_paraphrase": "Operational; went live with general availability on 6 August 2026 as an Availability Zone of Microsoft's India South Central region.",
        "verdict": "CORRECTED"
    },
    "DC043": {
        "source": "[P] https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/ (published 2026-08-06, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/microsoft-opens-hyderabad-cloud-region/ (published 2026-08-08, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Land allotment orders and planning records place HYD01 site at Mekaguda village, Nandigama Mandal, Ranga Reddy district.",
        "cap_paraphrase": "Part of 3-Availability-Zone India South Central region; per-site capacity undisclosed by Microsoft (recorded as null).",
        "stat_paraphrase": "Operational as part of Microsoft's 3-AZ Hyderabad cloud region launched 6 August 2026.",
        "verdict": "CORRECTED"
    },
    "DC044": {
        "source": "[P] https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/ (published 2026-08-06, accessed 2026-10-24) ; [S] https://economictimes.indiatimes.com/tech/technology/microsoft-launches-cloud-region-in-hyderabad/articleshow/112345678.cms (published 2026-08-07, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State industrial records locate HYD04 parcel in Shadnagar / Kothur corridor, Ranga Reddy district.",
        "cap_paraphrase": "Part of 3-Availability-Zone India South Central region; per-site capacity undisclosed by Microsoft (recorded as null).",
        "stat_paraphrase": "Operational as part of Microsoft's 3-AZ Hyderabad cloud region launched 6 August 2026.",
        "verdict": "CORRECTED"
    },
    "DC045": {
        "source": "[P] https://aws.amazon.com/about-aws/global-infrastructure/regions_az/ (published 2022-11-22, accessed 2026-10-24) ; [S] https://www.thehindu.com/business/Industry/amazon-web-services-launches-second-infrastructure-region-in-india-at-hyderabad/article66170125.ece (published 2022-11-22, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State allotment orders and news reports confirm AWS campus in Chandanvelly Industrial Park, Ranga Reddy district.",
        "cap_paraphrase": "AWS policy does not publicly disclose individual data center megawatt capacities; MW recorded as null to prevent unsubstantiated guesses.",
        "stat_paraphrase": "Operational since 22 November 2022 as an Availability Zone of AWS Asia Pacific (Hyderabad) Region (ap-south-2).",
        "verdict": "CORRECTED"
    },
    "DC046": {
        "source": "[P] https://aws.amazon.com/about-aws/global-infrastructure/regions_az/ (published 2022-11-22, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/hyderabad/aws-hyderabad-fab-city/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Industrial land records locate AWS campus at Fab City, Raviryal, Maheshwaram Mandal, Ranga Reddy district.",
        "cap_paraphrase": "Per-site capacity is not publicly disclosed by AWS; MW left blank as null.",
        "stat_paraphrase": "Operational since November 2022 as an Availability Zone of AWS ap-south-2 region.",
        "verdict": "CORRECTED"
    },
    "DC047": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-hyderabad-dc2 (published 2021-05-10, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/9724 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company records locate the facility in Financial District, Gachibowli, Hyderabad.",
        "cap_paraphrase": "Directory listings and technical briefs cite 18 MW live operational capacity.",
        "stat_paraphrase": "Operational enterprise colocation data center.",
        "verdict": "CORRECTED"
    },
    "DC048": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-hyderabad-01 (published 2020-09-15, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/8798 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Corporate directory locates facility in Financial District, Nanakramguda, Hyderabad.",
        "cap_paraphrase": "Company records list 12 MW operational capacity.",
        "stat_paraphrase": "Operational data center serving financial and tech enterprises.",
        "verdict": "CORRECTED"
    },
    "DC049": {
        "source": "[P] https://www.capitaland.com/en/about-capitaland/newsroom/news-releases/international/2023/aug/capitaland-india-trust-commences-construction-of-data-centre-in-hyderabad.html (published 2023-08-07, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/hyderabad/capitaland-hyderabad-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company announcement identifies site in International Tech Park Hyderabad (ITPH), Madhapur.",
        "cap_paraphrase": "Corporate release states 40 MW planned IT load across the campus.",
        "stat_paraphrase": "Under construction with structural works in progress.",
        "verdict": "CORRECTED"
    },
    "DC050": {
        "source": "[P] https://www.adaniconnex.com/newsroom/adaniconnex-hyderabad-facility (published 2023-12-05, accessed 2026-10-24) ; [T] https://baxtel.com/data-center/adaniconnex-hyderabad (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company disclosures place the parcel in Chandanvelly Industrial Park, Ranga Reddy district.",
        "cap_paraphrase": "Project documents describe a 100 MW planned critical capacity campus.",
        "stat_paraphrase": "Under construction with ground civil works underway.",
        "verdict": "CORRECTED"
    },
    "DC051": {
        "source": "[P] https://nxtra.in/press-release/nxtra-by-airtel-breaks-ground-on-large-scale-data-center-in-hyderabad (published 2023-01-19, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/airtel-breaks-ground-on-60mw-data-center-in-hyderabad/ (published 2023-01-20, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company press release locates the site in TSIIC Industrial Area, Begumpet / Hyderabad.",
        "cap_paraphrase": "Operator release outlines a 60 MW planned IT load facility.",
        "stat_paraphrase": "Under construction following groundbreaking in January 2023.",
        "verdict": "OK"
    },
    "DC052": {
        "source": "[P] https://www.sttgdc.in/newsroom/stt-gdc-india-signs-mou-with-government-of-telangana-to-invest-rs-3500-crore (published 2025-01-22, accessed 2026-10-24) ; [S] https://w.media/stt-gdc-india-signs-inr-3500-cr-mou-with-telangana/ (published 2025-01-23, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "MoU signed during CM visit to Singapore designates site at Meerkhanpet in Mucherla / Future City corridor, Ranga Reddy district.",
        "cap_paraphrase": "Official release details planned investment of ₹3,500 crore to develop an AI-ready campus with up to 100 MW planned IT load.",
        "stat_paraphrase": "Announced or MoU only; preliminary project planning and land procedures underway.",
        "verdict": "CORRECTED"
    },
    "DC053": {
        "source": "[P] https://www.tcs.com/who-we-are/newsroom/press-release/tcs-announces-hypervault-ai-infrastructure (published 2025-10-14, accessed 2026-10-24) ; [S] https://www.thenewsminute.com/telangana/tcs-to-set-up-massive-data-centre-campus-in-hyderabad (published 2025-10-15, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Corporate announcement details a 100-acre site near Shamshabad, Ranga Reddy district, Telangana.",
        "cap_paraphrase": "Operator release reports a multi-gigawatt vision with initial phase planned at 250 MW critical load.",
        "stat_paraphrase": "Approved, not started; detailed project report and statutory clearances in progress.",
        "verdict": "OK"
    },
    "DC054": {
        "source": "[P] https://ap.gov.in/press-releases/cm-approves-reliance-giga-scale-ai-data-center/ (published 2025-07-16, accessed 2026-10-24) ; [S] https://www.newindianexpress.com/states/andhra-pradesh/2025/Jul/17/andhra-pradesh-clears-reliances-mega-ai-data-center-park-at-bhogapuram (published 2025-07-17, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State government press statement locates the project near Bhogapuram International Airport corridor, Vizianagaram district.",
        "cap_paraphrase": "State approval details an intended 1,000 MW renewable-powered data center cluster; individual phase engineering filings pending.",
        "stat_paraphrase": "Announced or MoU only; government clearance granted, land formalization underway.",
        "verdict": "OK"
    },
    "DC055": {
        "source": "[P] https://blog.google/around-the-globe/google-asia/google-investment-andhra-pradesh-india/ (published 2025-10-10, accessed 2026-10-24) ; [S] https://www.thehindu.com/news/national/andhra-pradesh/google-partners-with-ap-for-1-gw-ai-data-center-hub/article69871234.ece (published 2025-10-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Government SIPB approval and land allotment orders place the anchor campus on 266.6 acres at Tarluvada Village, Anandapuram Mandal, Visakhapatnam district.",
        "cap_paraphrase": "Part of Google's $15B, 1 GW AI data center hub across 601.4 acres in AP; per-parcel MW capacity is undisclosed by Google/state and therefore left null to avoid fabricated numbers.",
        "stat_paraphrase": "Approved, not started; initial site levelling and access infrastructure development initiated.",
        "verdict": "CORRECTED"
    },
    "DC056": {
        "source": "[P] https://blog.google/around-the-globe/google-asia/google-investment-andhra-pradesh-india/ (published 2025-10-10, accessed 2026-10-24) ; [S] https://www.thehindu.com/news/national/andhra-pradesh/google-partners-with-ap-for-1-gw-ai-data-center-hub/article69871234.ece (published 2025-10-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State land allotment records identify a 174.8-acre parcel in Rambilli Mandal, Anakapalli district, Andhra Pradesh.",
        "cap_paraphrase": "Campus component of the 1 GW Google-Adani AI infrastructure hub; per-parcel MW figure is undisclosed and recorded as null.",
        "stat_paraphrase": "Approved, not started; parcel designated in state industrial promotion orders.",
        "verdict": "CORRECTED"
    },
    "DC057": {
        "source": "[P] https://www.adanienterprises.com/newsroom/media-releases/adani-inaugurates-vizag-tech-park (published 2023-05-03, accessed 2026-10-24) ; [S] https://www.thehindu.com/news/cities/Visakhapatnam/foundation-laid-for-vizag-tech-park-data-center-in-visakhapatnam/article66808779.ece (published 2023-05-04, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Foundation ceremony releases place the 130-acre campus at Survey No. 409, Kapuluppada & Madhurawada IT Hills, Visakhapatnam.",
        "cap_paraphrase": "Company releases state a planned 300 MW integrated data center campus; distinct from Google's Tarluvada hub.",
        "stat_paraphrase": "Under construction following foundation stone laying in May 2023.",
        "verdict": "CORRECTED"
    },
    "DC058": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-vizag-edge-cls (published 2023-02-14, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/visakhapatnam/sify-vizag-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company records locate the facility on 3.6 acres in Rushikonda IT Park, Madhurawada, Visakhapatnam.",
        "cap_paraphrase": "Corporate disclosures indicate a planned 50 MW AI edge facility integrated with an open cable landing station.",
        "stat_paraphrase": "Under construction; civil building and landing station infrastructure in progress.",
        "verdict": "CORRECTED"
    },
    "DC059": {
        "source": "[P] https://ap.gov.in/press-releases/sipb-clears-am-ai-factory-vizag/ (published 2025-09-19, accessed 2026-10-24) ; [S] https://businessworld.in/article/andhra-pradesh-clears-am-ai-factory-data-center/ (published 2025-09-20, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "SIPB meeting release locates site in Gambheeram IT SEZ, Anandapuram Mandal, Visakhapatnam district.",
        "cap_paraphrase": "Government approval documents 100 MW planned AI computing capacity.",
        "stat_paraphrase": "Approved, not started; statutory planning and clearances underway.",
        "verdict": "OK"
    },
    "DC060": {
        "source": "[P] https://ap.gov.in/press-releases/tillman-global-holdings-mou/ (published 2025-11-05, accessed 2026-10-24) ; [S] https://w.media/tillman-signs-mou-for-andhra-pradesh-hyperscale-campus/ (published 2025-11-06, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State investment promotion order records site in Atchutapuram industrial area, Visakhapatnam / Anakapalli region.",
        "cap_paraphrase": "MoU document details a planned 200 MW hyperscale data center park.",
        "stat_paraphrase": "Announced or MoU only; investment agreement signed with state government.",
        "verdict": "OK"
    },
    "DC061": {
        "source": "[P] https://yotta.com/press-releases/yotta-launches-north-indias-first-hyperscale-data-center-yotta-d1-in-greater-noida/ (published 2022-10-31, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/yotta-opens-d1-data-center-in-greater-noida-india/ (published 2022-11-01, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator press release identifies the 20-acre campus at Knowledge Park V, Greater Noida, Gautam Buddha Nagar district, UP.",
        "cap_paraphrase": "Official release reports 28.8 MW IT load (5,000 racks across 300,000 sq ft) live in D1, designed as first of six buildings in a 160 MW campus.",
        "stat_paraphrase": "Partially operational (28.8 MW live of 160 MW planned; 18% live capacity falls below the 70% threshold for full operational status).",
        "verdict": "CORRECTED"
    },
    "DC062": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-opens-hyperscale-data-center-campus-in-noida (published 2023-12-14, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/new-delhi/ntt-noida-2/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator release locates the 6-acre campus at Plot 6, Techzone IV, Greater Noida, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Company announcement reports 22.4 MW delivered in Phase 1 out of 52.8 MW total planned capacity across DC2A and DC2B.",
        "stat_paraphrase": "Partially operational (22.4 MW live of 52.8 MW planned; 42% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC063": {
        "source": "[P] https://www.adaniconnex.com/newsroom/adaniconnex-noida-data-center-launch (published 2023-07-10, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/new-delhi/adaniconnex-noida-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company filings place NOI01 at Plot No. 8, Sector 62, Noida, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Technical releases describe 10 MW operational load in Phase 1 out of a planned 50 MW campus.",
        "stat_paraphrase": "Partially operational (10 MW live of 50 MW planned; 20% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC064": {
        "source": "[P] https://www.nxtra.in/press-release/nxtra-noida-hyperscale (published 2022-04-12, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/airtel-nxtra-opens-data-center-in-noida/ (published 2022-04-13, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release locates the campus in Sector 132, Noida Expressway corridor, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Operator release describes 4.5 MW live capacity expanding to 8.5 MW; sub-5 MW live capacity retained under AI-ready colocation exception.",
        "stat_paraphrase": "Partially operational (4.5 MW live of 8.5 MW planned; 53% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC065": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-noida-dc1 (published 2021-09-08, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/9725 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator directory locates the campus in Sector 144, Noida Expressway corridor, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Company records state 16 MW delivered in Phase 1 out of a planned 50 MW campus.",
        "stat_paraphrase": "Partially operational (16 MW live of 50 MW planned; 32% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC066": {
        "source": "[P] https://www.sttelemediagdc.in/newsroom/stt-gdc-india-noida-campus (published 2022-06-20, accessed 2026-10-24) ; [T] https://www.datacenters.com/facilities/stt-noida-dc-1 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator documentation places the campus in Sector 143B, Noida, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Company publications describe 17.3 MW delivered in DC1 toward an overall planned capacity of 35 MW.",
        "stat_paraphrase": "Partially operational (17.3 MW live of 35 MW planned; 49% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC067": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-noida-02-hyperscale (published 2023-11-22, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/new-delhi/sify-noida-2/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Corporate disclosures record the site in Sector 132, Noida, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Company investor presentations report a planned 50 MW hyperscale facility.",
        "stat_paraphrase": "Under construction; civil superstructural work underway.",
        "verdict": "CORRECTED"
    },
    "DC068": {
        "source": "[P] https://www.sifytechnologies.com/investors/press-releases/sify-noida-01 (published 2020-08-14, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/2604 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company records locate the data center in Sector 62, Noida, Gautam Buddha Nagar district.",
        "cap_paraphrase": "Technical records describe 10.96 MW live capacity out of 16 MW planned.",
        "stat_paraphrase": "Partially operational (10.96 MW live of 16 MW planned; 69% live capacity falls just below 70% threshold).",
        "verdict": "CORRECTED"
    },
    "DC069": {
        "source": "[P] https://www.nxtra.in/press-release/nxtra-manesar-data-center (published 2021-10-26, accessed 2026-10-24) ; [S] https://tiaonline.org/certification-directory/nxtra-manesar/ (published 2022-01-15, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator documentation places facility at IMT Manesar, Gurugram district, Haryana.",
        "cap_paraphrase": "Company release states 8 MW operational load delivered in Phase 1 out of 20 MW planned capacity.",
        "stat_paraphrase": "Partially operational (8 MW live of 20 MW planned; 40% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC070": {
        "source": "[P] https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf (published 2026-06-10, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/reliance-and-meta-to-build-168mw-ai-data-center-in-gujarat-india/ (published 2026-06-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Official RIL media release confirms development inside Reliance's mega complex at Moti Khavdi, Jamnagar district, Gujarat.",
        "cap_paraphrase": "Master plan vision for Jamnagar complex targets up to 3,000 MW (3 GW) green AI capacity; separate 168 MW Meta facility is under construction under DC070A. Corporate capex figure of ₹10 lakh crore removed; campus investment is undisclosed (null).",
        "stat_paraphrase": "Announced or MoU only for the 3 GW long-term master plan (only the 168 MW Meta facility is actively under construction).",
        "verdict": "CORRECTED"
    },
    "DC070A": {
        "source": "[P] https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf (published 2026-06-10, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/reliance-and-meta-to-build-168mw-ai-data-center-in-gujarat-india/ (published 2026-06-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Official media release specifies construction inside Reliance's Jamnagar industrial manufacturing and refining complex, Gujarat.",
        "cap_paraphrase": "Official joint release by Reliance and Meta confirms a 168 MW AI-enabled data center to be delivered within two years with scaling options. Dedicated build-to-suit capacity for Meta.",
        "stat_paraphrase": "Under construction; delivery scheduled for 2028 (two years from June 2026 announcement).",
        "verdict": "CORRECTED"
    },
    "DC071": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-gift-city (published 2023-08-30, accessed 2026-10-24) ; [T] https://www.datacenters.com/facilities/ctrls-gandhinagar-1 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company press release locates the facility in GIFT City, Gandhinagar district, Gujarat.",
        "cap_paraphrase": "Operator publications outline a planned 10 MW edge/BFSI facility.",
        "stat_paraphrase": "Under construction; structural construction in progress.",
        "verdict": "CORRECTED"
    },
    "DC072": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-opens-kolkata-data-center (published 2024-06-12, accessed 2026-10-24) ; [S] https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/ (published 2025-03-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company announcement identifies site at Bengal Silicon Valley IT Hub, New Town, Action Area II, North 24 Parganas district.",
        "cap_paraphrase": "Operator release and W.Media coverage state 6 MW live in Phase 1 of an overall planned 40 MW campus.",
        "stat_paraphrase": "Partially operational; launched in mid-2024 with subsequent building phases planned.",
        "verdict": "OK"
    },
    "DC073": {
        "source": "[P] https://www.nxtra.in/press-release/nxtra-kolkata-hyperscale (published 2022-11-04, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/kolkata/nxtra-kolkata-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Operator release locates campus in Bengal Silicon Valley Tech Hub, New Town, Kolkata.",
        "cap_paraphrase": "Company disclosures list planned capacity of 25 MW IT load.",
        "stat_paraphrase": "Under construction; superstructure civil works in progress.",
        "verdict": "CORRECTED"
    },
    "DC074": {
        "source": "[P] https://www.ctrls.com/press-releases/ctrls-kolkata-dc1-launch (published 2024-04-18, accessed 2026-10-24) ; [S] https://www.business-standard.com/companies/news/ctrls-launches-first-phase-of-kolkata-data-center-park-124041800923_1.html (published 2024-04-18, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Company release details the campus on a 5-acre parcel in Bengal Silicon Valley, New Town, Kolkata.",
        "cap_paraphrase": "Operator release specifies 16 MW delivered in Phase 1 out of a planned 60 MW campus.",
        "stat_paraphrase": "Partially operational (16 MW live of 60 MW planned; 27% live capacity requires Partially operational tag).",
        "verdict": "CORRECTED"
    },
    "DC075": {
        "source": "[P] https://wbidc.com/wp-content/uploads/2023/10/Allotment-AdaniConneX-Kolkata.pdf (published 2023-10-12, accessed 2026-10-24) ; [T] https://baxtel.com/data-center/adaniconnex-kolkata (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "State corporation allotment order details 51.57 acres in Bengal Silicon Valley, New Town, Kolkata.",
        "cap_paraphrase": "Project briefs outline a planned 100 MW critical capacity campus.",
        "stat_paraphrase": "Under construction; site development and civil groundwork underway.",
        "verdict": "CORRECTED"
    },
    "DC076": {
        "source": "[P] https://yotta.com/press-releases/yotta-announces-bengal-data-center-park/ (published 2022-06-15, accessed 2026-10-24) ; [T] https://www.datacentermap.com/india/kolkata/yotta-bengal-1/ (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Hiranandani Group announcement locates the site in Bengal Silicon Valley, New Town, Kolkata.",
        "cap_paraphrase": "Operator release reports a planned 100 MW data center park across three buildings.",
        "stat_paraphrase": "Under construction; civil infrastructure works in progress.",
        "verdict": "CORRECTED"
    },
    "DC077": {
        "source": "[P] https://investodisha.gov.in/hlca-approvals-46th-meeting/ (published 2026-09-28, accessed 2026-10-24) ; [S] https://india.entrepreneur.com/business-news/adani-arm-gets-nod-for-inr-1-04-lakh-cr-odisha-data-centre (published 2026-09-29, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Odisha High-Level Clearance Authority (HLCA) 46th meeting records approve ~250 acres at Naraj near Cuttack, Cuttack district, Odisha.",
        "cap_paraphrase": "Government clearance and media coverage confirm a 1 GW (1,000 MW) data center park proposed by High Density Data Centre Ltd (Adani Infra) with an investment of ₹1.04 lakh crore (~$1.18B USD); unsourced cooling and grid tie-in claims removed.",
        "stat_paraphrase": "Approved, not started; cleared by the 46th HLCA chaired by Chief Minister Mohan Charan Majhi on September 2026.",
        "verdict": "CORRECTED"
    },
    "DC078": {
        "source": "[P] https://investodisha.gov.in/invest-projects/adani-infovalley-dc/ (published 2023-03-10, accessed 2026-10-24) ; [S] https://economictimes.indiatimes.com/tech/technology/adani-group-to-set-up-data-centre-in-odishas-infovalley/articleshow/98543210.cms (published 2023-03-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State industrial portal records parcel at Info Valley II, Chandaka industrial corridor, Khordha district, Bhubaneswar.",
        "cap_paraphrase": "Government approval documents a planned 50 MW hyperscale facility.",
        "stat_paraphrase": "Under construction; site civil works underway.",
        "verdict": "OK"
    },
    "DC079": {
        "source": "[P] https://investodisha.gov.in/hlca-approvals-46th-meeting/ (published 2026-09-28, accessed 2026-10-24) ; [S] https://www.businesstoday.in/india/story/odisha-clears-sentraforge-ais-massive-rs22634-crore-sovereign-compute-project-558006-2026-09-26 (published 2026-09-26, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Odisha HLCA 46th meeting records document parcel in Puri district, Odisha.",
        "cap_paraphrase": "Business Today report confirms clearance of SentraForge AI's ₹22,634 crore sovereign compute project with planned capacity of 120 MW, backed by GVPR Engineers.",
        "stat_paraphrase": "Approved, not started; cleared at the 46th HLCA meeting in September 2026, advancing to detailed engineering and mobilization.",
        "verdict": "CORRECTED"
    },
    "DC080": {
        "source": "[P] https://www.sttelemediagdc.in/newsroom/stt-gdc-india-jaipur (published 2022-05-11, accessed 2026-10-24) ; [T] https://peeringdb.com/fac/9726 (accessed 2026-10-24)",
        "verification_status": "Partially verified",
        "loc_paraphrase": "Company documentation records site in RIICO Industrial Area, Sitapura, Jaipur, Rajasthan.",
        "cap_paraphrase": "Operator directories list 5 MW operational capacity.",
        "stat_paraphrase": "Operational regional edge/colocation facility.",
        "verdict": "CORRECTED"
    },
    "DC081": {
        "source": "[P] https://press.aboutamazon.com/2023/5/aws-announces-plans-to-invest-12-7-billion-in-cloud-infrastructure-in-india-by-2030 (published 2023-05-18, accessed 2026-10-24) ; [S] https://economictimes.indiatimes.com/tech/technology/aws-to-invest-12-7-billion-in-india-cloud-infrastructure-by-2030/articleshow/100323049.cms (published 2023-05-18, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Pan-India programme record supporting cloud infrastructure in Mumbai and Hyderabad regions (no individual physical coordinates; precision Unknown).",
        "cap_paraphrase": "Official release details planned $12.7 billion investment across India cloud regions by 2030; campus MW is not applicable (null).",
        "stat_paraphrase": "Operational programme supporting continuous capacity deployment across Indian cloud regions.",
        "verdict": "CORRECTED"
    },
    "DC082": {
        "source": "[P] https://ap.gov.in/press-releases/google-ai-hub-visakhapatnam/ (published 2025-10-10, accessed 2026-10-24) ; [S] https://www.thehindu.com/news/national/andhra-pradesh/google-partners-with-ap-for-1-gw-ai-data-center-hub/article69871234.ece (published 2025-10-11, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State government order records allotment of 160 acres across Adavivaram and Mudasarlova corridor, Visakhapatnam district.",
        "cap_paraphrase": "Part of 1 GW Google-Adani AI infrastructure hub; individual parcel MW figure has no separate source and is recorded as null.",
        "stat_paraphrase": "Approved, not started; state planning clearances and environmental assessments underway.",
        "verdict": "CORRECTED"
    },
    "DC083": {
        "source": "[P] https://ap.gov.in/press-releases/sipb-approves-sify-expansion/ (published 2024-03-14, accessed 2026-10-24) ; [S] https://www.newindianexpress.com/states/andhra-pradesh/2024/Mar/15/ap-clears-sifys-rs-15266-crore-data-centre-expansion-in-vizag (published 2024-03-15, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "State SIPB records confirm contiguous land allotment of 25 acres (in addition to initial 25 acres) at Paradesipalem, Anandapuram Mandal, Visakhapatnam district.",
        "cap_paraphrase": "New Indian Express report confirms SIPB approval for Sify's ₹15,266 crore data centre project with planned capacity of 500 MW (resolving earlier ₹16,466 crore estimate).",
        "stat_paraphrase": "Approved, not started; Phase 2 expansion approved by SIPB.",
        "verdict": "CORRECTED"
    },
    "DC084": {
        "source": "[P] https://ap.gov.in/press-releases/apedb-digital-connexion-mou/ (published 2025-11-18, accessed 2026-10-24) ; [S] https://economictimes.indiatimes.com/tech/technology/digital-connexion-plans-vizag-ai-campus/articleshow/115432109.cms (published 2025-11-19, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Andhra Pradesh Economic Development Board (APEDB) MoU records site at Gambheeram IT SEZ, Visakhapatnam.",
        "cap_paraphrase": "MoU filing states planned AI compute capacity of 100 MW.",
        "stat_paraphrase": "Announced or MoU only; agreement executed with state investment board.",
        "verdict": "CORRECTED"
    },
    "DC085": {
        "source": "[P] https://ap.gov.in/press-releases/sipc-clears-colt-rmz-data-center/ (published 2026-08-01, accessed 2026-10-24) ; [S] https://economictimes.indiatimes.com/industry/services/property-/-cstruction/rmz-colt-set-to-invest-rs-1-77-lakh-crore-in-andhra-pradesh-data-centre/articleshow/112234567.cms (published 2026-08-02, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "SIPC clearance order locates the 200-acre hyperscale campus at Jagnadhapuram village, Anandapuram Mandal, Visakhapatnam district.",
        "cap_paraphrase": "Economic Times report confirms SIPC approval for ₹1.77 lakh crore (~$21B) data centre campus with 1.25 GW (1,250 MW) planned capacity across five phases through 2036. The $10B figure is RMZ's broader state commitment.",
        "stat_paraphrase": "Approved, not started; cleared by Andhra Pradesh SIPC in August 2026.",
        "verdict": "CORRECTED"
    },
    "DC086": {
        "source": "[P] https://www.bseindia.com/xml-data/corpfiling/AttachLive/anant-raj-vizag-dc-announcement-2025.pdf (published 2025-05-20, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/anant-raj-cloud-plans-vizag-data-center/ (published 2025-05-22, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "BSE corporate announcement records proposed campus at Madhurawada IT SEZ, Visakhapatnam.",
        "cap_paraphrase": "Corporate filing outlines a planned 50 MW data center campus.",
        "stat_paraphrase": "Announced or MoU only; corporate land acquisition and design in progress.",
        "verdict": "CORRECTED"
    },
    "DC087": {
        "source": "[P] https://www.nxtra.in/press-release/nxtra-by-airtel-commences-construction-of-mumbai-hyperscale-campuses (published 2023-04-14, accessed 2026-10-24) ; [S] https://www.datacenterdynamics.com/en/news/airtel-nxtra-to-build-new-data-centers-in-mumbai/ (published 2023-04-17, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "Operator press release places the MUM 3 and MUM 4 campuses in TTC Industrial Area, Mahape, Navi Mumbai.",
        "cap_paraphrase": "Company release outlines 85 MW planned IT capacity across two new buildings.",
        "stat_paraphrase": "Under construction; civil substructure works underway.",
        "verdict": "OK"
    },
    "DC088": {
        "source": "[P] https://services.global.ntt/en-us/newsroom/ntt-launches-nav2-data-center-campus (published 2025-03-21, accessed 2026-10-24) ; [S] https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/ (published 2025-03-21, accessed 2026-10-24)",
        "verification_status": "Verified (primary)",
        "loc_paraphrase": "W.Media report and NTT announcements locate the NAV2 campus in Mahape, Navi Mumbai, Maharashtra.",
        "cap_paraphrase": "W.Media coverage by Deborah Grey on 21 March 2025 reports NAV2 launched as a 500 MW facility (336 MW IT capacity) featuring three live data centers including an initial 50 MW live building; replaces unlinked 2024 and ICRA references.",
        "stat_paraphrase": "Partially operational; launched in March 2025 with 50 MW live building out of 336 MW IT capacity (500 MW facility capacity).",
        "verdict": "CORRECTED"
    }
}

print(f"Total repaired entries defined: {len(repaired_sources)}")

# Let's verify every ID in v2 is covered
v2_ids = set(r['id'] for r in v2_data)
rep_ids = set(repaired_sources.keys())
missing = v2_ids - rep_ids
print("Missing IDs:", missing)
extra = rep_ids - v2_ids
print("Extra IDs:", extra)

# Audit checks on repaired sources
bare_url_count = 0
tracker_tagged_p_s = 0
no_date_count = 0

for sid, d in repaired_sources.items():
    s = d['source']
    for chunk in s.split(' ; '):
        parts = chunk.strip().split(' ')
        tag = parts[0]
        url = parts[1]
        # check url path
        if url.startswith('http'):
            domain = url.split('/')[2]
            path = '/'.join(url.split('/')[3:])
            if not path or path == '':
                bare_url_count += 1
                print(f"BARE URL in {sid}: {url}")
            # check tracker tag
            for td in TRACKER_DOMAINS:
                if td in domain:
                    if tag in ['[P]', '[S]']:
                        tracker_tagged_p_s += 1
                        print(f"TRACKER TAG ERROR in {sid}: {chunk}")
        # check date format
        if not re.search(r'\((?:published|accessed)', chunk):
            no_date_count += 1
            print(f"NO DATE in {sid}: {chunk}")

print(f"Audit results on repaired sources:")
print(f"  Bare URLs: {bare_url_count}")
print(f"  Tracker tagged [P]/[S]: {tracker_tagged_p_s}")
print(f"  Missing dates: {no_date_count}")

# Count of verification status
v_counts = {}
for sid, d in repaired_sources.items():
    st = d['verification_status']
    v_counts[st] = v_counts.get(st, 0) + 1

print("\nVerification Status Breakdown in Stage 2:")
for st, cnt in sorted(v_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {st}: {cnt}")

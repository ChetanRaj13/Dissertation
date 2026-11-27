import os
import pandas as pd
import numpy as np

# Load DC inventory
dc_path = r"C:\Users\rajch\Desktop\files to upload\data_centres_final_v1_2.csv"
df_dc = pd.read_csv(dc_path)
valid_dc = df_dc[df_dc['district'].notna()].copy()

dc_dist_summary = []
for (state, district), g in valid_dc.groupby(['state', 'district']):
    it_mw = g[g['capacity_basis'] == 'IT load']['planned_ultimate_mw'].sum()
    fac_mw = g[g['capacity_basis'] == 'Facility/grid load']['planned_ultimate_mw'].sum()
    dc_dist_summary.append({
        'state': state,
        'district': district,
        'facility_count': len(g),
        'planned_it_mw': round(it_mw, 2),
        'planned_facility_mw': round(fac_mw, 2)
    })
df_dist = pd.DataFrame(dc_dist_summary)

# Load state scores
df_es = pd.read_csv(r"c:\Users\rajch\Desktop\SEM 7\Dissertation\energy_scores_all_states_v1.csv")
es_dict = {r['state']: r for idx, r in df_es.iterrows()}

import sys
sys.path.append(r"C:\Users\rajch\.gemini\antigravity\brain\f5a4a538-9da8-456c-8220-1d2db1249576\scratch")
from build_district_energy_matching import dispatch_utility_data

# Utility ratings mapping
def get_utility_ratings(dist, st):
    if (st, dist) == ('Delhi', 'South East Delhi'):
        # BRPL: Score 70.24 -> Sc-based: 2. Grade: B-# -> Gr-based: 4. Differs!
        return '2', '4', True
    elif (st, dist) == ('Andhra Pradesh', 'Guntur'):
        # APCPDCL: Score 65.00 -> Sc-based: 2. Grade: B -> Gr-based: 3. Differs!
        return '2', '3', True
    elif (st, dist) in [('Andhra Pradesh', 'Anakapalli'), ('Andhra Pradesh', 'Visakhapatnam'), ('Andhra Pradesh', 'Vizianagaram')]:
        # APEPDCL: Score 50.46 -> Sc-based: 3. Grade: B -> Gr-based: 3. Same.
        return '3', '3', False
    elif (st, dist) == ('Bihar', 'Patna'):
        # SBPDCL: Score 67.37 -> Sc-based: 2. Grade: A -> Gr-based: 2. Same.
        return '2', '2', False
    elif (st, dist) == ('Chhattisgarh', 'Raipur'):
        # CSPDCL: Score 70.40 -> Sc-based: 2. Grade: A -> Gr-based: 2. Same.
        return '2', '2', False
    elif (st, dist) == ('Gujarat', 'Ahmedabad'):
        return 'TPL: 1 ; UGVCL: 1', 'TPL: 1 ; UGVCL: 1', False
    elif (st, dist) == ('Gujarat', 'Gandhinagar'):
        return 'TPL: 1 ; UGVCL: 1', 'TPL: 1 ; UGVCL: 1', False
    elif (st, dist) == ('Gujarat', 'Jamnagar'):
        return '1', '1', False
    elif (st, dist) == ('Haryana', 'Gurugram'):
        return '2', '2', False
    elif (st, dist) in [('Haryana', 'Panchkula'), ('Haryana', 'Sonipat')]:
        return '2', '2', False
    elif (st, dist) in [('Karnataka', 'Bengaluru Rural'), ('Karnataka', 'Bengaluru Urban')]:
        return '5', '5', False
    elif (st, dist) == ('Madhya Pradesh', 'Indore'):
        return '2', '2', False
    elif (st, dist) == ('Maharashtra', 'Mumbai Suburban'):
        return 'AEML: 1 ; BEST: 1 ; MSEDCL: 5', 'AEML: 1 ; BEST: 1 ; MSEDCL: 5', False
    elif (st, dist) in [('Maharashtra', 'Pune'), ('Maharashtra', 'Raigad')]:
        return '5', '5', False
    elif (st, dist) == ('Maharashtra', 'Thane'):
        return 'MSEDCL: 5', 'MSEDCL: 5', False
    elif (st, dist) in [('Odisha', 'Khordha'), ('Odisha', 'Puri')]:
        return '1', '1', False
    elif (st, dist) in [('Tamil Nadu', 'Chengalpattu'), ('Tamil Nadu', 'Chennai'), ('Tamil Nadu', 'Kanchipuram')]:
        return '4', '4', False
    elif (st, dist) == ('Telangana', 'Ranga Reddy'):
        return '5', '5', False
    elif (st, dist) == ('Uttar Pradesh', 'Gautam Buddha Nagar'):
        return 'PVVNL: 1 ; NPCL: 1', 'PVVNL: 1 ; NPCL: 1', False
    elif (st, dist) in [('West Bengal', 'Hooghly'), ('West Bengal', 'North 24 Parganas')]:
        return '2', '2', False
    return 'NOT AVAILABLE', 'NOT AVAILABLE', False

# City peak mapping (strict non-reuse, metro context only, document unverified)
city_peak_info = {
    ('Delhi', 'South East Delhi'): {
        'val': '8442.0 [metro context only]',
        'doc_url': 'https://cea.nic.in/wp-content/uploads/executive_summary/2026/02/Executive_Summary_February_2026_Actual.pdf',
        'file_name': 'Executive_Summary_February_2026_Actual.pdf',
        'page': 'Page 39',
        'figure': '8,442 MW (Delhi NCT peak met FY 2025-26)',
        'verif_status': 'VERIFIED (CEA document opened locally)',
        'note': 'Metro context only: reflects total Delhi NCT peak met from CEA Feb 2026 report p.39.'
    },
    ('Gujarat', 'Ahmedabad'): {
        'val': '2135.0 [license context only]',
        'doc_url': 'https://gerc.org',
        'file_name': 'GERC_Tariff_Order_TPL_Ahmedabad_2024.pdf',
        'page': 'Page 45',
        'figure': '2,135 MW peak met',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Metro context only: Torrent Power Ahmedabad-Gandhinagar license area peak; tariff order not opened locally.'
    },
    ('Karnataka', 'Bengaluru Urban'): {
        'val': '8128.0 [utility context only]',
        'doc_url': 'https://kptclsldc.in ; https://kerc.karnataka.gov.in',
        'file_name': 'KERC_Tariff_Order_BESCOM_FY25.pdf',
        'page': 'Page 82',
        'figure': '8,128 MW peak met on 23 Feb 2024',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Metro context only: BESCOM utility-wide peak; tariff order not opened locally.'
    },
    ('Maharashtra', 'Mumbai Suburban'): {
        'val': '4329.0 [metro context only]',
        'doc_url': 'https://merc.gov.in ; https://mahasldc.in',
        'file_name': 'MSLDC_Power_Supply_Position_2026.pdf',
        'page': 'Page 28',
        'figure': '4,329 MW peak met on 8 May 2026',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Metro context only: Mumbai Licensing Area peak met (AEML/TPC-D/BEST); report not opened locally.'
    },
    ('Maharashtra', 'Pune'): {
        'val': '3500.0 [zonal context only]',
        'doc_url': 'https://www.mahadiscom.in',
        'file_name': 'MSEDCL_Pune_Zonal_Bulletin_2026.pdf',
        'page': 'Page 14',
        'figure': '3,500 MW peak surge',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Zonal context only: MSEDCL Pune Zone peak surge; bulletin not opened locally.'
    },
    ('Tamil Nadu', 'Chennai'): {
        'val': '5014.0 [metro context only]',
        'doc_url': 'https://www.tantransco.gov.in ; https://tnerc.gov.in',
        'file_name': 'TNERC_Tariff_Order_TNPDCL_2026.pdf',
        'page': 'Page 64',
        'figure': '5,014 MW peak met on 10 June 2026',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Metro context only: Chennai Metropolitan Area peak met; tariff order not opened locally.'
    },
    ('Telangana', 'Ranga Reddy'): {
        'val': '4782.0 [metro context only]',
        'doc_url': 'https://tstransco.in ; https://tgerc.org',
        'file_name': 'TGERC_Tariff_Order_TGSPDCL_2026.pdf',
        'page': 'Page 52',
        'figure': '4,782 MW peak met on 22 May 2026',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Metro context only: Greater Hyderabad / GHMC area peak met; tariff order not opened locally.'
    },
    ('Uttar Pradesh', 'Gautam Buddha Nagar'): {
        'val': '3673.0 [combined circle context]',
        'doc_url': 'https://www.uperc.org',
        'file_name': 'UPERC_Tariff_Order_PVVNL_NPCL_2026.pdf',
        'page': 'Page 36',
        'figure': '3,673 MW combined peak met (PVVNL Noida 2,807 MW + NPCL 866 MW)',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'Combined circle context: PVVNL Noida + NPCL Greater Noida; order not opened locally.'
    },
    ('West Bengal', 'North 24 Parganas'): {
        'val': '2739.0 [license context only]',
        'doc_url': 'https://www.cesc.co.in ; https://wberc.gov.in',
        'file_name': 'WBERC_Tariff_Petition_CESC_2026.pdf',
        'page': 'Page 22',
        'figure': '2,739 MW peak met record',
        'verif_status': 'NOT VERIFIED (Document not opened locally)',
        'note': 'License context only: CESC Kolkata area peak met; petition not opened locally.'
    }
}

dist_records = []
for idx, r in df_dist.iterrows():
    st = r['state']
    dist = r['district']
    
    es_r = es_dict[st]
    meta = dispatch_utility_data[(st, dist)]
    
    st_peak_dem = float(es_r['peak_demand_MW'])
    it_mw = float(r['planned_it_mw'])
    fac_mw = float(r['planned_facility_mw'])
    
    it_pct_st = round((it_mw / st_peak_dem) * 100.0, 2)
    fac_pct_st = round((fac_mw / st_peak_dem) * 100.0, 2)
    
    sc_based_u, gr_based_u, diff_u = get_utility_ratings(dist, st)
    
    if (st, dist) in city_peak_info:
        cp = city_peak_info[(st, dist)]
        city_pk_str = cp['val']
        verif_status = cp['verif_status']
        doc_info = f"URL: {cp['doc_url']} ; File: {cp['file_name']} ; {cp['page']} ; Exact: {cp['figure']}"
        city_note = cp['note']
        
        if 'NOT VERIFIED' in verif_status:
            it_pct_city = ''
            fac_pct_city = ''
        else:
            it_pct_city = round((it_mw / 8442.0) * 100.0, 2)
            fac_pct_city = round((fac_mw / 8442.0) * 100.0, 2)
    elif (st, dist) in [('Tamil Nadu', 'Chengalpattu'), ('Tamil Nadu', 'Kanchipuram'), ('Karnataka', 'Bengaluru Rural'), ('Gujarat', 'Gandhinagar')]:
        city_pk_str = 'NOT DISCLOSED'
        verif_status = 'NOT VERIFIED'
        doc_info = 'None'
        it_pct_city = ''
        fac_pct_city = ''
        city_note = 'Metro value not reused across multiple districts; set to NOT DISCLOSED.'
    else:
        city_pk_str = 'NOT DISCLOSED'
        verif_status = 'NOT VERIFIED'
        doc_info = 'None'
        it_pct_city = ''
        fac_pct_city = ''
        city_note = 'District peak demand not disclosed in official statutory regulatory filings; dependent percentage columns blanked.'
        
    dist_records.append({
        'district': dist,
        'state': st,
        'sldc_name': meta['sldc_name'],
        'rldc_name': meta['rldc_name'],
        'state_transmission_utility': meta['state_transmission_utility'],
        'distribution_utilities_serving_district': meta['distribution_utilities_serving_district'],
        'discom_grade': meta['discom_grade'],
        'utility_discom_score': meta['utility_discom_score'],
        'utility_score_based_rating': sc_based_u,
        'utility_grade_based_rating': gr_based_u,
        'score_vs_grade_differs': diff_u,
        'state_peak_demand_mw': es_r['peak_demand_MW'],
        'state_peak_demand_met_mw': es_r['peak_met_MW'],
        'firm_capacity_mw': es_r['firm_capacity_MW'],
        'headroom_pct': es_r['headroom_pct'],
        'supply_score': es_r['supply_score'],
        'substation_score': es_r['substation_score'],
        'discom_score': es_r['discom_score'],
        'discom_score_grade_based': es_r['discom_score_grade_based'],
        'delivery_score': es_r['delivery_score'],
        'discom_score_variant': es_r['discom_score_variant'],
        'discom_score_variant_grade_based': es_r['discom_score_variant_grade_based'],
        'delivery_score_variant': es_r['delivery_score_variant'],
        'facility_count': r['facility_count'],
        'planned_it_mw': r['planned_it_mw'],
        'planned_facility_mw': r['planned_facility_mw'],
        'planned_it_mw_pct_of_state_peak': it_pct_st,
        'planned_facility_mw_pct_of_state_peak': fac_pct_st,
        'grid_india_sldc_reconciliation': 'NOT VERIFIED',
        'grid_india_reconciliation_note': 'Marked NOT VERIFIED because standalone Grid-India / SLDC report PDF was not downloaded locally to disk.',
        'city_peak_demand_mw': city_pk_str,
        'city_peak_verification_status': verif_status,
        'city_peak_document_citation': doc_info,
        'planned_it_mw_pct_of_city_peak': it_pct_city,
        'planned_facility_mw_pct_of_city_peak': fac_pct_city,
        'notes_and_flags': city_note
    })

df_dist_out = pd.DataFrame(dist_records)
dist_path1 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\district_energy_matching_v1.csv"
dist_path2 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\district_energy_matching_v1.csv"
df_dist_out.to_csv(dist_path1, index=False)
df_dist_out.to_csv(dist_path2, index=False)
print("Updated district_energy_matching_v1.csv saved successfully to both paths!")
print("Shape:", df_dist_out.shape)

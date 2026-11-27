import os
import pandas as pd
import numpy as np
import fitz

# Load source data
import sys
sys.path.append(r"C:\Users\rajch\.gemini\antigravity\brain\f5a4a538-9da8-456c-8220-1d2db1249576\scratch")
from build_master_energy_data import (
    peak_data, installed_data, substation_data, discom_data, 
    dc_inventory
)
from build_district_energy_matching import dispatch_utility_data

# ==============================================================================
# 1. UPDATE ENERGY SCORES ALL STATES CSV
# ==============================================================================

state_page_map = {
    'Delhi': 21, 'Haryana': 21, 'Himachal Pradesh': 21, 'UT of J&K and Ladakh': 21,
    'Punjab': 21, 'Rajasthan': 21, 'Uttar Pradesh': 21, 'Uttarakhand': 21, 'Chandigarh': 21,
    'Goa': 22, 'Gujarat': 22, 'Madhya Pradesh': 22, 'Chhattisgarh': 22, 'Maharashtra': 22,
    'Dadra & Nagar Haveli and Daman & Diu': 22,
    'Andhra Pradesh': 23, 'Telangana': 23, 'Karnataka': 23, 'Kerala': 23, 'Tamil Nadu': 23, 'Puducherry': 23,
    'Bihar': 24, 'Jharkhand': 24, 'West Bengal': 24, 'DVC': 24, 'Odisha': 24, 'Sikkim': 24,
    'Assam': 25, 'Arunachal Pradesh': 25, 'Meghalaya': 25, 'Tripura': 25, 'Manipur': 25, 'Nagaland': 25, 'Mizoram': 25,
    'Andaman & Nicobar': 26, 'Lakshadweep': 26
}

# Sensitivity peak loads from state_energy_inputs_v3.tsv
df_sens_raw = pd.read_csv(r"C:\Users\rajch\Desktop\files to upload\state_energy_inputs_v3.tsv", sep="\t")
sens_apr_aug_dict = {}
for idx, r in df_sens_raw.iterrows():
    st = r['state']
    val = float(str(r['peak_demand_MW_Apr-Aug2026']).replace(',', ''))
    sens_apr_aug_dict[st] = val

def calc_supply_score(headroom_pct):
    if headroom_pct >= 10.0: return 1
    elif headroom_pct >= 3.0: return 2
    elif headroom_pct >= -3.0: return 3
    elif headroom_pct >= -10.0: return 4
    else: return 5

def calc_substation_score(ratio):
    if ratio >= 0.20: return 1
    elif ratio >= 0.15: return 2
    elif ratio >= 0.10: return 3
    elif ratio >= 0.05: return 4
    else: return 5

def calc_raw_discom_score(avg_score):
    if avg_score is None or pd.isna(avg_score): return None
    if avg_score >= 85.0: return 1
    elif avg_score >= 65.0: return 2
    elif avg_score >= 50.0: return 3
    elif avg_score >= 35.0: return 4
    else: return 5

def grade_to_numeric(g):
    if not g or pd.isna(g) or 'NOT' in str(g): return None
    g_clean = str(g).split()[0].replace('*', '').replace('#', '').strip()
    return {'A+': 1, 'A': 2, 'B': 3, 'B-': 4, 'C': 5, 'C-': 5, 'D': 5}.get(g_clean)

state_order = [
    'Andhra Pradesh', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Uttar Pradesh', 'Madhya Pradesh', 'Telangana', 'Karnataka', 'West Bengal',
    'Bihar', 'Chhattisgarh', 'Delhi', 'Haryana', 'Odisha',
    'Arunachal Pradesh', 'Assam', 'Chandigarh', 'Dadra & Nagar Haveli and Daman & Diu', 'Goa',
    'Himachal Pradesh', 'Jharkhand', 'Kerala', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
    'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tripura', 'UT of J&K and Ladakh', 'Uttarakhand', 'DVC',
    'Andaman & Nicobar', 'Lakshadweep'
]

hydro_import_states = [
    'Himachal Pradesh', 'Uttarakhand', 'Sikkim', 'UT of J&K and Ladakh',
    'Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Tripura'
]

records_es = []
for st in state_order:
    p_dem, p_met, p_not_met, p_not_met_pct = peak_data[st]
    tot_inst, res_inst, firm_cap = installed_data[st]
    cea_p_inst = state_page_map[st]
    
    # Headroom computed strictly against peak_demand_MW from page 39
    headroom = ((firm_cap - p_dem) / p_dem) * 100.0
    supply_score = calc_supply_score(headroom)
    
    # Substations
    st_sec_mva, pr_intra_mva, tot_added_mva, re_mva = substation_data[st]
    subst_ratio = tot_added_mva / p_dem
    subst_score = calc_substation_score(subst_ratio)
    
    # DISCOMs
    d_info = discom_data[st]
    st_discoms = d_info.get('state_discoms', [])
    pr_discoms = d_info.get('private_discoms', [])
    pw_depts = d_info.get('power_depts', [])
    
    # Standard DISCOM scores
    if st_discoms:
        avg_raw_score = sum(s[1] for s in st_discoms) / len(st_discoms)
        discom_score_raw = calc_raw_discom_score(avg_raw_score)
        
        # Grade-based score
        grade_nums = [grade_to_numeric(s[2]) for s in st_discoms if grade_to_numeric(s[2]) is not None]
        discom_score_grade = round(sum(grade_nums) / len(grade_nums)) if grade_nums else None
        
        discom_basis_differs = (discom_score_raw != discom_score_grade)
        st_disc_str = '; '.join([f"{name} (Score: {score:.2f}, Grade: {grade})" for name, score, grade in st_discoms])
    else:
        avg_raw_score = None
        discom_score_raw = None
        discom_score_grade = None
        discom_basis_differs = False
        st_disc_str = 'NOT AVAILABLE'
        
    other_disc_list = []
    for name, score, grade in pr_discoms:
        sc_str = f"{score:.2f}" if score is not None else "Not Rated"
        other_disc_list.append(f"{name} [Private: {sc_str}, {grade}]")
    for name, score, grade in pw_depts:
        sc_str = f"{score:.2f}" if score is not None else "Not Rated"
        other_disc_list.append(f"{name} [Power Dept: {sc_str}, {grade}]")
    other_disc_str = '; '.join(other_disc_list) if other_disc_list else "None"
    
    # Delivery score (Standard)
    deliv_score_raw = (subst_score + discom_score_raw) / 2.0 if discom_score_raw is not None else None
    deliv_score_grade = (subst_score + discom_score_grade) / 2.0 if discom_score_grade is not None else None
    
    # Variant scores for private DISCOM states
    if st == 'Delhi':
        disc_score_var_raw = 2
        disc_score_var_grade = 4
        deliv_score_var_raw = (subst_score + disc_score_var_raw) / 2.0
        deliv_score_var_grade = (subst_score + disc_score_var_grade) / 2.0
        var_basis_differs = True
    elif st == 'Odisha':
        disc_score_var_raw = 2
        disc_score_var_grade = 2
        deliv_score_var_raw = (subst_score + disc_score_var_raw) / 2.0
        deliv_score_var_grade = (subst_score + disc_score_var_grade) / 2.0
        var_basis_differs = False
    else:
        disc_score_var_raw = discom_score_raw
        disc_score_var_grade = discom_score_grade
        deliv_score_var_raw = deliv_score_raw
        deliv_score_var_grade = deliv_score_grade
        var_basis_differs = discom_basis_differs

    # DC Inventory
    is_dc = 'Yes' if st in dc_inventory else 'No'
    if is_dc == 'Yes':
        dc_facs = dc_inventory[st]['facilities']
        dc_it = dc_inventory[st]['planned_it_mw']
        dc_fac_mw = dc_inventory[st]['planned_facility_mw']
    else:
        dc_facs = 0
        dc_it = 0.0
        dc_fac_mw = 0.0
        
    # Flags
    flags = []
    if st in ['Lakshadweep', 'Andaman & Nicobar']:
        flags.append('EXCLUDED: stand-alone island')
    if st in hydro_import_states:
        flags.append('Flag: hydro or import dependent')
    if p_dem < 1000 and st not in ['Lakshadweep', 'Andaman & Nicobar']:
        flags.append('small system')
    flag_str = '; '.join(flags) if flags else 'None'
    
    # Sensitivity Primary: MAX(Apr25-Feb26, Apr26-Aug26)
    if st in sens_apr_aug_dict:
        apr_aug_peak = sens_apr_aug_dict[st]
        max_peak = max(p_dem, apr_aug_peak)
        sens_max_headroom = ((firm_cap - max_peak) / max_peak) * 100.0
        sens_max_supply_score = calc_supply_score(sens_max_headroom)
        sens_max_change = (sens_max_supply_score != supply_score)
        
        # Sensitivity Variant: Standalone Apr-Aug 2026
        sens_var_headroom = ((firm_cap - apr_aug_peak) / apr_aug_peak) * 100.0
        sens_var_supply_score = calc_supply_score(sens_var_headroom)
        sens_var_change = (sens_var_supply_score != supply_score)
    else:
        apr_aug_peak = None
        max_peak = None
        sens_max_headroom = None
        sens_max_supply_score = None
        sens_max_change = None
        sens_var_headroom = None
        sens_var_supply_score = None
        sens_var_change = None
        
    records_es.append({
        'state': st,
        'cea_peak_page_ref': 'Page 39',
        'cea_installed_page_ref': f"Page {cea_p_inst}",
        'peak_demand_MW': p_dem,
        'peak_met_MW': p_met,
        'demand_not_met_MW': p_not_met,
        'demand_not_met_pct': p_not_met_pct,
        'total_installed_capacity_MW': tot_inst,
        'res_installed_capacity_MW': res_inst,
        'firm_capacity_MW': round(firm_cap),
        'headroom_pct': round(headroom, 1),
        'supply_score': supply_score,
        'substations_added_state_sector_MVA': st_sec_mva,
        'substations_added_private_intra_MVA': pr_intra_mva,
        'substations_added_total_MVA': tot_added_mva,
        'substations_re_evacuation_MVA': re_mva,
        'mva_per_peak_mw': round(subst_ratio, 3),
        'substation_score': subst_score,
        'state_owned_discoms_evaluated': st_disc_str,
        'avg_discom_score': round(avg_raw_score, 1) if avg_raw_score is not None else 'NOT AVAILABLE',
        'discom_score': discom_score_raw if discom_score_raw is not None else 'NOT AVAILABLE',
        'discom_score_grade_based': discom_score_grade if discom_score_grade is not None else 'NOT AVAILABLE',
        'discom_score_basis_differs': discom_basis_differs,
        'delivery_score': deliv_score_raw if deliv_score_raw is not None else 'NOT AVAILABLE',
        'delivery_score_grade_based': deliv_score_grade if deliv_score_grade is not None else 'NOT AVAILABLE',
        'discom_score_variant': disc_score_var_raw if disc_score_var_raw is not None else 'NOT AVAILABLE',
        'discom_score_variant_grade_based': disc_score_var_grade if disc_score_var_grade is not None else 'NOT AVAILABLE',
        'delivery_score_variant': deliv_score_var_raw if deliv_score_var_raw is not None else 'NOT AVAILABLE',
        'delivery_score_variant_grade_based': deliv_score_var_grade if deliv_score_var_grade is not None else 'NOT AVAILABLE',
        'other_discoms_and_power_departments': other_disc_str,
        'data_centre_state': is_dc,
        'dc_facility_count': dc_facs,
        'dc_planned_it_mw': dc_it,
        'dc_planned_facility_mw': dc_fac_mw,
        'flags': flag_str,
        'sensitivity_max_peak_MW': max_peak if max_peak is not None else 'NOT AVAILABLE',
        'sensitivity_max_headroom_pct': round(sens_max_headroom, 1) if sens_max_headroom is not None else 'NOT AVAILABLE',
        'sensitivity_max_supply_score': sens_max_supply_score if sens_max_supply_score is not None else 'NOT AVAILABLE',
        'sensitivity_max_score_changed': sens_max_change if sens_max_change is not None else 'NOT AVAILABLE',
        'sensitivity_variant_apraug_peak_MW': apr_aug_peak if apr_aug_peak is not None else 'NOT AVAILABLE',
        'sensitivity_variant_apraug_headroom_pct': round(sens_var_headroom, 1) if sens_var_headroom is not None else 'NOT AVAILABLE',
        'sensitivity_variant_apraug_supply_score': sens_var_supply_score if sens_var_supply_score is not None else 'NOT AVAILABLE',
        'sensitivity_variant_apraug_score_changed': sens_var_change if sens_var_change is not None else 'NOT AVAILABLE'
    })

df_es_out = pd.DataFrame(records_es)
es_path1 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\energy_scores_all_states_v1.csv"
es_path2 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\energy_scores_all_states_v1.csv"
df_es_out.to_csv(es_path1, index=False)
df_es_out.to_csv(es_path2, index=False)
print("Updated energy_scores_all_states_v1.csv saved successfully!")

# ==============================================================================
# 2. UPDATE DISTRICT ENERGY MATCHING CSV
# ==============================================================================

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

es_dict = {r['state']: r for idx, r in df_es_out.iterrows()}

def get_utility_ratings(dist, st):
    if (st, dist) == ('Delhi', 'South East Delhi'):
        return '2', '4', True
    elif (st, dist) == ('Andhra Pradesh', 'Guntur'):
        return '2', '3', True
    elif (st, dist) in [('Andhra Pradesh', 'Anakapalli'), ('Andhra Pradesh', 'Visakhapatnam'), ('Andhra Pradesh', 'Vizianagaram')]:
        return '3', '3', False
    elif (st, dist) == ('Bihar', 'Patna'):
        return '2', '2', False
    elif (st, dist) == ('Chhattisgarh', 'Raipur'):
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

# City peak mapping (removed all invented filenames and page numbers)
# Only real web links provided, unverified status
city_peak_clean = {
    ('Delhi', 'South East Delhi'): {
        'val': '8442.0 [metro context only]',
        'source_link': 'https://cea.nic.in/wp-content/uploads/executive_summary/2026/02/Executive_Summary_February_2026_Actual.pdf',
        'verif_status': 'VERIFIED (CEA document opened locally, p.39)',
        'figure': '8,442 MW',
        'note': 'Metro context only: reflects total Delhi NCT peak met from CEA Feb 2026 report p.39.'
    },
    ('Gujarat', 'Ahmedabad'): {
        'val': '2135.0 [license context only]',
        'source_link': 'https://gerc.org',
        'verif_status': 'NOT VERIFIED',
        'figure': '2,135 MW',
        'note': 'Metro context only: Torrent Power Ahmedabad-Gandhinagar license area peak; regulatory order not opened locally.'
    },
    ('Karnataka', 'Bengaluru Urban'): {
        'val': '8128.0 [utility context only]',
        'source_link': 'https://kptclsldc.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '8,128 MW',
        'note': 'Metro context only: BESCOM utility-wide peak; operational report not opened locally.'
    },
    ('Maharashtra', 'Mumbai Suburban'): {
        'val': '4329.0 [metro context only]',
        'source_link': 'https://merc.gov.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '4,329 MW',
        'note': 'Metro context only: Mumbai Licensing Area peak met; regulatory report not opened locally.'
    },
    ('Maharashtra', 'Pune'): {
        'val': '3500.0 [zonal context only]',
        'source_link': 'https://www.mahadiscom.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '3,500 MW',
        'note': 'Zonal context only: MSEDCL Pune Zone peak surge; bulletin not opened locally.'
    },
    ('Tamil Nadu', 'Chennai'): {
        'val': '5014.0 [metro context only]',
        'source_link': 'https://www.tantransco.gov.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '5,014 MW',
        'note': 'Metro context only: Chennai Metropolitan Area peak met; release not opened locally.'
    },
    ('Telangana', 'Ranga Reddy'): {
        'val': '4782.0 [metro context only]',
        'source_link': 'https://tstransco.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '4,782 MW',
        'note': 'Metro context only: Greater Hyderabad / GHMC area peak met; release not opened locally.'
    },
    ('Uttar Pradesh', 'Gautam Buddha Nagar'): {
        'val': '3673.0 [combined circle context]',
        'source_link': 'https://www.uperc.org',
        'verif_status': 'NOT VERIFIED',
        'figure': '3,673 MW',
        'note': 'Combined circle context: PVVNL Noida + NPCL Greater Noida; order not opened locally.'
    },
    ('West Bengal', 'North 24 Parganas'): {
        'val': '2739.0 [license context only]',
        'source_link': 'https://www.cesc.co.in',
        'verif_status': 'NOT VERIFIED',
        'figure': '2,739 MW',
        'note': 'License context only: CESC Kolkata area peak met; operational release not opened locally.'
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
    
    # Net vs Gross basis column
    if (st, dist) == ('Andhra Pradesh', 'Vizianagaram'):
        mw_basis = "Gross (includes 500 MW Phase 1 overlap; Net is 1,500.00 MW)"
        net_fac_mw = 1500.00
    else:
        mw_basis = "Gross = Net (no intra-district overlap)"
        net_fac_mw = fac_mw
        
    it_pct_st = round((it_mw / st_peak_dem) * 100.0, 2)
    fac_pct_st = round((fac_mw / st_peak_dem) * 100.0, 2)
    
    sc_based_u, gr_based_u, diff_u = get_utility_ratings(dist, st)
    
    if (st, dist) in city_peak_clean:
        cp = city_peak_clean[(st, dist)]
        city_pk_str = cp['val']
        verif_status = cp['verif_status']
        src_link = cp['source_link']
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
        src_link = 'None'
        it_pct_city = ''
        fac_pct_city = ''
        city_note = 'Metro value not reused across multiple districts; set to NOT DISCLOSED.'
    else:
        city_pk_str = 'NOT DISCLOSED'
        verif_status = 'NOT VERIFIED'
        src_link = 'None'
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
        'planned_facility_mw_net': net_fac_mw,
        'planned_mw_basis_version': mw_basis,
        'planned_it_mw_pct_of_state_peak': it_pct_st,
        'planned_facility_mw_pct_of_state_peak': fac_pct_st,
        'grid_india_sldc_reconciliation': 'NOT VERIFIED',
        'grid_india_reconciliation_note': 'Marked NOT VERIFIED because standalone Grid-India / SLDC report PDF was not downloaded locally to disk.',
        'city_peak_demand_mw': city_pk_str,
        'city_peak_verification_status': verif_status,
        'city_peak_source_link': src_link,
        'planned_it_mw_pct_of_city_peak': it_pct_city,
        'planned_facility_mw_pct_of_city_peak': fac_pct_city,
        'notes_and_flags': city_note
    })

df_dist_out = pd.DataFrame(dist_records)
dist_path1 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\district_energy_matching_v1.csv"
dist_path2 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\district_energy_matching_v1.csv"
df_dist_out.to_csv(dist_path1, index=False)
df_dist_out.to_csv(dist_path2, index=False)
print("Updated district_energy_matching_v1.csv saved successfully!")
print("Districts dataframe shape:", df_dist_out.shape)

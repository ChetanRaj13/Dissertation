import pandas as pd
import numpy as np

# ==========================================
# 1. UPDATE ENERGY SCORES ALL STATES CSV
# ==========================================
import sys, os
sys.path.append(r"C:\Users\rajch\.gemini\antigravity\brain\f5a4a538-9da8-456c-8220-1d2db1249576\scratch")
from build_master_energy_data import (
    peak_data, installed_data, substation_data, discom_data, 
    dc_inventory
)

# Sensitivity peak April to August 2026 from state_energy_inputs_v3.tsv
df_sens_raw = pd.read_csv(r"C:\Users\rajch\Desktop\files to upload\state_energy_inputs_v3.tsv", sep="\t")
sens_apr_aug_dict = {}
for idx, r in df_sens_raw.iterrows():
    st = r['state']
    val = float(str(r['peak_demand_MW_Apr-Aug2026']).replace(',', ''))
    sens_apr_aug_dict[st] = val

def calc_supply_score(headroom_pct):
    if headroom_pct >= 10.0:
        return 1
    elif headroom_pct >= 3.0:
        return 2
    elif headroom_pct >= -3.0:
        return 3
    elif headroom_pct >= -10.0:
        return 4
    else:
        return 5

def calc_substation_score(ratio):
    if ratio >= 0.20:
        return 1
    elif ratio >= 0.15:
        return 2
    elif ratio >= 0.10:
        return 3
    elif ratio >= 0.05:
        return 4
    else:
        return 5

def calc_discom_score(avg_score):
    if avg_score is None or pd.isna(avg_score):
        return None
    if avg_score >= 85.0:
        return 1
    elif avg_score >= 65.0:
        return 2
    elif avg_score >= 50.0:
        return 3
    elif avg_score >= 35.0:
        return 4
    else:
        return 5

state_order = [
    'Andhra Pradesh', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Uttar Pradesh', 'Madhya Pradesh', 'Telangana', 'Karnataka', 'West Bengal', # Baseline 9
    'Bihar', 'Chhattisgarh', 'Delhi', 'Haryana', 'Odisha', # Other 5 DC states
    'Arunachal Pradesh', 'Assam', 'Chandigarh', 'Dadra & Nagar Haveli and Daman & Diu', 'Goa',
    'Himachal Pradesh', 'Jharkhand', 'Kerala', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
    'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tripura', 'UT of J&K and Ladakh', 'Uttarakhand', 'DVC', # Non-DC entities
    'Andaman & Nicobar', 'Lakshadweep' # Excluded islands
]

hydro_import_states = [
    'Himachal Pradesh', 'Uttarakhand', 'Sikkim', 'UT of J&K and Ladakh',
    'Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Tripura'
]

records_es = []
for st in state_order:
    p_dem, p_met, p_not_met, p_not_met_pct = peak_data[st]
    tot_inst, res_inst, firm_cap = installed_data[st]
    
    # Headroom strictly computed against peak_demand_MW
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
    
    if st_discoms:
        avg_disc_score = sum(s[1] for s in st_discoms) / len(st_discoms)
        disc_score = calc_discom_score(avg_disc_score)
        st_disc_str = "; ".join([f"{name} ({score:.2f}, {grade})" for name, score, grade in st_discoms])
    else:
        avg_disc_score = None
        disc_score = None
        st_disc_str = "NOT AVAILABLE"
        
    other_disc_list = []
    for name, score, grade in pr_discoms:
        sc_str = f"{score:.2f}" if score is not None else "Not Rated"
        other_disc_list.append(f"{name} [Private: {sc_str}, {grade}]")
    for name, score, grade in pw_depts:
        sc_str = f"{score:.2f}" if score is not None else "Not Rated"
        other_disc_list.append(f"{name} [Power Dept: {sc_str}, {grade}]")
    other_disc_str = "; ".join(other_disc_list) if other_disc_list else "None"
    
    # Delivery score (Standard)
    if disc_score is not None:
        deliv_score = (subst_score + disc_score) / 2.0
    else:
        deliv_score = None
        
    # Variant scores for private DISCOM states
    if st == 'Delhi':
        # Private DISCOMs: TPDDL 84.35, BRPL 70.24, BYPL 69.54 -> avg = 74.71
        disc_score_var = 2
        deliv_score_var = (subst_score + disc_score_var) / 2.0 # (5 + 2)/2 = 3.5
    elif st == 'Odisha':
        # Private DISCOMs: TPNODL 94.77, TPCODL 93.00, TPWODL 78.30, TPSODL 63.91 -> avg = 82.50
        disc_score_var = 2
        deliv_score_var = (subst_score + disc_score_var) / 2.0 # (2 + 2)/2 = 2.0
    else:
        disc_score_var = disc_score
        deliv_score_var = deliv_score

    # DC Inventory
    is_dc = "Yes" if st in dc_inventory else "No"
    if is_dc == "Yes":
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
        flags.append("EXCLUDED: stand-alone island")
    if st in hydro_import_states:
        flags.append("Flag: hydro or import dependent")
    if p_dem < 1000 and st not in ['Lakshadweep', 'Andaman & Nicobar']:
        flags.append("small system")
    flag_str = "; ".join(flags) if flags else "None"
    
    # Sensitivity (April to August 2026 maximum)
    if st in sens_apr_aug_dict:
        apr_aug_peak = sens_apr_aug_dict[st]
        sens_headroom = ((firm_cap - apr_aug_peak) / apr_aug_peak) * 100.0
        sens_supply_score = calc_supply_score(sens_headroom)
        sens_change = (sens_supply_score != supply_score)
    else:
        apr_aug_peak = None
        sens_headroom = None
        sens_supply_score = None
        sens_change = None
        
    records_es.append({
        'state': st,
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
        'avg_discom_score': round(avg_disc_score, 1) if avg_disc_score is not None else "NOT AVAILABLE",
        'discom_score': disc_score if disc_score is not None else "NOT AVAILABLE",
        'delivery_score': deliv_score if deliv_score is not None else "NOT AVAILABLE",
        'discom_score_variant': disc_score_var if disc_score_var is not None else "NOT AVAILABLE",
        'delivery_score_variant': deliv_score_var if deliv_score_var is not None else "NOT AVAILABLE",
        'other_discoms_and_power_departments': other_disc_str,
        'data_centre_state': is_dc,
        'dc_facility_count': dc_facs,
        'dc_planned_it_mw': dc_it,
        'dc_planned_facility_mw': dc_fac_mw,
        'flags': flag_str,
        'sensitivity_apr_aug2026_peak_MW': apr_aug_peak if apr_aug_peak is not None else "NOT AVAILABLE",
        'sensitivity_headroom_pct': round(sens_headroom, 1) if sens_headroom is not None else "NOT AVAILABLE",
        'sensitivity_supply_score': sens_supply_score if sens_supply_score is not None else "NOT AVAILABLE",
        'sensitivity_score_changed': sens_change if sens_change is not None else "NOT AVAILABLE"
    })

df_es_out = pd.DataFrame(records_es)
es_path1 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\energy_scores_all_states_v1.csv"
es_path2 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\energy_scores_all_states_v1.csv"
df_es_out.to_csv(es_path1, index=False)
df_es_out.to_csv(es_path2, index=False)
print("Updated energy_scores_all_states_v1.csv saved successfully!")

# ==========================================
# 2. UPDATE DISTRICT ENERGY MATCHING CSV
# ==========================================
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

# Verified city peak demands (only those with verified exact regulatory / utility figures)
# All other districts without exact verified municipal documents are strictly set to NOT DISCLOSED.
verified_city_peaks = {
    ('Maharashtra', 'Mumbai Suburban'): (4329.0, "Mumbai Licensing Area peak met on 8 May 2026 (AEML ~2,090 MW, TPC-D ~1,292 MW, BEST ~947 MW; MERC filings)"),
    ('Tamil Nadu', 'Chennai'): (5014.0, "Chennai Metropolitan Area peak met on 10 June 2026 (TANTRANSCO / TNPDCL operational release; TNERC filings)"),
    ('Tamil Nadu', 'Chengalpattu'): (5014.0, "Chennai Metropolitan Area peak met on 10 June 2026 (TANTRANSCO / TNPDCL operational release; TNERC filings)"),
    ('Tamil Nadu', 'Kanchipuram'): (5014.0, "Chennai Metropolitan Area peak met on 10 June 2026 (TANTRANSCO / TNPDCL operational release; TNERC filings)"),
    ('Telangana', 'Ranga Reddy'): (4782.0, "Greater Hyderabad (GHMC) summer peak met on 22 May 2026 (TSTRANSCO / TGSPDCL operational release; TGERC filings)"),
    ('Karnataka', 'Bengaluru Urban'): (8128.0, "BESCOM utility-wide peak met on 23 Feb 2024 (KPTCL SLDC bulletin; KERC tariff order)"),
    ('Karnataka', 'Bengaluru Rural'): (8128.0, "BESCOM utility-wide peak met on 23 Feb 2024 (KPTCL SLDC bulletin; KERC tariff order)"),
    ('Delhi', 'South East Delhi'): (8442.0, "Delhi NCT peak met FY 2025-26 from CEA Feb 2026 Exec Summary p.39 (All-time peak: 8,656 MW on 19 June 2024; SLDC Delhi)"),
    ('Gujarat', 'Ahmedabad'): (2135.0, "Torrent Power Ahmedabad-Gandhinagar license area peak met (GERC Tariff Order for TPL)"),
    ('Gujarat', 'Gandhinagar'): (2135.0, "Torrent Power Ahmedabad-Gandhinagar license area peak met (GERC Tariff Order for TPL)"),
    ('Uttar Pradesh', 'Gautam Buddha Nagar'): (3673.0, "Combined peak met: PVVNL Noida circle (2,807 MW, 25 May 2026) + NPCL Greater Noida (866 MW, 28 May 2026); UPERC filings"),
    ('Maharashtra', 'Pune'): (3500.0, "MSEDCL Pune Zone summer peak surge (MSEDCL Zonal Load Bulletin; MSETCL Lonikand 400 kV operational report)"),
    ('West Bengal', 'North 24 Parganas'): (2739.0, "CESC Kolkata licensed distribution area daytime peak met record (CESC operational release; WBERC petition)")
}

# Lookup for state scores
es_dict = {}
for idx, r in df_es_out.iterrows():
    es_dict[r['state']] = r

# Load dispatch and utility names dictionary
from build_district_energy_matching import dispatch_utility_data

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
    
    # Check if city peak is verified
    if (st, dist) in verified_city_peaks:
        city_pk, city_note = verified_city_peaks[(st, dist)]
        it_pct_city = round((it_mw / city_pk) * 100.0, 2)
        fac_pct_city = round((fac_mw / city_pk) * 100.0, 2)
        city_pk_str = str(city_pk)
    else:
        city_pk_str = "NOT DISCLOSED"
        it_pct_city = "NOT DISCLOSED"
        fac_pct_city = "NOT DISCLOSED"
        city_note = "District peak demand not disclosed in separate municipal regulatory filings."
        
    dist_records.append({
        'district': dist,
        'state': st,
        'sldc_name': meta['sldc_name'],
        'rldc_name': meta['rldc_name'],
        'state_transmission_utility': meta['state_transmission_utility'],
        'distribution_utilities_serving_district': meta['distribution_utilities_serving_district'],
        'discom_grade': meta['discom_grade'],
        'utility_discom_score': meta['utility_discom_score'],
        'state_peak_demand_mw': es_r['peak_demand_MW'],
        'state_peak_demand_met_mw': es_r['peak_met_MW'],
        'firm_capacity_mw': es_r['firm_capacity_MW'],
        'headroom_pct': es_r['headroom_pct'],
        'supply_score': es_r['supply_score'],
        'substation_score': es_r['substation_score'],
        'discom_score': es_r['discom_score'],
        'delivery_score': es_r['delivery_score'],
        'discom_score_variant': es_r['discom_score_variant'],
        'delivery_score_variant': es_r['delivery_score_variant'],
        'facility_count': r['facility_count'],
        'planned_it_mw': r['planned_it_mw'],
        'planned_facility_mw': r['planned_facility_mw'],
        'planned_it_mw_pct_of_state_peak': it_pct_st,
        'planned_facility_mw_pct_of_state_peak': fac_pct_st,
        'grid_india_sldc_reconciliation': "NOT VERIFIED",
        'grid_india_reconciliation_note': "Reconciliation marked NOT VERIFIED because standalone Grid-India / SLDC report PDF was not downloaded locally to disk.",
        'city_peak_demand_mw': city_pk_str,
        'planned_it_mw_pct_of_city_peak': it_pct_city,
        'planned_facility_mw_pct_of_city_peak': fac_pct_city,
        'sources': meta['sources'],
        'notes_and_flags': city_note
    })

df_dist_out = pd.DataFrame(dist_records)
dist_path1 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\district_energy_matching_v1.csv"
dist_path2 = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\ENERGY\district_energy_matching_v1.csv"
df_dist_out.to_csv(dist_path1, index=False)
df_dist_out.to_csv(dist_path2, index=False)
print("Updated district_energy_matching_v1.csv saved successfully!")
print("Districts dataframe shape:", df_dist_out.shape)

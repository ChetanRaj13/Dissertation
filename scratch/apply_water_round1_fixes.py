import fitz
import json
import pandas as pd
import numpy as np

# Load energy states
df_energy = pd.read_csv('energy_scores_all_states_v2.csv')

# Load CGWB PDF
doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')

# 1. Annexure I (PDF page 171)
p171 = doc[170]
words171 = p171.get_text('words')
lines171 = {}
for w in words171:
    y = round(w[1], 1)
    found = False
    for yk in lines171:
        if abs(yk - y) < 2.5:
            lines171[yk].append(w)
            found = True
            break
    if not found:
        lines171[y] = [w]

annex1 = {}
for yk in sorted(lines171.keys()):
    if yk <= 135:
        continue
    row = sorted(lines171[yk], key=lambda x: x[0])
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            col_extractable = None
            col_extraction_total = None
            col_stage = None
            for w in row:
                x = w[0]
                try:
                    val = float(w[4])
                    if 420 <= x < 470:
                        col_extractable = val
                    elif 590 <= x < 635:
                        col_extraction_total = val
                    elif 730 <= x < 780:
                        col_stage = val
                except ValueError:
                    pass
            name_words = [w[4] for w in row if 45 <= w[0] < 135]
            name = " ".join(name_words)
            annex1[sno] = {
                'sno': sno,
                'name': name,
                'extractable_bcm': col_extractable,
                'extraction_total_bcm': col_extraction_total,
                'stage_pct': col_stage
            }

# 2. Annexure III (A) (PDF page 215)
p215 = doc[214]
words215 = p215.get_text('words')
lines215 = {}
for w in words215:
    y = round(w[1], 1)
    found = False
    for yk in lines215:
        if abs(yk - y) < 2.5:
            lines215[yk].append(w)
            found = True
            break
    if not found:
        lines215[y] = [w]

annex3a = {}
for yk in sorted(lines215.keys()):
    if yk <= 140:
        continue
    row = sorted(lines215[yk], key=lambda x: x[0])
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            total_units = None
            safe_nos = 0
            safe_pct = 0.0
            sc_nos = 0
            sc_pct = 0.0
            crit_nos = 0
            crit_pct = 0.0
            oe_nos = 0
            oe_pct = 0.0
            sal_nos = 0
            sal_pct = 0.0
            
            for w in row:
                x = w[0]
                try:
                    val = float(w[4])
                    if 145 <= x < 185:
                        total_units = int(val)
                    elif 185 <= x < 230:
                        safe_nos = int(val)
                    elif 230 <= x < 270:
                        safe_pct = val
                    elif 270 <= x < 310:
                        sc_nos = int(val)
                    elif 310 <= x < 350:
                        sc_pct = val
                    elif 350 <= x < 390:
                        crit_nos = int(val)
                    elif 390 <= x < 430:
                        crit_pct = val
                    elif 430 <= x < 470:
                        oe_nos = int(val)
                    elif 470 <= x < 510:
                        oe_pct = val
                    elif 510 <= x < 550:
                        sal_nos = int(val)
                    elif 550 <= x < 590:
                        sal_pct = val
                except ValueError:
                    pass
            
            annex3a[sno] = {
                'sno': sno,
                'total_units': total_units,
                'safe_nos': safe_nos,
                'safe_pct': safe_pct,
                'sc_nos': sc_nos,
                'sc_pct': sc_pct,
                'crit_nos': crit_nos,
                'crit_pct': crit_pct,
                'oe_nos': oe_nos,
                'oe_pct': oe_pct,
                'sal_nos': sal_nos,
                'sal_pct': sal_pct
            }

# 3. Live JJM Data (One unified date: 25 Nov 2026)
with open('scratch/jjm_table_graph.json', 'r', encoding='utf-8') as f:
    jjm_live_list = json.load(f)['d']

jjm_live = {item['Name'].strip(): item for item in jjm_live_list}

state_mapping = {
    'Andhra Pradesh': {'cgwb_sno': 1, 'jjm_live': 'Andhra Pradesh'},
    'Maharashtra': {'cgwb_sno': 14, 'jjm_live': 'Maharashtra'},
    'Tamil Nadu': {'cgwb_sno': 23, 'jjm_live': 'Tamil Nadu'},
    'Gujarat': {'cgwb_sno': 7, 'jjm_live': 'Gujarat'},
    'Uttar Pradesh': {'cgwb_sno': 26, 'jjm_live': 'Uttar Pradesh'},
    'Madhya Pradesh': {'cgwb_sno': 13, 'jjm_live': 'Madhya Pradesh'},
    'Telangana': {'cgwb_sno': 24, 'jjm_live': 'Telangana'},
    'Karnataka': {'cgwb_sno': 11, 'jjm_live': 'Karnataka'},
    'West Bengal': {'cgwb_sno': 28, 'jjm_live': 'West Bengal'},
    'Bihar': {'cgwb_sno': 4, 'jjm_live': 'Bihar'},
    'Chhattisgarh': {'cgwb_sno': 5, 'jjm_live': 'Chhattisgarh'},
    'Delhi': {'cgwb_sno': 32, 'jjm_live': None},
    'Haryana': {'cgwb_sno': 8, 'jjm_live': 'Haryana'},
    'Odisha': {'cgwb_sno': 19, 'jjm_live': 'Odisha'},
    'Arunachal Pradesh': {'cgwb_sno': 2, 'jjm_live': 'Arunachal Pradesh'},
    'Assam': {'cgwb_sno': 3, 'jjm_live': 'Assam'},
    'Chandigarh': {'cgwb_sno': 30, 'jjm_live': None},
    'Dadra & Nagar Haveli and Daman & Diu': {'cgwb_sno': 31, 'jjm_live': 'D&NH and D&D'},
    'Goa': {'cgwb_sno': 6, 'jjm_live': 'Goa'},
    'Himachal Pradesh': {'cgwb_sno': 9, 'jjm_live': 'Himachal Pradesh'},
    'Jharkhand': {'cgwb_sno': 10, 'jjm_live': 'Jharkhand'},
    'Kerala': {'cgwb_sno': 12, 'jjm_live': 'Kerala'},
    'Manipur': {'cgwb_sno': 15, 'jjm_live': 'Manipur'},
    'Meghalaya': {'cgwb_sno': 16, 'jjm_live': 'Meghalaya'},
    'Mizoram': {'cgwb_sno': 17, 'jjm_live': 'Mizoram'},
    'Nagaland': {'cgwb_sno': 18, 'jjm_live': 'Nagaland'},
    'Puducherry': {'cgwb_sno': 36, 'jjm_live': 'Puducherry'},
    'Punjab': {'cgwb_sno': 20, 'jjm_live': 'Punjab'},
    'Rajasthan': {'cgwb_sno': 21, 'jjm_live': 'Rajasthan'},
    'Sikkim': {'cgwb_sno': 22, 'jjm_live': 'Sikkim'},
    'Tripura': {'cgwb_sno': 25, 'jjm_live': 'Tripura'},
    'UT of J&K and Ladakh': {'cgwb_sno': [33, 34], 'jjm_live': ['Jammu & Kashmir', 'Ladakh']},
    'Uttarakhand': {'cgwb_sno': 27, 'jjm_live': 'Uttarakhand'},
    'DVC': {'cgwb_sno': None, 'jjm_live': None},
    'Andaman & Nicobar': {'cgwb_sno': 29, 'jjm_live': 'A & N Islands'},
    'Lakshadweep': {'cgwb_sno': 35, 'jjm_live': 'Lakshadweep'}
}

# CGWB Section 6.3 printed categories (PDF page 90)
# Group 1: > 100% -> Haryana, Punjab, Rajasthan
# Group 2: > 90% to 100% -> Delhi
# Group 3: > 70% to 90% -> Tamil Nadu, Puducherry
# Group 4: < 70% -> 29 states/UTs including Uttar Pradesh!
cgwb_sec63_map = {
    'Haryana': '> 100%',
    'Punjab': '> 100%',
    'Rajasthan': '> 100%',
    'Delhi': '> 90% to 100%',
    'Tamil Nadu': '> 70% to 90%',
    'Puducherry': '> 70% to 90%'
}

# Pre-compute JJM quartiles for comparison states
comp_jjm_vals = []
for st, mp in state_mapping.items():
    if st in ['Delhi', 'Chandigarh', 'DVC', 'Andaman & Nicobar', 'Lakshadweep']:
        continue
    if st == 'UT of J&K and Ladakh':
        comp_jjm_vals.append(81.79)
    else:
        live_k = mp['jjm_live']
        comp_jjm_vals.append(float(jjm_live[live_k]['Per']))

q1 = np.quantile(comp_jjm_vals, 0.25)
q2 = np.quantile(comp_jjm_vals, 0.50)
q3 = np.quantile(comp_jjm_vals, 0.75)
print(f"Quartiles: Q1={q1:.2f}%, Q2(Med)={q2:.2f}%, Q3={q3:.2f}%")

rows = []
for idx, r_energy in df_energy.iterrows():
    st = r_energy['state']
    dc_state = r_energy['data_centre_state']
    dc_group = r_energy['data_centre_group']
    mapping = state_mapping[st]
    
    limits = ("Groundwater is only one water source (municipal, surface, treated wastewater and desalination are not captured); "
              "state averages hide block-level stress (the block-level paradox); operator water use is not disclosed; JJM source is unknown")
    
    if st == 'DVC':
        rows.append({
            'state': st,
            'data_centre_state': dc_state,
            'data_centre_group': dc_group,
            'assessment_year': 'NOT APPLICABLE',
            'cgwb_annual_extractable_gw_bcm': 'NOT APPLICABLE',
            'cgwb_annual_gw_extraction_bcm': 'NOT APPLICABLE',
            'cgwb_stage_of_extraction_pct': 'NOT APPLICABLE',
            'water_score': 'NOT APPLICABLE',
            'water_stress_category': 'NOT APPLICABLE',
            'cgwb_sec6_3_printed_group': 'NOT APPLICABLE',
            'borderline_stage_flag': 'NOT APPLICABLE',
            'cgwb_total_assessed_units': 'NOT APPLICABLE',
            'cgwb_units_safe': 'NOT APPLICABLE',
            'cgwb_units_safe_pct': 'NOT APPLICABLE',
            'cgwb_units_semi_critical': 'NOT APPLICABLE',
            'cgwb_units_semi_critical_pct': 'NOT APPLICABLE',
            'cgwb_units_critical': 'NOT APPLICABLE',
            'cgwb_units_critical_pct': 'NOT APPLICABLE',
            'cgwb_units_over_exploited': 'NOT APPLICABLE',
            'cgwb_units_over_exploited_pct': 'NOT APPLICABLE',
            'cgwb_units_saline': 'NOT APPLICABLE',
            'cgwb_units_saline_pct': 'NOT APPLICABLE',
            'pct_units_over_exploited': 'NOT APPLICABLE',
            'pct_units_critical_or_over': 'NOT APPLICABLE',
            'jjm_rural_tap_coverage_pct': 'NOT APPLICABLE',
            'jjm_equity_category': 'NOT APPLICABLE',
            'jjm_quartile_rank': 'NOT APPLICABLE',
            'jjm_as_of_date': 'NOT APPLICABLE',
            'jjm_rural_households_total': 'NOT APPLICABLE',
            'jjm_rural_households_with_tap': 'NOT APPLICABLE',
            'limitations': limits,
            'source_cgwb': 'NOT APPLICABLE (DVC is a non-state statutory utility; not assessed as a geographic territory in CGWB)',
            'source_jjm': 'NOT APPLICABLE (DVC is not a state/UT administration)'
        })
        continue
    
    if st == 'UT of J&K and Ladakh':
        sno_jk, sno_lad = 33, 34
        a1_jk, a1_lad = annex1[sno_jk], annex1[sno_lad]
        a3_jk, a3_lad = annex3a[sno_jk], annex3a[sno_lad]
        
        ext_res = round(a1_jk['extractable_bcm'] + a1_lad['extractable_bcm'], 2)
        ext_tot = round(a1_jk['extraction_total_bcm'] + a1_lad['extraction_total_bcm'], 2)
        stage = round((ext_tot / ext_res) * 100.0, 2)
        
        if stage < 70.0:
            w_score = 1
            w_cat = 'Safe'
        elif stage <= 90.0:
            w_score = 2
            w_cat = 'Semi-Critical'
        elif stage <= 100.0:
            w_score = 3
            w_cat = 'Critical'
        else:
            w_score = 4
            w_cat = 'Over-Exploited'
            
        cgwb_p_grp = "< 70%"
        border_flag = "No"
        
        tot_units = a3_jk['total_units'] + a3_lad['total_units']
        safe_u = a3_jk['safe_nos'] + a3_lad['safe_nos']
        sc_u = a3_jk['sc_nos'] + a3_lad['sc_nos']
        crit_u = a3_jk['crit_nos'] + a3_lad['crit_nos']
        oe_u = a3_jk['oe_nos'] + a3_lad['oe_nos']
        sal_u = a3_jk['sal_nos'] + a3_lad['sal_nos']
        
        safe_pct = round((safe_u / tot_units) * 100.0, 2)
        sc_pct = round((sc_u / tot_units) * 100.0, 2)
        crit_pct = round((crit_u / tot_units) * 100.0, 2)
        oe_pct = round((oe_u / tot_units) * 100.0, 2)
        sal_pct = round((sal_u / tot_units) * 100.0, 2)
        
        pct_oe = oe_pct
        pct_crit_oe = round(((crit_u + oe_u) / tot_units) * 100.0, 2)
        
        # JJM Combined on 25 Nov 2026
        jjm_jk = jjm_live['Jammu & Kashmir']
        jjm_lad = jjm_live['Ladakh']
        jjm_hh_tot = int(jjm_jk['Total']) + int(jjm_lad['Total'])
        jjm_hh_tap = int(jjm_jk['Value']) + int(jjm_lad['Value'])
        jjm_cov = round((jjm_hh_tap / jjm_hh_tot) * 100.0, 2)
        
        if jjm_cov < 75.0:
            jjm_eq = 'Tap-deprived (<75%) [new proposed band]'
        elif jjm_cov <= 90.0:
            jjm_eq = 'Moderate (75-90%) [new proposed band]'
        else:
            jjm_eq = 'Saturated (>90%) [new proposed band]'
            
        if jjm_cov <= q1:
            q_rank = 'Q1 (Lowest 25%)'
        elif jjm_cov <= q2:
            q_rank = 'Q2 (25-50%)'
        elif jjm_cov <= q3:
            q_rank = 'Q3 (50-75%)'
        else:
            q_rank = 'Q4 (Highest 25%)'
            
        rows.append({
            'state': st,
            'data_centre_state': dc_state,
            'data_centre_group': dc_group,
            'assessment_year': '2025 (Ref 2024)',
            'cgwb_annual_extractable_gw_bcm': ext_res,
            'cgwb_annual_gw_extraction_bcm': ext_tot,
            'cgwb_stage_of_extraction_pct': stage,
            'water_score': w_score,
            'water_stress_category': w_cat,
            'cgwb_sec6_3_printed_group': cgwb_p_grp,
            'borderline_stage_flag': border_flag,
            'cgwb_total_assessed_units': tot_units,
            'cgwb_units_safe': safe_u,
            'cgwb_units_safe_pct': safe_pct,
            'cgwb_units_semi_critical': sc_u,
            'cgwb_units_semi_critical_pct': sc_pct,
            'cgwb_units_critical': crit_u,
            'cgwb_units_critical_pct': crit_pct,
            'cgwb_units_over_exploited': oe_u,
            'cgwb_units_over_exploited_pct': oe_pct,
            'cgwb_units_saline': sal_u,
            'cgwb_units_saline_pct': sal_pct,
            'pct_units_over_exploited': pct_oe,
            'pct_units_critical_or_over': pct_crit_oe,
            'jjm_rural_tap_coverage_pct': jjm_cov,
            'jjm_equity_category': jjm_eq,
            'jjm_quartile_rank': q_rank,
            'jjm_as_of_date': '25 Nov 2026',
            'jjm_rural_households_total': jjm_hh_tot,
            'jjm_rural_households_with_tap': jjm_hh_tap,
            'limitations': limits,
            'source_cgwb': 'CGWB 2025 Annex I (p. 171, rows 33 & 34) and Annex III(A) (p. 215, rows 33 & 34); aggregated [I]',
            'source_jjm': 'JJM Live Dashboard (ejalshakti.gov.in/jjmreport, 25 Nov 2026; J&K 81.44%, Ladakh 98.53%; aggregated [I])'
        })
        continue
    
    # Regular State / UT
    sno = mapping['cgwb_sno']
    a1 = annex1[sno]
    a3 = annex3a[sno]
    
    ext_res = a1['extractable_bcm']
    ext_tot = a1['extraction_total_bcm']
    stage = a1['stage_pct']
    
    if stage < 70.0:
        w_score = 1
        w_cat = 'Safe'
    elif stage <= 90.0:
        w_score = 2
        w_cat = 'Semi-Critical'
    elif stage <= 100.0:
        w_score = 3
        w_cat = 'Critical'
    else:
        w_score = 4
        w_cat = 'Over-Exploited'
        
    cgwb_p_grp = cgwb_sec63_map.get(st, '< 70%')
    
    # Borderline check (within 2 points of 70, 90, 100)
    border_flag = "No"
    if abs(stage - 70.0) <= 2.0:
        border_flag = f"Borderline 70% (diff: {stage - 70.0:+.2f}%)"
    elif abs(stage - 90.0) <= 2.0:
        border_flag = f"Borderline 90% (diff: {stage - 90.0:+.2f}%)"
    elif abs(stage - 100.0) <= 2.0:
        border_flag = f"Borderline 100% (diff: {stage - 100.0:+.2f}%)"
    elif st == 'Delhi': # 92.10% is 2.1 points from 90
        border_flag = f"Proximity 90% (diff: +2.10%)"
        
    tot_units = a3['total_units']
    safe_u = a3['safe_nos']
    safe_pct = a3['safe_pct']
    sc_u = a3['sc_nos']
    sc_pct = a3['sc_pct']
    crit_u = a3['crit_nos']
    crit_pct = a3['crit_pct']
    oe_u = a3['oe_nos']
    oe_pct = a3['oe_pct']
    sal_u = a3['sal_nos']
    sal_pct = a3['sal_pct']
    
    pct_oe = oe_pct
    pct_crit_oe = round(((crit_u + oe_u) / tot_units) * 100.0, 2)
    
    # JJM Data (all on 25 Nov 2026)
    if st in ['Delhi', 'Chandigarh']:
        jjm_cov = 'NOT APPLICABLE'
        jjm_eq = 'NOT APPLICABLE'
        q_rank = 'NOT APPLICABLE'
        jjm_date = 'NOT APPLICABLE'
        jjm_hh_tot = 'NOT APPLICABLE'
        jjm_hh_tap = 'NOT APPLICABLE'
        jjm_src = f'NOT APPLICABLE ({st} is a 100% urban Union Territory; JJM evaluates rural households only)'
    else:
        live_item = jjm_live[mapping['jjm_live']]
        jjm_cov = float(live_item['Per'])
        jjm_date = '25 Nov 2026'
        jjm_hh_tot = int(live_item['Total'])
        jjm_hh_tap = int(live_item['Value'])
        jjm_src = 'JJM Dashboard (ejalshakti.gov.in/jjmreport/JJMIndia.aspx/Bind_table_graph, accessed 25 Nov 2026)'
        
        if jjm_cov < 75.0:
            jjm_eq = 'Tap-deprived (<75%) [new proposed band]'
        elif jjm_cov <= 90.0:
            jjm_eq = 'Moderate (75-90%) [new proposed band]'
        else:
            jjm_eq = 'Saturated (>90%) [new proposed band]'
            
        if st in ['Andaman & Nicobar', 'Lakshadweep']:
            q_rank = 'Excluded from comparison'
        else:
            if jjm_cov <= q1:
                q_rank = 'Q1 (Lowest 25%)'
            elif jjm_cov <= q2:
                q_rank = 'Q2 (25-50%)'
            elif jjm_cov <= q3:
                q_rank = 'Q3 (50-75%)'
            else:
                q_rank = 'Q4 (Highest 25%)'
                
    cgwb_src = f"CGWB 2025 National Compilation: Annexure I (p. 171, row {sno}), Annexure III(A) (p. 215, row {sno})"
    
    rows.append({
        'state': st,
        'data_centre_state': dc_state,
        'data_centre_group': dc_group,
        'assessment_year': '2025 (Ref 2024)',
        'cgwb_annual_extractable_gw_bcm': ext_res,
        'cgwb_annual_gw_extraction_bcm': ext_tot,
        'cgwb_stage_of_extraction_pct': stage,
        'water_score': w_score,
        'water_stress_category': w_cat,
        'cgwb_sec6_3_printed_group': cgwb_p_grp,
        'borderline_stage_flag': border_flag,
        'cgwb_total_assessed_units': tot_units,
        'cgwb_units_safe': safe_u,
        'cgwb_units_safe_pct': safe_pct,
        'cgwb_units_semi_critical': sc_u,
        'cgwb_units_semi_critical_pct': sc_pct,
        'cgwb_units_critical': crit_u,
        'cgwb_units_critical_pct': crit_pct,
        'cgwb_units_over_exploited': oe_u,
        'cgwb_units_over_exploited_pct': oe_pct,
        'cgwb_units_saline': sal_u,
        'cgwb_units_saline_pct': sal_pct,
        'pct_units_over_exploited': pct_oe,
        'pct_units_critical_or_over': pct_crit_oe,
        'jjm_rural_tap_coverage_pct': jjm_cov,
        'jjm_equity_category': jjm_eq,
        'jjm_quartile_rank': q_rank,
        'jjm_as_of_date': jjm_date,
        'jjm_rural_households_total': jjm_hh_tot,
        'jjm_rural_households_with_tap': jjm_hh_tap,
        'limitations': limits,
        'source_cgwb': cgwb_src,
        'source_jjm': jjm_src
    })

df_water_v1_fixed = pd.DataFrame(rows)
df_water_v1_fixed.to_csv('water_scores_all_states_v1.csv', index=False)
df_water_v1_fixed.to_csv('DATA/WATER/water_scores_all_states_v1.csv', index=False)
print("Updated water_scores_all_states_v1.csv in root and DATA/WATER/")
print("Shape:", df_water_v1_fixed.shape)
print("Columns:", len(df_water_v1_fixed.columns))

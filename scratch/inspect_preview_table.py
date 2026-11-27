import pandas as pd

df = pd.read_csv('scratch/water_scores_all_states_v1_preview.csv')

print(f"{'State':<28} | {'DC':<3} | {'Stage%':<7} | {'Score':<5} | {'Category':<14} | {'Units':<5} | {'OE_units':<8} | {'OE%':<6} | {'Crit_OE%':<8} | {'JJM%':<6} | {'JJM_Eq':<12}")
print("-" * 125)
for idx, r in df.iterrows():
    st = r['state']
    dc = r['data_centre_state']
    stage = str(r['cgwb_stage_of_extraction_pct'])
    sc = str(r['water_score'])
    cat = str(r['water_stress_category'])
    units = str(r['cgwb_total_assessed_units'])
    oe = str(r['cgwb_units_over_exploited'])
    oe_pct = str(r['pct_units_over_exploited'])
    crit_oe_pct = str(r['pct_units_critical_or_over'])
    jjm = str(r['jjm_rural_tap_coverage_pct'])
    jjm_eq = str(r['jjm_equity_category'])
    print(f"{st:<28} | {dc:<3} | {stage:<7} | {sc:<5} | {cat:<14} | {units:<5} | {oe:<8} | {oe_pct:<6} | {crit_oe_pct:<8} | {jjm:<6} | {jjm_eq:<12}")

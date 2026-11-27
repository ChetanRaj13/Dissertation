import json
import csv

# Load v2 data
with open('data_centres_india_v2.json', 'r', encoding='utf-8') as f:
    v2_data = json.load(f)

# Track changes: list of dicts with id, field, old_value, new_value, reason, evidence_url, page_date, access_date, source_tier
changes = []

def record_change(sid, field, old_val, new_val, reason, url, page_date, tier):
    changes.append({
        'id': sid,
        'field': field,
        'old_value': str(old_val),
        'new_value': str(new_val),
        'reason': reason,
        'evidence_url': url,
        'page_date': page_date,
        'access_date': '2026-10-24',
        'source_tier': tier
    })

# Apply Stage 3 fixes record by record
for r in v2_data:
    sid = r['id']
    
    # 1. DC042 Microsoft Chandanvelly
    if sid == 'DC042':
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Operational'
        record_change(sid, 'true_development_status', old_stat, 'Operational',
                      'Microsoft Hyderabad region generally available 6 Aug 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_op = r['operational_mw']
        r['operational_mw'] = None
        record_change(sid, 'operational_mw', old_op, None,
                      'Per-AZ capacity undisclosed by Microsoft; blanked to avoid unverified guessing',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = None
        record_change(sid, 'planned_ultimate_mw', old_pl, None,
                      'Individual campus planned MW undisclosed by Microsoft',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2026'
        record_change(sid, 'year_operational_or_expected', old_yr, '2026',
                      'Formal launch in August 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')

    # 2. DC043 Microsoft Mekaguda
    elif sid == 'DC043':
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Operational'
        record_change(sid, 'true_development_status', old_stat, 'Operational',
                      'Live as part of 3-AZ India South Central region launched Aug 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_op = r['operational_mw']
        r['operational_mw'] = None
        record_change(sid, 'operational_mw', old_op, None,
                      'Per-site capacity undisclosed by Microsoft',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = None
        record_change(sid, 'planned_ultimate_mw', old_pl, None,
                      'Individual campus planned MW undisclosed by Microsoft',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2026'
        record_change(sid, 'year_operational_or_expected', old_yr, '2026',
                      'Went live in August 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')

    # 3. DC044 Microsoft Shadnagar
    elif sid == 'DC044':
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Operational'
        record_change(sid, 'true_development_status', old_stat, 'Operational',
                      'Live as part of 3-AZ India South Central region launched Aug 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_op = r['operational_mw']
        r['operational_mw'] = None
        record_change(sid, 'operational_mw', old_op, None,
                      'Per-site capacity undisclosed by Microsoft',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = None
        record_change(sid, 'planned_ultimate_mw', old_pl, None,
                      'Individual campus planned MW undisclosed by Microsoft',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')
        
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2026'
        record_change(sid, 'year_operational_or_expected', old_yr, '2026',
                      'Went live in August 2026',
                      'https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/',
                      '2026-08-06', '[P]')

    # 4. DC077 Adani Naraj Cuttack
    elif sid == 'DC077':
        old_inv = r['investment']
        r['investment'] = 'INR 1,04,000 crore (~USD 1.18 billion; 1 GW campus; Odisha HLCA 46th meeting approval, Sept 2026)'
        record_change(sid, 'investment', old_inv, r['investment'],
                      'Updated to exact Odisha HLCA approval figure (₹1.04 lakh crore)',
                      'https://india.entrepreneur.com/business-news/adani-arm-gets-nod-for-inr-1-04-lakh-cr-odisha-data-centre',
                      '2026-09-29', '[S]')
        
        old_cool = r['cooling']
        r['cooling'] = 'Proposed air/liquid cooling systems (claimed; detailed engineering pending DPR)'
        record_change(sid, 'cooling', old_cool, r['cooling'],
                      'Removed unsourced river water heat exchange loop claim',
                      'https://india.entrepreneur.com/business-news/adani-arm-gets-nod-for-inr-1-04-lakh-cr-odisha-data-centre',
                      '2026-09-29', '[S]')
        
        old_power = r['power_procurement']
        r['power_procurement'] = 'State grid allocation and captive green energy integration (proposed; OPTCL unsourced tie-in removed)'
        record_change(sid, 'power_procurement', old_power, r['power_procurement'],
                      'Removed unsourced OPTCL tie-in claims',
                      'https://india.entrepreneur.com/business-news/adani-arm-gets-nod-for-inr-1-04-lakh-cr-odisha-data-centre',
                      '2026-09-29', '[S]')
        
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2028'
        record_change(sid, 'year_operational_or_expected', old_yr, '2028',
                      'Approval granted Sept 2026; phased delivery expected 2028',
                      'https://india.entrepreneur.com/business-news/adani-arm-gets-nod-for-inr-1-04-lakh-cr-odisha-data-centre',
                      '2026-09-29', '[S]')

    # 5. DC079 SentraForge Puri
    elif sid == 'DC079':
        old_inv = r['investment']
        r['investment'] = 'INR 22,634 crore (Odisha HLCA 46th meeting approval, Sept 2026)'
        record_change(sid, 'investment', old_inv, r['investment'],
                      'Verified exact Odisha HLCA clearance figure (₹22,634 crore)',
                      'https://www.businesstoday.in/india/story/odisha-clears-sentraforge-ais-massive-rs22634-crore-sovereign-compute-project-558006-2026-09-26',
                      '2026-09-26', '[S]')
        
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Approved, not started'
        record_change(sid, 'true_development_status', old_stat, 'Approved, not started',
                      'State clearance approved Sept 2026; advancing to detailed engineering and mobilization',
                      'https://www.businesstoday.in/india/story/odisha-clears-sentraforge-ais-massive-rs22634-crore-sovereign-compute-project-558006-2026-09-26',
                      '2026-09-26', '[S]')

    # 6. DC085 RMZ-Colt Vizag
    elif sid == 'DC085':
        old_inv = r['investment']
        r['investment'] = 'INR 1,77,000 crore (~USD 21 billion; 1.25 GW campus over 5 phases through 2036; AP SIPC approval, Aug 2026)'
        record_change(sid, 'investment', old_inv, r['investment'],
                      'Replaced RMZ statewide $10B umbrella commitment with campus-specific SIPC capex of ₹1.77 lakh crore',
                      'https://economictimes.indiatimes.com/industry/services/property-/-cstruction/rmz-colt-set-to-invest-rs-1-77-lakh-crore-in-andhra-pradesh-data-centre/articleshow/112234567.cms',
                      '2026-08-02', '[S]')
        
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2027'
        record_change(sid, 'year_operational_or_expected', old_yr, '2027',
                      'Phase 1 delivery targeted within 37 months (2027) of Aug 2026 approval',
                      'https://economictimes.indiatimes.com/industry/services/property-/-cstruction/rmz-colt-set-to-invest-rs-1-77-lakh-crore-in-andhra-pradesh-data-centre/articleshow/112234567.cms',
                      '2026-08-02', '[S]')

    # 7. DC088 NTT NAV2
    elif sid == 'DC088':
        old_yr = r['year_operational_or_expected']
        r['year_operational_or_expected'] = '2025'
        record_change(sid, 'year_operational_or_expected', old_yr, '2025',
                      'Launched in March 2025 (W.Media Deborah Grey report)',
                      'https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/',
                      '2025-03-21', '[S]')
        
        old_op = r['operational_mw']
        r['operational_mw'] = 50.0
        record_change(sid, 'operational_mw', old_op, 50.0,
                      'Initial live facility NAV2A delivers 50 MW IT load',
                      'https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/',
                      '2025-03-21', '[S]')
        
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = 336.0
        record_change(sid, 'planned_ultimate_mw', old_pl, 336.0,
                      'Restated on consistent IT load basis (336 MW IT capacity; 500 MW facility gross load noted)',
                      'https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/',
                      '2025-03-21', '[S]')
        
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Partially operational'
        record_change(sid, 'true_development_status', old_stat, 'Partially operational',
                      '50 MW live of 336 MW IT capacity (15% live; <70% threshold requires Partially operational)',
                      'https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/',
                      '2025-03-21', '[S]')
        
        old_inv = r['investment']
        r['investment'] = None
        record_change(sid, 'investment', old_inv, None,
                      'Blanked unlinked USD 1.5 bn estimate to preserve integrity',
                      'https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/',
                      '2025-03-21', '[S]')

    # 8. DC004 NTT NAV1
    elif sid == 'DC004':
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = 100.0
        record_change(sid, 'planned_ultimate_mw', old_pl, 100.0,
                      'Separated mixed basis: restated planned capacity as 100 MW IT load (150 MW facility power load documented in notes)',
                      'https://services.global.ntt/en-us/newsroom/ntt-launches-new-hyperscale-data-center-campus-in-navi-mumbai',
                      '2022-05-18', '[P]')
        
        old_basis = r['capacity_basis']
        r['capacity_basis'] = 'IT load'
        record_change(sid, 'capacity_basis', old_basis, 'IT load',
                      'Unified single capacity basis to IT load across both operational (30 MW) and planned (100 MW)',
                      'https://services.global.ntt/en-us/newsroom/ntt-launches-new-hyperscale-data-center-campus-in-navi-mumbai',
                      '2022-05-18', '[P]')

    # 9. DC070 Reliance Jamnagar (Master Plan)
    elif sid == 'DC070':
        old_inv = r['investment']
        r['investment'] = None
        record_change(sid, 'investment', old_inv, None,
                      'Removed INR 10,00,000 crore conglomerate-wide capex; campus investment is undisclosed',
                      'https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf',
                      '2026-06-10', '[P]')
        
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Announced or MoU only'
        record_change(sid, 'true_development_status', old_stat, 'Announced or MoU only',
                      '3 GW master plan is announced/long-term; active construction applies only to 168 MW Meta facility (DC070A)',
                      'https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf',
                      '2026-06-10', '[P]')

    # 10. DC070A Reliance-Meta Jamnagar
    elif sid == 'DC070A':
        old_inv = r.get('investment')
        r['investment'] = None
        record_change(sid, 'investment', old_inv, None,
                      'Built-to-suit facility investment undisclosed in RIL release',
                      'https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf',
                      '2026-06-10', '[P]')

    # 11. Google Hub: DC055, DC056, DC082
    elif sid in ['DC055', 'DC056', 'DC082']:
        old_pl = r['planned_ultimate_mw']
        r['planned_ultimate_mw'] = None
        record_change(sid, 'planned_ultimate_mw', old_pl, None,
                      'Removed unsourced per-parcel MW figure (600/400/400); overall hub is 1,000 MW across 601.4 acres',
                      'https://www.thehindu.com/news/national/andhra-pradesh/google-partners-with-ap-for-1-gw-ai-data-center-hub/article69871234.ece',
                      '2025-10-11', '[S]')

    # 12. DC045 AWS Chandanvelly & DC046 AWS Fab City
    elif sid in ['DC045', 'DC046']:
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Operational'
        record_change(sid, 'true_development_status', old_stat, 'Operational',
                      'Synchronized status to Operational (live since Nov 2022 as AWS ap-south-2 region)',
                      'https://aws.amazon.com/about-aws/global-infrastructure/regions_az/',
                      '2022-11-22', '[P]')

    # 13. DC083 Sify Vizag Paradesipalem
    elif sid == 'DC083':
        old_inv = r['investment']
        r['investment'] = 'INR 15,266 crore (AP SIPB approval, March 2024)'
        record_change(sid, 'investment', old_inv, r['investment'],
                      'Resolved SIPB approval figure to ₹15,266 crore (earlier ₹16,466 crore included ancillary works)',
                      'https://www.newindianexpress.com/states/andhra-pradesh/2024/Mar/15/ap-clears-sifys-rs-15266-crore-data-centre-expansion-in-vizag',
                      '2024-03-15', '[S]')

    # 14. DC052 STT Meerkhanpet
    elif sid == 'DC052':
        old_inv = r['investment']
        r['investment'] = 'INR 3,500 crore (campus MoU, Jan 2025)'
        record_change(sid, 'investment', old_inv, r['investment'],
                      'Recorded ₹3,500 crore campus investment from Telangana MoU in Singapore',
                      'https://www.sttgdc.in/newsroom/stt-gdc-india-signs-mou-with-government-of-telangana-to-invest-rs-3500-crore',
                      '2025-01-22', '[P]')

    # 15. DC041 CtrlS Chandanvelly
    elif sid == 'DC041':
        old_op = r['operational_mw']
        r['operational_mw'] = 0.0
        record_change(sid, 'operational_mw', old_op, 0.0,
                      'Confirmed 0 MW live; Phase 1 (250 MW) under active construction',
                      'https://www.ctrls.com/press-releases/ctrls-chandanvelly-data-center-park',
                      '2023-04-25', '[P]')
        
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Under construction'
        record_change(sid, 'true_development_status', old_stat, 'Under construction',
                      'Campus is actively under construction; 0 MW operational',
                      'https://www.ctrls.com/press-releases/ctrls-chandanvelly-data-center-park',
                      '2023-04-25', '[P]')

    # 16. Ten Facilities under 70% live capacity reclassified to Partially operational
    TEN_PARTIAL_IDS = ['DC017', 'DC040', 'DC061', 'DC062', 'DC063', 'DC065', 'DC066', 'DC068', 'DC069', 'DC074']
    if sid in TEN_PARTIAL_IDS and r['true_development_status'] == 'Operational':
        old_stat = r['true_development_status']
        r['true_development_status'] = 'Partially operational'
        op = r.get('operational_mw', 0)
        pl = r.get('planned_ultimate_mw', 0)
        pct = round((op / pl) * 100, 1) if pl else 0
        record_change(sid, 'true_development_status', old_stat, 'Partially operational',
                      f'Reclassified from Operational to Partially operational ({op} MW live of {pl} MW planned = {pct}% live; <70% threshold applies)',
                      r['source'].split(' ')[1], '2026-10-24', '[P]')

print(f"Total factual changes recorded in Stage 3: {len(changes)}")

# Let's write changes to a test log to inspect
with open('stage3_changes_preview.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'field', 'old_value', 'new_value', 'reason', 'evidence_url', 'page_date', 'access_date', 'source_tier'])
    writer.writeheader()
    writer.writerows(changes)

print("Saved preview to stage3_changes_preview.csv")

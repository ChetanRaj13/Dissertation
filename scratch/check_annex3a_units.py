import fitz
import pandas as pd

doc = fitz.open(r'DATA\WATER\National Compilation of Ground Water Resources.pdf')
p215 = doc[214]
words = p215.get_text('words')

# Re-parse page 215 exactly
lines = {}
for w in words:
    y = round(w[1], 1)
    found = False
    for yk in lines:
        if abs(yk - y) < 2.5:
            lines[yk].append(w)
            found = True
            break
    if not found:
        lines[y] = [w]

rows = []
for yk in sorted(lines.keys()):
    if yk <= 140:
        continue
    row = sorted(lines[yk], key=lambda x: x[0])
    if len(row) > 0 and row[0][4].isdigit():
        sno = int(row[0][4])
        if 1 <= sno <= 36:
            # extract name, total, crit, oe
            name_words = [w[4] for w in row if 45 <= w[0] < 145]
            name = " ".join(name_words)
            tot = None
            safe = 0
            sc = 0
            crit = 0
            oe = 0
            sal = 0
            for w in row:
                x = w[0]
                try:
                    val = float(w[4])
                    if 145 <= x < 185:
                        tot = int(val)
                    elif 185 <= x < 230:
                        safe = int(val)
                    elif 270 <= x < 310:
                        sc = int(val)
                    elif 350 <= x < 390:
                        crit = int(val)
                    elif 430 <= x < 470:
                        oe = int(val)
                    elif 510 <= x < 550:
                        sal = int(val)
                except ValueError:
                    pass
            rows.append({
                'sno': sno,
                'name': name,
                'total_units': tot,
                'safe': safe,
                'sc': sc,
                'crit': crit,
                'oe': oe,
                'sal': sal
            })

df_units = pd.DataFrame(rows)

# Map to DC states
dc_states_names = [
    'Andhra Pradesh', 'Maharashtra', 'Tamil Nadu', 'Gujarat', 'Uttar Pradesh',
    'Madhya Pradesh', 'Telangana', 'Karnataka', 'West Bengal', 'Bihar',
    'Chhattisgarh', 'Delhi', 'Haryana', 'Odisha'
]

# Map SNOs of DC states
dc_snos = [1, 14, 23, 7, 26, 13, 24, 11, 28, 4, 5, 32, 8, 19]

print("=== ALL 36 ENTITIES UNITS FROM ANNEXURE III(A) ===")
print(f"{'SNo':<4} | {'State':<28} | {'Total':<6} | {'Safe':<5} | {'SC':<4} | {'Crit':<5} | {'OE':<5} | {'Sal':<4} | {'DC State'}")
print("-" * 85)
for idx, r in df_units.iterrows():
    is_dc = "Yes" if r['sno'] in dc_snos else "No"
    print(f"{r['sno']:<4} | {r['name']:<28} | {r['total_units']:<6} | {r['safe']:<5} | {r['sc']:<4} | {r['crit']:<5} | {r['oe']:<5} | {r['sal']:<4} | {is_dc}")

print("\n=== DC STATES SUB-TOTALS ===")
dc_df = df_units[df_units['sno'].isin(dc_snos)]
for idx, r in dc_df.iterrows():
    print(f"{r['name']:<25} | Total: {r['total_units']:<4} | Crit: {r['crit']:<3} | OE: {r['oe']:<4} | Crit+OE: {r['crit']+r['oe']}")

print("-" * 55)
print(f"DC States Sum -> Total: {dc_df['total_units'].sum()}, Crit: {dc_df['crit'].sum()}, OE: {dc_df['oe'].sum()}, Crit+OE: {dc_df['crit'].sum() + dc_df['oe'].sum()}")

print("\n=== NON-DC STATES SUB-TOTALS ===")
non_dc_df = df_units[~df_units['sno'].isin(dc_snos)]
print(f"Non-DC Sum -> Total: {non_dc_df['total_units'].sum()}, Crit: {non_dc_df['crit'].sum()}, OE: {non_dc_df['oe'].sum()}, Crit+OE: {non_dc_df['crit'].sum() + non_dc_df['oe'].sum()}")

print("\n=== GRAND TOTALS ===")
print(f"Grand Total -> Total: {df_units['total_units'].sum()}, Crit: {df_units['crit'].sum()}, OE: {df_units['oe'].sum()}, Safe: {df_units['safe'].sum()}, SC: {df_units['sc'].sum()}, Sal: {df_units['sal'].sum()}")

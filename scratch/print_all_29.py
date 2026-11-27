with open(r'C:\Users\rajch\Desktop\files to upload\cgwb_2025_district_groundwater_29.tsv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    parts = line.strip().split('\t')
    if i == 0:
        print(f"{'State':<15} | {'District':<18} | {'Stage%':<8} | {'Category':<14} | {'PDF_Pg':<6} | {'Printed_Pg'}")
        print('-'*75)
    else:
        print(f"{parts[0]:<15} | {parts[1]:<18} | {parts[8]:<8} | {parts[9]:<14} | {parts[11]:<6} | {parts[12]}")

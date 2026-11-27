with open(r'C:\Users\rajch\Desktop\files to upload\cgwb_2025_district_groundwater_29.tsv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines[:15]:
    print(line.strip())

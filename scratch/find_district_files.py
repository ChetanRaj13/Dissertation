import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if any(k in f.lower() for k in ['district', 'groundwater', 'cgwb', 'annex']):
            print(os.path.join(root, f))

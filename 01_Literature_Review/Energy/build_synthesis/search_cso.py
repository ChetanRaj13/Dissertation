import fitz

doc = fitz.open('Data Centres Metered Electricity Consumption 2025 (Central Statistics Office Ireland).pdf')
print("=== CSO Ireland MEC02 ===")
print(doc[0].get_text())

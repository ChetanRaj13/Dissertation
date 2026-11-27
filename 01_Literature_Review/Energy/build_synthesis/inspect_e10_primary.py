import fitz

doc_cru25 = fitz.open('CRU-2025-236 Large Energy User connection policy decision paper.pdf')
print("CRU 2025 pages:", len(doc_cru25))

doc_cru21 = fitz.open('CRU-21-124 Direction to the System Operators related to Data Centre grid connection.pdf')
print("CRU 2021 pages:", len(doc_cru21))

doc_mop = fitz.open('Ministry of Power - Rajya Sabha Question 956 (26.3 GW Data Centre Projections).pdf')
print("MoP RS Q956 pages:", len(doc_mop))

doc_cso = fitz.open('Data Centres Metered Electricity Consumption 2025 (Central Statistics Office Ireland).pdf')
print("CSO Ireland pages:", len(doc_cso))

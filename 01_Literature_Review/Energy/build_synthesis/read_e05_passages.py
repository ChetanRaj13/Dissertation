import fitz

doc = fitz.open('The carbon and water footprints of data centers and what this could mean for artificial intelligence.pdf')

pages_to_check = [1, 2, 3, 4, 5, 7, 9, 10]
for p in pages_to_check:
    print(f"\n=================== PAGE {p} ===================")
    print(doc[p-1].get_text()[:1800])

import fitz

doc = fitz.open("Data Centres and India's Power Grid - Technical Review of Grid Integration Challenges.pdf")

pages_to_check = [3, 5, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

for p in pages_to_check:
    txt = doc[p-1].get_text()
    print(f"\n=================== E09 PAGE {p} ===================")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    for l in lines[:10]:
        print("  *", l)

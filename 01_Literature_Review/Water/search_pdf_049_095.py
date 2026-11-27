import fitz

doc_p03 = fitz.open('Making AI Less Thirsty - Uncovering and Addressing the Secret Water Footprint of AI Models.pdf')
for pno in range(len(doc_p03)):
    txt = doc_p03[pno].get_text()
    if '0.49' in txt:
        print(f"P03 p.{pno+1} has 0.49: {txt[:300]}")

doc_p06 = fitz.open('Estimating data center water use - Best practices and critical questions.pdf')
for pno in range(len(doc_p06)):
    txt = doc_p06[pno].get_text()
    if '0.95' in txt:
        print(f"P06 p.{pno+1} has 0.95")

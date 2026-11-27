import fitz

doc_e13 = fitz.open("Dominion Energy admits it cannot meet data center power demands in Virginia (Data Center Dynamics).pdf")
for p in range(len(doc_e13)):
    t = doc_e13[p].get_text()
    if 'tapley' in t.lower() or 'transmission' in t.lower() or 'generation' in t.lower():
        print(f"Found match in E13 page {p+1}!")
        pos = t.lower().find('transmission')
        print(repr(t[pos-30:pos+150]))

doc_e15 = fitz.open("Every Data Center in Virginia - Operating, Under Construction and Planned (Inside the DataCenter).pdf")
p2 = doc_e15[1].get_text()
pos = p2.find('233')
print("\nE15 around 233:")
print(repr(p2[pos-50:pos+100]))

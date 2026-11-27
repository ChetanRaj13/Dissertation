with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

pos = js_text.find("function StateWiseFHTCTap")
if pos != -1:
    print(js_text[pos+1000:pos+3000])

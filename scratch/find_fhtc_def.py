with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

pos = js_text.find("StateWiseFHTCTap = function")
if pos != -1:
    print(js_text[pos:pos+1500])
else:
    pos2 = js_text.find("function StateWiseFHTCTap")
    if pos2 != -1:
        print(js_text[pos2:pos2+1500])
    else:
        print("Not found with '=' or 'function'")

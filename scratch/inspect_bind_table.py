with open('scratch/JJM_Dashboard.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

pos = js_text.find("url: PageName + '.aspx/Bind_table_graph'")
if pos != -1:
    print(js_text[pos:pos+1500])

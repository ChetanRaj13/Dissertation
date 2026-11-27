import openpyxl

wb = openpyxl.load_workbook('water_datacentre_literature_synthesis_v1.xlsx', data_only=True)
ws = wb['Link_to_My_Dataset']
print("G11:", ws.cell(11, 7).value)

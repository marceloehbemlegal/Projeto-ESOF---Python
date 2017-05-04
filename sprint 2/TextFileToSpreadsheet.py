import openpyxl


wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()

for i in range(11):
    file = open('spreadsheetToText_%03d.txt' % (i+1), 'r')
    lines = file.readlines()
    for j in range(len(lines)):
        sheet.cell(row=j+1, column=i+1).value = lines[j]

wb.save('textToSpreadsheet.xlsx')

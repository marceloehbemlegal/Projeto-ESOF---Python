import openpyxl


wb = openpyxl.load_workbook('multiplication_table.xlsx')
sheet = wb.get_active_sheet()

for column in range(1, sheet.max_column+1):
    file = open('spreadsheetToText_%03d.txt' % column, 'w')
    for row in range(1, sheet.max_row+1):
        if sheet.cell(row=row, column=column).value == None:
            file.write('\n')
        else:
            file.write(str(sheet.cell(row=row, column=column).value)+'\n')
    file.close()

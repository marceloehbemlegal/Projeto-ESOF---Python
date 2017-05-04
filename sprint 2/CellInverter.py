import openpyxl


wb = openpyxl.load_workbook('blank_rows.xlsx')
sheet = wb.get_active_sheet()

wbInverted = openpyxl.Workbook()
sheetInverted = wbInverted.get_active_sheet()

sheetList = []

for row in range(1, sheet.max_row+1):
    rowList = []
    for column in range(1, sheet.max_column+1):
        rowList.append(sheet.cell(row=row, column=column).value)
    sheetList.append(rowList)

for row in range(1, sheet.max_column+1):
    for column in range(1, sheet.max_row+1):
        sheetInverted.cell(row=row, column=column).value = sheetList[column-1][row-1]

wbInverted.save('inverted_cells.xlsx')

import openpyxl


wb = openpyxl.load_workbook('multiplication_table.xlsx')
wbWithBlankRow = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheetBlankRow = wbWithBlankRow.get_active_sheet()

N = int(input())
M = int(input())

rowBlank = 1

for row in range(1, 200+M):
    if row == N:
        rowBlank += M
    for column in range(1, 200):
        sheetBlankRow.cell(row=rowBlank, column=column).value = sheet.cell(row=row, column=column).value
    rowBlank += 1

wbWithBlankRow.save('blank_rows.xlsx')
#! python3
# TextFileToSpreadsheet.py - Reads several files and prints the content of the lines into the rows of a column for each one


import openpyxl


wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()

for i in range(11):
    file = open('spreadsheetToText_%03d.txt' % (i+1), 'r')
    lines = file.readlines() # 'lines' -> list in which each elements is a line from the file read
    for j in range(len(lines)):
        sheet.cell(row=j+1, column=i+1).value = lines[j] # prints each line into each row

wb.save('textToSpreadsheet.xlsx')

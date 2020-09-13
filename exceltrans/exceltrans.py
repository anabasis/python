#!/usr/bin/env python

# pip install virtualenv
# virtualenv exceltrans
# \exceltrans\Scripts\activate
# python -m pip install --upgrade pip
# pip install xlsxwriter
# pip install openpyxl


# Openpyxl <https://doitnow-man.tistory.com/159>

from openpyxl import load_workbook

def xlsx_read(filename):

    wb = load_workbook(filename)
    sheet_names = wb.sheetnames
    print(sheet_names)

    for sheet_name in sheet_names:
        print(sheet_name)

        sheet_xlsx = wb[sheet_name]

        print(sheet_xlsx.max_row)
        print(sheet_xlsx.max_column)

        for row in range(1, sheet_xlsx.max_row):
            for col in range(1, sheet_xlsx.max_column):
                print(sheet_xlsx.cell(row,col).value)

    wb.close()
    return print(sheet_names)

def xlsx_sheet_read(filename, sheetname='Sheet1'):
    wb = load_workbook(filename)
    sheet_xlsx = wb[sheetname]

    print(sheet_xlsx.max_row)
    print(sheet_xlsx.max_column)

    for row in range(1, sheet_xlsx.max_row):
        for col in range(1, sheet_xlsx.max_column):
            print(sheet_xlsx.cell(row,col).value)

    wb.close()
    return print(sheetname)

def xlsx_sheet_trans(filename, sheetname='Sheet1', key='A', fields=[]):
    wb = load_workbook(filename)
    sheet_xlsx = wb[sheetname]

    print('## SIZE  ##########################################################')
    print(sheet_xlsx.max_row)
    print(sheet_xlsx.max_column)
    print('###################################################################')

    for row in range(1, sheet_xlsx.max_row):

        if sheet_xlsx.cell(row,col) == None :
            break

        for col in range(1, sheet_xlsx.max_column):
            print(sheet_xlsx.cell(row,col).value)
        print('###################################################################')

    wb.close()
    return print(sheetname)

    return ''

def xlsx_writer(data):
    print(data)
    # write stuff to database or something...

if __name__ == "__main__":
    #xlsx_read('.\\data\\ES_시나리오_한글_20200910.xlsx')
    xlsx_sheet_trans('.\\data\\ES_시나리오_한글_20200910.xlsx','ANALYTICS','B',['B','F','G','P'])

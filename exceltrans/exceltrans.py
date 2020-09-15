#!/usr/bin/env python

# pip install virtualenv
# virtualenv exceltrans
# \exceltrans\Scripts\activate
# python -m pip install --upgrade pip
# pip install xlsxwriter
# pip install openpyxl
# pip install pandas

# Openpyxl <https://doitnow-man.tistory.com/159>

from openpyxl import load_workbook
from openpyxl import Workbook
from itertools import islice
import numpy as np
import pandas as pd

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

def xlsx_sheet_trans(filename, cellrange, sheetname='Sheet1', key='A', fields=[]):
    wb = load_workbook(filename)
    sheet_xlsx = wb[sheetname]

    print('## SIZE  ##' + '#'*18)
    print(sheet_xlsx.max_row)
    print(sheet_xlsx.max_column)
    print('#'*25)

    data = iter(sheet_xlsx[cellrange])

    cols = [i.value for i in next(data)[1:]]
    print(cols)

    idx = [i.value for i in [r[0] for r in list(data)]]
    print(idx)

    data = (islice(r, 1, None) for r in data)


    df = pd.DataFrame(data, index=idx, columns=cols)


    #
    # # Trim()
    # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # print(df)

    # cell_range = sheet['A1':'C2']# 특정 범위
    # row10 = sheet[10]# 특정 row
    # row_range = sheet[5:10]# 특정 row 범위
    # colC = sheet['C']# 특정 Column
    # col_range = sheet['C:D']# 특정 Column 범위

    #for row in range(1, sheet_xlsx.max_row):
    # for row in range(1, 5):
    #     #print(row + " : " + sheet_xlsx[row])
    #     print("{0} : {1}".format(row,sheet_xlsx[row]))
    #     for col in range(1, sheet_xlsx.max_column):
    #         print(sheet_xlsx.cell(row,col).value)
    #     print('-'*20)

    wb.close()
    return print(sheetname)

    return ''




def xlsx_writer(data):
    print(data)
    # write stuff to database or something...

if __name__ == "__main__":
    #xlsx_read('.\\data\\ES_시나리오_한글_20200910.xlsx')
    xlsx_sheet_trans('.\\data\\ES_시나리오_한글_20200910.xlsx','A2:AU493','ANALYTICS','B',['B','F','G','P'])
    #xlsx_sheet_trans('.\\data\\ES_시나리오_한글_20200910.xlsx','A2:G8','ANALYTICS','B',['B','F','G','P'])

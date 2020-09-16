#!/usr/bin/env python

# pip install virtualenv
# virtualenv exceltrans
# \exceltrans\Scripts\activate
# python -m pip install --upgrade pip
# pip install xlsxwriter
# pip install openpyxl
# pip install pandas

# Openpyxl <https://doitnow-man.tistory.com/159>
# Pandas <https://www.delftstack.com/ko/howto/python-pandas/how-to-add-new-column-to-existing-dataframe-in-python-pandas/>

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

def xlsx_sheet_trans(filename, sheetname='Sheet1', cellrange=[]):

    total_df = pd.DataFrame()

    wb = load_workbook(filename)
    sheet_xlsx = wb[sheetname]

    print('## SIZE  ##' + '#'*18)
    print(sheet_xlsx.max_row)
    print(sheet_xlsx.max_column)
    print('#'*25)

    for field in cellrange :

        data = sheet_xlsx[field] # tuple
        fields = [ [ col.value for col in row] for row in data[:1]]
        contents = [ [ col.value for col in row] for row in data[1:]]
        #total_df = pd.DataFrame(contents, columns=fields)
        #total_df.insert(df)
        #total_df = total_df.assign(fields = contents)
        total_df.loc[:,fields] = contents
        #print(df)

    wb.close()
    return total_df


def xlsx_writer(data):
    print(data)
    # write stuff to database or something...

if __name__ == "__main__":
    #xlsx_read('.\\data\\ES_시나리오_한글_20200910.xlsx')
    #xlsx_sheet_trans('.\\data\\ES_시나리오_한글_20200910.xlsx','ANALYTICS',['B2:B493','F2:G493','P2:P493'])
    main_df = xlsx_sheet_trans('.\\data\\ES_시나리오_한글_20200910.xlsx','ANALYTICS',['B2:B493','F2:G493','P2:P493'])
    print(main_df)

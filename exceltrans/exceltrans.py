#!/usr/bin/env python

# pip install xlsxwriter
# pip install openpyxl

from openpyxl import load_workbook

def xlsx_read(filename):
    wb2 = load_workbook(filename)
    print(wb2.sheetnames)

def xlsx_writer(data):
    print(data)
    # write stuff to database or something...

if __name__ == "__main__":

    xlsx_read('E:\\ATOM_WORK\\python\\exceltrans\\data\\ES_시나리오_한글_20200910.xlsx')

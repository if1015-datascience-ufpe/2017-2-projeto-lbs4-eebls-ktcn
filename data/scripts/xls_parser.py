#!/usr/bin/python
# -*- coding:utf-8 -*-
import xlrd
import unicodedata
import pprint
import csv
import os

path_to_xls = '/home/joaoluiz/Documents/Cadeiras/TAIA/project/2017-2-projeto-lbs4-eebls-ktcn/data/censo_2000_pe/indicadores_sociais_pe/xls/tab04.xls'
folder = '/home/joaoluiz/Documents/Cadeiras/TAIA/project/2017-2-projeto-lbs4-eebls-ktcn/data/censo_2000_pe/indicadores_sociais_pe/csv/'
multi = False
START_ROW_NUMBER = 2
END_ROW_NUMBER = 5
START_ROW = 14
TITLE = 'domicilios_particulares_permanentes'
book = xlrd.open_workbook(path_to_xls)
sheet = book.sheet_by_index(0)

final_column_topics = []
lines = []
found = False

ROW_SIZE = len(sheet.row(0))

for e in range(START_ROW_NUMBER, END_ROW_NUMBER):
    line_vector = []
    save_value = ''
    for k in range(ROW_SIZE):
        cell_value = unicodedata.normalize('NFKD', sheet.row(e)[k].value).encode('ascii', 'ignore')
        # print sheet.cell(2, 6), "@@@@@@@@@@@"
        # print cell_value
        print k
        if cell_value:
            if k == 0:
                if found:
                    pass
                else:
                    found = True
                    save_value = 'municipio'
                    line_vector.append(save_value)
            elif 'Unidade' in cell_value:
                save_value = 'codigo'
                line_vector.append(save_value)
            else:
                save_value = '_'.join(cell_value.lower().split())
                print save_value
                # if k == 1 and e == 2:
                #     print save_value
                #     TITLE = save_value
                line_vector.append(save_value)
        else:
            if k == ROW_SIZE/2 and multi:
                pass
            elif k == ROW_SIZE-1:
                # save_value = ''
                line_vector.append(save_value)
            else:
                line_vector.append(save_value)
        # print "Element: ", k, save_value, sheet.row(e)[k].value
    print
    lines.append(line_vector)
pprint.pprint(lines)


def get_col_names(lines):
    print zip(*lines)
    a = [{i: str('_'.join(x)).strip('_')} for i, x in enumerate(list(zip(*lines)))]
    return a

a = get_col_names(lines)
print a
new_columns = []
for i, l in enumerate(a):
    if multi:
        if i < ROW_SIZE/2:
            # print i, l[i], sheet.col(i+1)
            column = sheet.col(i)
            new_columns.append({'title': l[i], 'column': column[START_ROW:]})
        elif i >= ROW_SIZE/2:
            # print i, l[i], sheet.col(i+1)
            column = sheet.col(i+1)
            new_columns.append({'title': l[i], 'column': column[START_ROW:]})
    else:
        column = sheet.col(i)
        new_columns.append({'title': l[i], 'column': column[START_ROW:]})


def convert_data(row):
    aux_row = []
    for cell in row:
        if isinstance(cell.value, unicode):
            cell_value = unicodedata.normalize('NFKD', cell.value).encode('ascii', 'ignore')
            aux_row.append(cell_value)
        else:
            aux_row.append(cell.value)
    return aux_row

dir = folder + TITLE + ".csv"
with open(dir, 'wb') as csvfile:
    first_row = []
    columns = []
    for col in new_columns:
        first_row.append(col.get('title'))
        columns.append(col.get('column'))

    # pprint.pprint(columns)
    # print first_row
    rows = zip(*columns)
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(first_row)
    for r in rows:
        row = convert_data(r)
        # print row
        spamwriter.writerow(row)


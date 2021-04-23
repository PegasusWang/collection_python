#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1.用xlwings打开工作簿
import xlwings as xw

app = xw.App(visible=True, add_book=False)
workbook = app.books.open(r'data.xlsx')
sheet = workbook.sheets[0]  # 选中第一个表格
# 2.循环每行的数据
info = sheet.used_range
#nrows = info.last_cell.row
#ncols = info.last_cell.column
list_cell = ['B1', 'D1', 'F1', 'H1', 'B2', 'D2', 'F2', 'H2']
for i in info.raw_value[1:]:
    print(i)
    app = xw.App(visible=True, add_book=False)
    workbook = app.books.open(r'template.xlsx')
    sheet = workbook.sheets[0]
    sheet['B1'].value = i[0]
    sheet['D1'].value = i[1]
    sheet['F1'].value = i[8]
    sheet['H1'].value = i[2]
    sheet['B2'].value = i[9]
    sheet['D2'].value = i[5]
    sheet['F2'].value = i[6]
    sheet['H2'].value = i[7]
    # 4.设置单元格格式
    for j in list_cell:
        sheet[j].api.Font.Name = '楷体'  # 设置字体
        sheet[j].api.Font.Size = 14  # 设置字号
        # 设置文本水平对齐方式为居中
        sheet[j].expand('table').api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
        # 设置文本水平对齐方式为居中
        sheet[j].expand('table').api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter
    workbook.save(r'data\{}.xlsx'.format(i[0]))  # 以名字命名
    workbook.close()
    app.quit()


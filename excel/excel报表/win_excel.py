import time
import pathlib
import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv(r"fruit_and_veg_sales.csv")
print(df)

# 创建原始数据表并复制数据
wb = xw.Book()
sht = wb.sheets["Sheet1"]
sht.name = "fruit_and_veg_sales"
sht.range("A1").options(index=False).value = df

# 查看所有列名
print(df.columns)

# 总利润透视表
pv_total_profit = pd.pivot_table(df, index='类别', values='总利润(美元)', aggfunc='sum')
print(pv_total_profit)

# 销售数量透视表
pv_quantity_sold = pd.pivot_table(df, index='类别', values='销售数量', aggfunc='sum')
print(pv_quantity_sold)

# 查看每列的数据类型
print(df.dtypes)
df["销售日期"] = pd.to_datetime(df["销售日期"])

# 每日的数据情况
gb_date_sold = df.groupby(
    df["销售日期"].dt.to_period('m')).sum()[["销售数量", '总收入(美元)', '总成本(美元)', "总利润(美元)"]]
gb_date_sold.index = gb_date_sold.index.to_series().astype(str)
print(gb_date_sold)

# 总收入前8的日期数据
gb_top_revenue = (df.groupby(df["销售日期"]).sum().sort_values(
    '总收入(美元)', ascending=False).head(8))[["销售数量", '总收入(美元)', '总成本(美元)', "总利润(美元)"]]
print(gb_top_revenue)

# 创建展示表
wb.sheets.add('Dashboard')
sht_dashboard = wb.sheets('Dashboard')

# 设置背景颜色, 从A1单元格到Z1000单元格的矩形区域
sht_dashboard.range('A1:Z1000').color = (198, 224, 180)

# A、B列的列宽
sht_dashboard.range('A:B').column_width = 2.22

# B2单元格, 文字内容、字体、字号、粗体、颜色、行高(主标题)
sht_dashboard.range('B2').value = '销售数据报表'
sht_dashboard.range('B2').api.Font.Name = '黑体'
sht_dashboard.range('B2').api.Font.Size = 48
sht_dashboard.range('B2').api.Font.Bold = True
sht_dashboard.range('B2').api.Font.Color = 0x000000
sht_dashboard.range('B2').row_height = 61.2

# B2单元格到W2单元格的矩形区域, 下边框的粗细及颜色
sht_dashboard.range('B2:W2').api.Borders(9).Weight = 4
sht_dashboard.range('B2:W2').api.Borders(9).Color = 0x00B050

# 不同产品总的收益情况图表名称、字体、字号、粗体、颜色(副标题)
sht_dashboard.range('M2').value = '每种产品的收益情况'
sht_dashboard.range('M2').api.Font.Name = '黑体'
sht_dashboard.range('M2').api.Font.Size = 20
sht_dashboard.range('M2').api.Font.Bold = True
sht_dashboard.range('M2').api.Font.Color = 0x000000

# 主标题和副标题的分割线, 粗细、颜色、线型
sht_dashboard.range('L2').api.Borders(7).Weight = 3
sht_dashboard.range('L2').api.Borders(7).Color = 0x00B050
sht_dashboard.range('L2').api.Borders(7).LineStyle = -4115


# 表格生成函数.
def create_formatted_summary(header_cell, title, df_summary, color):
    """
    Parameters
    ----------
    header_cell : Str
        左上角单元格位置, 放置数据

    title : Str
        当前表格的标题

    df_summary : DataFrame
        表格的数据

    color : Str
        表格填充色
    """

    # 可选择的表格填充色
    colors = {
        "purple": [(112, 48, 160), (161, 98, 208)],
        "blue": [(0, 112, 192), (155, 194, 230)],
        "green": [(0, 176, 80), (169, 208, 142)],
        "yellow": [(255, 192, 0), (255, 217, 102)]
    }

    # 设置表格标题的列宽
    sht_dashboard.range(header_cell).column_width = 1.5

    # 获取单元格的行列数
    row, col = sht_dashboard.range(header_cell).row, sht_dashboard.range(header_cell).column

    # 设置表格的标题及相关信息, 如：字号、行高、向左居中对齐、颜色、粗体、表格的背景颜色等
    summary_title_range = sht_dashboard.range(row, col)
    summary_title_range.value = title
    summary_title_range.api.Font.Size = 14
    summary_title_range.row_height = 32.5
    # 垂直对齐方式
    summary_title_range.api.VerticalAlignment = xw.constants.HAlign.xlHAlignCenter
    summary_title_range.api.Font.Color = 0xFFFFFF
    summary_title_range.api.Font.Bold = True
    sht_dashboard.range(
        (row, col),
        (row, col + len(df_summary.columns) + 1)).color = colors[color][0]  # Darker color

    # 设置表格内容、起始单元格、数据填充、字体大小、粗体、颜色填充
    summary_header_range = sht_dashboard.range(row + 1, col + 1)
    summary_header_range.value = df_summary
    summary_header_range = summary_header_range.expand('right')
    summary_header_range.api.Font.Size = 11
    summary_header_range.api.Font.Bold = True
    sht_dashboard.range(
        (row + 1, col),
        (row + 1, col + len(df_summary.columns) + 1)).color = colors[color][1]  # Darker color
    sht_dashboard.range((row + 1, col + 1),
                        (row + len(df_summary), col + len(df_summary.columns) + 1)).autofit()

    for num in range(1, len(df_summary) + 2, 2):
        sht_dashboard.range((row + num, col),
                            (row + num, col + len(df_summary.columns) + 1)).color = colors[color][1]

    # 找到表格的最后一行
    last_row = sht_dashboard.range(row + 1, col + 1).expand('down').last_cell.row
    side_border_range = sht_dashboard.range((row + 1, col), (last_row, col))

    # 给表格左边添加带颜色的边框
    sht_dashboard.range(side_border_range).api.Borders(7).Weight = 3
    sht_dashboard.range(side_border_range).api.Borders(7).Color = xw.utils.rgb_to_int(
        colors[color][1])
    sht_dashboard.range(side_border_range).api.Borders(7).LineStyle = -4115


# 生成4个表格
create_formatted_summary('B5', '每种产品的收益情况', pv_total_profit, 'green')
create_formatted_summary('B17', '每种产品的售出情况', pv_quantity_sold, 'purple')
create_formatted_summary('F17', '每月的销售情况', gb_date_sold, 'blue')
create_formatted_summary('F5', '每日总收入排名Top8 ', gb_top_revenue, 'yellow')

# 中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']

# 使用Matplotlib绘制可视化图表, 饼图
fig, ax = plt.subplots(figsize=(6, 3))
pv_total_profit.plot(color='g', kind='bar', ax=ax)

# 添加图表到Excel
sht_dashboard.pictures.add(fig,
                           name='ItemsChart',
                           left=sht_dashboard.range("M5").left,
                           top=sht_dashboard.range("M5").top,
                           update=True)
time.sleep(3)
# 添加logo到Excel
logo = sht_dashboard.pictures.add(image=f"{pathlib.Path.cwd()}/pie_logo.png",
                                  name='PC_3',
                                  left=sht_dashboard.range("J2").left,
                                  top=sht_dashboard.range("J2").top + 5,
                                  update=True)

# 设置logo的大小
logo.width = 54
logo.height = 54
time.sleep(3)
# 保存Excel文件
wb.save(rf"水果蔬菜销售报表.xlsx")
wb.close()

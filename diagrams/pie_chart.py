import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

"""
pip3 install seaborn
pip3 install matplotlib

解决 mac matplotlib 不展示中文的问题：(问的 deepseek) 。但是好像对 seaborn 还是不行

import matplotlib.font_manager as fm
[f.name for f in fm.fontManager.ttflist if 'PingFang' in f.name]  # 检查字体是否加载

我的mac 返回了  ['PingFang HK']

删除字体缓存：
rm -rf ~/.matplotlib/fontlist-*.json

代码里使用：

plt.rcParams['font.sans-serif'] = ['PingFang HK']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
"""


result = """
无surl请求: 4887
归因类型不一致: 3913
{"duanju_reverse":"命中业务短剧反转"}: 630
{"click_info":"长短链触点都为空"}: 127
归因为自然量等: 71
{"ab_info":"命中穿山甲商店点位离线表实验不返回触点: https://bytedance.larkoffice.com/docx/Ajmsd3chLowC4fxrmdHcqTDxnUg"}: 39
触点超过24h(ios 36h)窗口期失效: 33
{"undertake_reverse":"命中承接策略大反转"}: 12
{"book_info":"书籍信息获取失败(下架或者书城不可见)"}: 6
{"cold_start_type":"未能识别的operation类型或者没有命中短剧冷启归因实验"}: 3
"""


# 指定中文字体（例如使用苹果的 PingFang SC）
plt.rcParams['font.sans-serif'] = ['PingFang HK']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def get_lables_and_numbers():
    ll = result.split('\n')
    ll = [l for l in ll if l]
    labels = []
    numbers = []
    for line in ll:
        label, num = line.rsplit(maxsplit=1)
        labels.append(label)
        numbers.append(int(num))

    return labels, numbers


def draw_pie_chart(labels, data):
    # labels = [f'Part {i + 1}' for i in range(len(data))]
    # sns.set_style("whitegrid") # 被设置这行，好像中文不生效
    _, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.set_title('Proportion Chart')
    plt.show()



if __name__ == "__main__":
    # numbers = [15, 30, 45, 10]
    # draw_pie_chart(numbers)
    # print(get_lables_and_numbers())

    labels, nums = get_lables_and_numbers()
    draw_pie_chart(labels, nums)

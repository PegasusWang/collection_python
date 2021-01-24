# -*- coding: utf-8 -*-

"""
抓取蛋卷基金数据。主要是为了导出我关注的一些优秀主动基金的季度重仓股

pip3 install requests
pip3 install SQLAlchemy -i https://pypi.doubanio.com/simple --user
pip3 install pymysql -i https://pypi.doubanio.com/simple --user

# https://github.com/numpy/numpy/issues/15947 numpy 版本高有问题
pip3 install numpy==1.18.0 -i https://pypi.doubanio.com/simple
pip3 install pandas -i https://pypi.doubanio.com/simple
pip3 install openpyxl -i https://pypi.doubanio.com/simple

"""

import collections
import json
import random
import time

import pandas as pd
import requests
import sqlalchemy as db

"""
curl 'https://danjuanfunds.com/djapi/fund/detail/005827' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36' \
  -H 'elastic-apm-traceparent: 00-8936c0d09ef99045716fac06ff3777a0-3df470af2db9906a-01' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://danjuanfunds.com/funding/005827?channel=1300100141' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Cookie: device_id=web_SkS2df508; _ga=GA1.2.1397406205.1593612461; gr_user_id=2ac24d8b-927e-475d-8f29-27589058f70f; channel=1300100141; xq_a_token=d79103ea23560cd344415ed151659059a3397776; Hm_lvt_d8a99640d3ba3fdec41370651ce9b2ac=1609645857; acw_tc=2760776e16113729412211916e762552b2c598aae61864775cda6af8bb016f; Hm_lpvt_d8a99640d3ba3fdec41370651ce9b2ac=1611373570; timestamp=1611373569899' \
  --compressed

requests.get("https://danjuanfunds.com/djapi/fund/detail/005827",
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Referer": "https://danjuanfunds.com/funding/005827?channel=1300100141",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "elastic-apm-traceparent": "00-8936c0d09ef99045716fac06ff3777a0-3df470af2db9906a-01"
    },
    cookies={
        "Hm_lpvt_d8a99640d3ba3fdec41370651ce9b2ac": "1611373570",
        "Hm_lvt_d8a99640d3ba3fdec41370651ce9b2ac": "1609645857",
        "_ga": "GA1.2.1397406205.1593612461",
        "acw_tc": "2760776e16113729412211916e762552b2c598aae61864775cda6af8bb016f",
        "channel": "1300100141",
        "device_id": "web_SkS2df508",
        "gr_user_id": "2ac24d8b-927e-475d-8f29-27589058f70f",
        "timestamp": "1611373569899",
        "xq_a_token": "d79103ea23560cd344415ed151659059a3397776"
    },
)
"""


def get_fund_json(fund_code, fund_name="", to_file=False):
    """抓取蛋卷基金数据"""
    url = "https://danjuanfunds.com/djapi/fund/detail/{}".format(fund_code)
    print("抓取:{} {}".format(fund_code, fund_name))
    resp = requests.get(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://danjuanfunds.com/funding/005827?channel=1300100141",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "elastic-apm-traceparent": "00-8936c0d09ef99045716fac06ff3777a0-3df470af2db9906a-01",
        },
        cookies={
            "Hm_lpvt_d8a99640d3ba3fdec41370651ce9b2ac": "1611373570",
            "Hm_lvt_d8a99640d3ba3fdec41370651ce9b2ac": "1609645857",
            "_ga": "GA1.2.1397406205.1593612461",
            "acw_tc": "2760776e16113729412211916e762552b2c598aae61864775cda6af8bb016f",
            "channel": "1300100141",
            "device_id": "web_SkS2df508",
            "gr_user_id": "2ac24d8b-927e-475d-8f29-27589058f70f",
            "timestamp": "1611373569899",
            "xq_a_token": "d79103ea23560cd344415ed151659059a3397776",
        },
    )
    jsontext = resp.text  # 重定向到 json 文件可以格式化查看

    if to_file:  # 写到本地 json 文件方便调试
        filename = "./{}.json".format(fund_code)
        with open(filename, "w") as f:
            json.dump(resp.json(), f, indent=2, ensure_ascii=False)

    return jsontext


Connection = None
Table = None
TableName = "danjuan_fund_2020_4"  # 2020 四季度基金


def init_conn():
    global Connection, Table  # 全局使用
    url = "mysql+pymysql://root:wnnwnn@127.0.0.1:3306/testdb"  # 测试地址，改成你的本地 mysql 数据库地址
    engine = db.create_engine(url)
    metadata = db.MetaData()
    Connection = engine.connect()
    Table = db.Table(TableName, metadata, autoload=True, autoload_with=engine)


def fund_name_from_manager_list(fund_code, achievement_list):
    """每个管理者都会管理很多基金，找到当前这个基金并返回名字"""
    for fund in achievement_list:
        if fund.get("fund_code") == fund_code:
            return fund["fundsname"]
    return ""


def get_managers(manager_list):
    """找到所有基金管理人返回空格分割字符串 eg: 李晓星 张坤"""
    name_list = []
    for manager in manager_list:
        name_list.append(manager["name"])
    return " ".join(name_list)


def parse_danjuan_fund(fund_code, json_text):
    d = json.loads(json_text)
    data = d["data"]
    manager_list = data["manager_list"]
    achievement_list = manager_list[0]["achievement_list"]  # 找到一个管理者

    fund_name = fund_name_from_manager_list(fund_code, achievement_list)
    managers = get_managers(manager_list)
    try:
        enddate = data["fund_position"]["enddate"]  # 季报披露日期
    except KeyError:
        enddate = ""
    return fund_name, managers, enddate


# 本地安装 mysql，并且在你的 mysql 创建这个表
"""
CREATE TABLE `danjuan_fund_2020_4` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `fund_name` varchar(64) DEFAULT '' COMMENT '基金名称',
    `fund_code` varchar(16) NOT NULL DEFAULT '' COMMENT '基金代码',
    `managers` varchar(32) NOT NULL DEFAULT '' COMMENT '管理人',
    `enddate` varchar(32) NOT NULL DEFAULT '' COMMENT '季报日期',
    `detail_json` text NOT NULL COMMENT '蛋卷基金详细信息 json',
    PRIMARY KEY (`id`),
    KEY `idx_code` (`fund_code`),
    KEY `idx_name` (`fund_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def save_mysql(fund_code, fund_name, managers, enddate, detail_json):
    query = db.insert(Table).values(
        fund_name=fund_name,
        fund_code=fund_code,
        managers=managers,
        enddate=enddate,
        detail_json=detail_json,
    )
    Connection.execute(query)


def request_and_save(fund_code, fund_name):
    json_text = get_fund_json(fund_code, fund_name)
    fund_name, managers, enddate = parse_danjuan_fund(fund_code, json_text)
    save_mysql(fund_code, fund_name, managers, enddate, json_text)


def get_my_xueqiu_fund_codes():
    """从我的雪球获取我关注的所有基金代码
    https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&pid=-110&category=2
    """
    codes = []  # [ (code, name) ]
    with open("./funds.json") as f:
        res = json.load(f)
        stocks = res["data"]["stocks"]
        for stock in stocks:
            symbol = stock["symbol"]
            fund_code = "".join(char for char in symbol if char.isdigit())
            fund_name = stock["name"]
            codes.append((fund_code, fund_name))
    return codes


def crawl_all_my_funds_to_mysql():
    funds = get_my_xueqiu_fund_codes()
    __import__("pprint").pprint(funds)

    for fund_code, fund_name in funds:
        request_and_save(fund_code, fund_name)
        time.sleep(random.randint(5, 10))  # 慢一点，防止反作弊命中


def export_all_mysql_funds_stocks_to_dict():
    """导出所有基金的股票前十大重仓股票到 excel"""
    query = db.select([Table]).order_by(db.desc(Table.columns.id)).limit(100)
    rows = Connection.execute(query).fetchall()
    fund_dict = {}
    for row in rows:
        d = json.loads(row.detail_json)
        try:
            stock_percent = d["data"]["fund_position"]["stock_percent"]  # 股票比
            stock_list = d["data"]["fund_position"]["stock_list"]
        except KeyError:  # 新基金没披露可能为空
            stock_list = []
            stock_percent = 0

        stocks = []
        for stock in stock_list:
            name, code, percent = stock["name"], stock["code"], stock["percent"]
            stock_fmt = u"{}[{}]({}%)".format(name, code, percent)
            stocks.append(stock_fmt)

        if len(stocks) < 10:
            stocks += (10 - len(stocks)) * [""]

        key = row.fund_name
        vals = [row.fund_code, row.managers, row.enddate, stock_percent] + stocks
        fund_dict[key] = vals

    return fund_dict


# https://www.geeksforgeeks.org/how-to-create-dataframe-from-dictionary-in-python-pandas/
def export_all_mysql_funds_stocks_to_excel_vertical():
    fund_dict = export_all_mysql_funds_stocks_to_dict()
    index = ["代码", "管理人", "季报日期", "股票仓位"] + ["重仓股"] * 10  # 十大重仓
    df = pd.DataFrame(fund_dict, index=index)
    df.to_excel("./funds_stock_vertical.xlsx")


def export_all_mysql_funds_stocks_to_excel():  # 横着
    fund_dict = export_all_mysql_funds_stocks_to_dict()
    df = pd.DataFrame.from_dict(fund_dict, orient="index")
    df.to_excel("./fund_stock.xlsx")


def export_all_stock_funds():
    """导出每个股票被多少基金持有，比较容易看出哪些股票被抱团"""
    query = db.select([Table]).order_by(db.desc(Table.columns.id)).limit(100)
    rows = Connection.execute(query).fetchall()
    stock_funds = collections.defaultdict(list)
    for row in rows:
        d = json.loads(row.detail_json)
        try:
            stock_list = d["data"]["fund_position"]["stock_list"]
        except KeyError:  # 新基金没披露可能为空
            stock_list = []

        for stock in stock_list:
            name, code, percent = stock["name"], stock["code"], stock["percent"]
            if len(code) == 5:  # 港股目前是 5 位数
                stock_name = u"{}({})[HK]".format(name, code)
            else:
                stock_name = u"{}({})".format(name, code)  # 股票名
            stock_funds[stock_name].append(row.fund_name)

    keys = sorted(stock_funds, key=lambda k: len(stock_funds[k]), reverse=True)
    sorted_stock_dict = {k: stock_funds[k] for k in keys}
    df = pd.DataFrame.from_dict(sorted_stock_dict, orient="index")
    df.to_excel("./stock.xlsx")


def main():
    crawl_all_my_funds_to_mysql()  # 抓取所有我关注的雪球上的基金到 mysql

    export_all_mysql_funds_stocks_to_excel_vertical()  # 导出基金十大重仓股
    export_all_mysql_funds_stocks_to_excel()  # 导出横版基金十大重仓

    export_all_stock_funds()  # 导出每个重仓股票分别被多少基金持有


if __name__ == "__main__":
    init_conn()
    main()

# -*- coding: utf-8 -*-

"""
sqlalchemy 快速读取 mysql 数据示例

pip install SQLAlchemy -i https://pypi.doubanio.com/simple --user
pip install pymysql -i https://pypi.doubanio.com/simple --user
"""

import sqlalchemy as db


def read_mysql():
    # https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
    url = "mysql+pymysql://user:pass@127.0.0.1:3306/dbname"
    engine = db.create_engine(url)
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('table_name', metadata, autoload=True, autoload_with=engine)

    query = db.select([table]).order_by(db.desc(table.columns.id)).limit(10)
    res = connection.execute(query)
    rows = res.fetchall()
    for row in rows:
        print(row.id)


"""
# 本机 mysql 创建一个测试表

CREATE TABLE `area_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` bigint(12) NOT NULL DEFAULT '0' COMMENT '行政区划代码',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '名称',
  PRIMARY KEY (`id`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

"""


def sqlalchemy_demo():
    # https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
    url = "mysql+pymysql://root:wnnwnn@127.0.0.1:3306/testdb"  # 测试地址
    engine = db.create_engine(url)
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('area_code', metadata, autoload=True, autoload_with=engine)

    # 插入单个数据
    query = db.insert(table).values(code=10010, name="北京")
    connection.execute(query)

    # 插入多个数据
    query = db.insert(table)
    values = [
        {'code': 10020, 'name': '上海'},
        {'code': 10030, 'name': '杭州'},
    ]
    connection.execute(query, values)

    # 查询
    query = db.select([table]).order_by(db.desc(table.columns.id)).limit(10)
    rows = connection.execute(query).fetchall()
    for row in rows:
        print(row.id, row.code, row.name)

    # 修改
    query = db.update(table).values(name="帝都").where(table.columns.code == 10010)
    connection.execute(query)

    # 删除行
    query = db.delete(table).where(table.columns.code == 10010)
    connection.execute(query)


if __name__ == "__main__":
    sqlalchemy_demo()

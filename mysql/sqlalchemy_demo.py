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

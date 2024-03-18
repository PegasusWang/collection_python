#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import json
import pymysql
from sqlalchemy import create_engine

# 打开数据库连接
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='xxxx',
                       charset='utf8'
                       )
engine = create_engine('mysql+pymysql://root:xxxx@localhost/mysql?charset=utf8')


def read_excel(file):
    df_excel = pd.read_excel(file)
    return df_excel


def read_json(file):
    with open(file, 'r') as json_f:
        df_json = pd.read_json(json_f)
        return df_json


def read_sql(table):
    sql_cmd = 'SELECT * FROM %s' % table
    df_sql = pd.read_sql(sql_cmd, engine)
    return df_sql


def read_csv(file):
    df_csv = pd.read_csv(file)
    return df_csv

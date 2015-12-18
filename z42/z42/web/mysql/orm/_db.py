#!/usr/bin/env python
#coding:utf-8
import _env
from z42 import config
from z42.web.mysql.sqlstore import Db


MYSQL_CONFIG = {
    config.MYSQL_DATABASE: {
        'master': '%s:%s:%s:%s:%s' % (config.MYSQL_HOST, config.MYSQL_PORT,
                                      config.MYSQL_DATABASE, config.MYSQL_USER, config.MYSQL_PASSWORD),
        'tables': '*',
    }
}

DB = Db(MYSQL_CONFIG)

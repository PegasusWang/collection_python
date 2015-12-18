#!/usr/bin/env python
# coding: utf-8
import _env
import os
from os.path import exists
from os.path import join,dirname
from os import makedirs
import subprocess
from datetime import datetime
from z42 import config

BACKUP_PATH = '/var/backup'
COMM_OPTION = ' -h%s -P%s -u%s -p%s %s '

def backup_data(prefix, appname, host, port, name, user, password):
    comm_option = COMM_OPTION % (host, port, user, password, name)

    """
    备份一个表数据的命令实例
    mysqldump --skip-opt --no-create-info 数据库名字 表名 --where="id<2000"
    """
    create_table_option = ' --no-create-info --quick --default-character-set=utf8 --skip-opt --hex-blob '+comm_option

    cmd = 'mysqldump ' + create_table_option
    with open(join(prefix, '%s.sql'%appname), 'w') as backfile:
        subprocess.Popen(
            cmd.split(),
            stdout=backfile
        )

def backup_table(prefix, appname, host, port, name, user, password):
    comm_option = COMM_OPTION % (host, port, user, password, name)

    """
    备份一个表数据的命令实例
    mysqldump --skip-opt --no-create-info 数据库名字 表名
    """
    create_table_option = '--skip-comments --no-data --default-character-set=utf8 --skip-opt --add-drop-table --create-options --quick --hex-blob ' + comm_option

    cmd = 'mysqldump ' + create_table_option
    with open(join(prefix, '%s.sql'%appname), 'w') as backfile:
        subprocess.Popen(
            cmd.split(),
            stdout=backfile
        )

def check_prefix(prefix):
    if not exists(prefix):
        makedirs(prefix, 0755)


if __name__ == '__main__':

    host = config.MYSQL_HOST
    port = config.MYSQL_PORT
    database = config.MYSQL_DATABASE
    user = config.MYSQL_USER
    password = config.MYSQL_PASSWORD
    #'%s/%s'%(BACKUP_PATH, str(datetime.now())[:-7].replace(' ','_').replace(':','_'))


    schema_prefix = dirname(__file__) 
    data_prefix = '%s/%s'%(BACKUP_PATH, 'data')

    check_prefix(data_prefix)

    backup_table(schema_prefix, database, host, port, database, user, password)
    backup_data(data_prefix, database, host, port, database, user, password)



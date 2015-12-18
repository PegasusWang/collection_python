#!/usr/bin/env python
# coding:utf-8
import _env
from array import array
from hashlib import md5
from z42.web.memcache import mc
from z42.web.mysql.orm.model import _key_by_table
from z42.web.mysql.orm._db import DB
__metaclass__ = type

class Kv(object):
    def __init__(self, table, NULL=''):
        self.__table__ = table
        db = DB.db(table)
        self.cursor = cursor = db.cursor()
        cursor.execute("select * from %s limit 1"%table)
        cursor.fetchone()
        mc_key = _key_by_table(db, table, cursor)
        self.__mc_id__ = "%s'+%%s"%mc_key
        self.NULL = NULL


    def get(self, id):
        mc_key = self.__mc_id__ % id
        r = mc.get(mc_key)
        if r is None:
            cursor = self.cursor
            cursor.execute(
                'select value from %s where id=%%s' % self.__table__, id)
            r = cursor.fetchone()
            if r:
                r = r[0]
            if r is None:
                r = self.NULL
            mc.set(mc_key, r)
        return r

    def get_dict(self, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = self.__mc_id__
        result = mc.get_dict([mc_key%i for i in id_list])
        r = {}
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = self.get(i)
            r[i] = t
        return r

    def get_list(self, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = self.__mc_id__
        result = mc.get_dict([mc_key%i for i in id_list])
        r = []
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                t = self.get(i)
            r.append(t)
        return r


    def iteritems(self, value=None):
        id = 0
        cursor = self.cursor
        while True:
            if value is None:
                cursor.execute('select id,value from %s where id>%%s order by id limit 128' % self.__table__, id)
            else:
                cursor.execute('select id,value from %s where id>%%s and value=%%s order by id limit 128' % self.__table__, (id, value))
            result = cursor.fetchall()
            if not result:
                break
            for id, value in result:
                yield id, value


    def set(self, id, value):
        r = self.get(id)
        if r != value:
            mc_key = self.__mc_id__ % id
            cursor = self.cursor
            table = self.__table__
            cursor.execute(
                'insert into %s (id,value) values (%%s,%%s) on duplicate key update value=values(value)' % table,
                (id, value)
            )
            cursor.connection.commit()
            if value is None:
                value = False
            mc.set(mc_key, value)

    def mc_flush(self, id):
        mc_key = self.__mc_id__ % id
        mc.delete(mc_key)

    def delete(self, id):
        cursor = self.cursor
        cursor.execute('delete from %s where id=%%s' % self.__table__, id)
        mc_key = self.__mc_id__ % id
        mc.delete(mc_key)


    def count(self, value=''):
        cursor = self.cursor
        if value:
            cursor.execute(
                'select count(0) from %s where value=%%s' % self.__table__,
                value
            )
        else:
            cursor.execute(
                'select count(0) from %s' % self.__table__
            )
        r = cursor.fetchone()
        if r:
            r = r[0]
        else:
            r = 0
        return r


    def id_by_value(self, value):
        cursor = self.cursor
        cursor.execute(
            'select id from %s where value=%%s limit 1' % self.__table__,
            value
        )
        r = cursor.fetchone()
        if r:
            r = r[0]
        else:
            r = 0
        return r

    def id_list_by_value(self, value):
        cursor = self.cursor
        cursor.execute(
            'select id from %s where value=%%s' % self.__table__,
            value
        )
        r = cursor.fetchall()

        return (s[0] for s in r)

    def id_list_by_name_value(self, name, value, offset=0, limit=0):
        # TODO 直接使用 mysql like 性能待改善
        cursor = self.cursor
        cursor.execute(
            'select o.id from Ob o left join %s c on o.id = c.id where c.value = %s and o.name like "%%%s%%" limit %s, %s' % (self.__table__, value, name, offset, limit)
        )
        r = cursor.fetchall()

        li = list()
        for o in r:
            li.append(o[0])

        cursor.execute(
            'select count(0) as count from Ob o left join %s c on o.id = c.id where c.value = %s and o.name like "%%%s%%"' % (self.__table__, value, name)
        )
        r = cursor.fetchone()
        count = r[0] if r else 0

        return li, count


# -*- coding: UTF-8 -*-
import time
from warnings import warn
import MySQLdb
from _mysql_exceptions import Warning, InterfaceError, DataError,\
     DatabaseError, OperationalError, IntegrityError, InternalError,\
     NotSupportedError, ProgrammingError
from MySQLdb.converters import FIELD_TYPE, conversions
import logging
from DBUtils.SteadyDB import connect
from operator import itemgetter

def connection(*args, **kwds):
    kwds['maxusage'] = False
    return connect(MySQLdb, *args, **kwds)

class LogCursor(object):
    def __init__(self, cursor):
        self._cursor = cursor
        self.log = []

    def execute(self, *a, **kw):
        t1 = time.time()
        try:
            retval = self._cursor.execute(*a, **kw)
        except:
            self.log.append((a, kw, 0))
            raise
        timecost = time.time() - t1
        self.log.append((a, kw, timecost))
        return retval

    def __iter__(self):
        return iter(self._cursor)

    def __getattr__(self, attr):
        return getattr(self._cursor, attr)

class SqlFarm:
    def __init__(self, conf=None, **kwargs):
        self._config = self.parse_config_string(conf)
        self._config.update(kwargs)
        self._cursor = None

    def connect(self, host, user, passwd, db, **kwargs):
        conn_params = dict(host=host, user=user,
                db=db, init_command='set names utf8',
                **kwargs)
        if passwd :
            conn_params['passwd'] = passwd
        conv = conversions.copy()
        conv.update({
             FIELD_TYPE.TIMESTAMP: None,
             FIELD_TYPE.DATETIME: None,
             FIELD_TYPE.TIME: None,
             FIELD_TYPE.DATE: None,
        })

        conn_params['conv'] = conv
        conn = connection(**conn_params)

        if not conn:
            raise DatabaseError('can not connect to database: %s %s %s'
                         % (host, user, db))
        cursor = conn.cursor()
        #cursor.execute('set sort_buffer_size=2000000')
        cursor = CursorWrapper(cursor, self)
        return cursor

    def close(self):
        if self._cursor:
            self._cursor.connection.close()

    def cursor(self, ro=False):
        if self._cursor is None:
            self._cursor = self.connect(**self._config)
        return self._cursor

    def start_log(self):
        if self._cursor is None:
            self._cursor = self.connect(**self._config)
        self._cursor = LogCursor(self._cursor)

    def stop_log(self):
        if self._cursor is not None:
            self._cursor = self._cursor._cursor

    def get_log(self, name):
        def sql_log(name, log):
            if log:
                return '%s: %d SQL statements (%s seconds):\n%s\n\n' % (
                        name, len(log), sum(x[2] for x in log),
                        '\n'.join(['%8.6fsec %s' % (timecost, a)
                                  for a, kw, timecost in log]))
            else:
                return '%s No Sql Log\n\n'%name
        so = sql_log(name, self._cursor.log)
        return so

    def parse_config_string(self, s):
        dummy = s.split(':')
        if len(dummy) == 4:
            host, db, user, passwd = dummy
            return dict(host=host, db=db, user=user, passwd=passwd)
        elif len(dummy) == 5:
            host, port, db, user, passwd = dummy
            return dict(host=host, port=int(port), db=db, user=user,
                    passwd=passwd)
        else:
            raise ValueError(s)

class SqlStore:

    def __init__(self, host='', port='', user='', password='', db='',
                 db_config=None, **kwargs):
        self.farms = {}
        self.tables = {}
        if db_config is not None:
            for name, f in db_config.items():
                farm = SqlFarm(f['master'], **kwargs)
                self.farms[name] = farm
                for table in f['tables']:
                    self.tables[table] = farm
        #if db_config and '*' not in self.tables:
        #raise DatabaseError('No default farm specified')

        else:
            farm = SqlFarm(':'.join([host, port, db, user, password]))
            self.farms[db] = farm
            self.tables['*'] = farm

        # cache. SqlStore needs to be reloaded is any of these is updated
        self._categories = {}
        self._category_list = None

    def close(self):
        for farm in self.farms.values():
            farm.close()

    def get_farm(self, farm_name):
        farm = self.farms.get(farm_name)
        if farm is None:
            warn('Farm %r is not configured, use default farm' % farm_name,
                    stacklevel=3)
            return self.tables['*']
        else:
            return farm

    def get_db_by_table(self, table):
        farm = self.tables.get(table)
        if farm is None:
            return self.tables.get('*')
            #raise Exception("%s TABLE NOT CONFIGURE" % table)
        else:
            return farm

    def cursor(self, ro=False, farm=None, table='*', tables=[]):
        """get a cursor according to table or tables.

        Note:

          * If `tables` is given, `table` is ignored.
          * If `farm` is given, `table` and `tables` are both ignored.
        """

        if farm:
            farm = self.get_farm(farm)
        elif tables:
            farms = set(self.get_db_by_table(table) for table in tables)
            if len(farms) > 1:
                raise DatabaseError('%s are not in the same farm' % (tables, ))
            farm = farms.pop()
        else:
            farm = self.get_db_by_table(table)
        return farm.cursor(ro=ro)

    def start_log(self):
        for farm in self.farms.values():
            farm.start_log()

    def stop_log(self):
        for farm in self.farms.values():
            farm.stop_log()

    def get_log(self):
        r = ' '.join(farm.get_log(name) for name, farm in self.farms.items())
        return r

    def sync_row(self, from_farm, from_table, to_farm, to_table, **conditions):
        """sync rows of a table from one farm to another.

        Eg.
            store.sync_row('b_farm', 'a_farm.entry_vote',
                           'a_farm', 'entry_vote',
                           user_id=1000001, entry_id=10013364)
        The above method call will copy the first row of entry_vote table
        on b_farm to the corresponding table on a_farm.
        """
        try:
            self._sync_row(from_farm, from_table, to_farm, to_table,
                    **conditions)
        except IntegrityError:
            import traceback; traceback.print_exc()

    def _sync_row(self, from_farm, from_table, to_farm, to_table, **conditions):
        cols, vals = zip(*conditions.items())
        from_cursor = self.cursor(farm=from_farm)
        to_cursor = self.cursor(farm=to_farm)
        where_clause = 'where ' + ' and '.join([col+'=%s' for col in cols])

        # acquire lock
        from_cursor.connection.commit()
        sql = 'update %s set %s %s' % (from_table,
                ','.join(['%s=%s'%(col, col) for col in cols]),
                where_clause)
        from_cursor.execute(sql, vals)

        from_cursor.execute('select * from '+from_table+' ' + where_clause, vals)
        rows = from_cursor.fetchall()

        to_cursor.execute('delete from '+to_table+' ' + where_clause, vals)
        if rows:
            sql = 'insert into %s values (%s)' % (to_table,
                    ','.join(['%s'] * len(rows[0])))
            to_cursor.executemany(sql, rows)
        to_cursor.connection.commit()

        # release lock
        from_cursor.connection.rollback()


    def rollback_all(self):
        for farm in self.farms.values():
            cursor = farm.cursor()
            cursor.connection.rollback()

class CursorWrapper() :

    def __init__(self, cursor, farm) :
        self._cursor = cursor
        self.farm = farm

    def __getattr__(self, name) :
        return getattr(self._cursor, name)

    def execute(self, *args, **kwargs) :
        try :
            return self._cursor.execute(*args, **kwargs)
        except MySQLdb.OperationalError, e:
            error_no = e.args[0]
            if 2000 <= error_no < 3000  :
                self.farm._cursor = None
            self._cursor.connection.rollback()
            raise
        except MySQLdb.ProgrammingError, e:
            if e.args[0] == 2014:
                self.farm._cursor = None
            self._cursor.connection.rollback()
            raise
        except MySQLdb.IntegrityError, e:
            self._cursor.connection.rollback()
            raise

class Db(object):
    def __init__(self, mysql_config):
        self._sqlstore = SqlStore(db_config=mysql_config, charset='utf8')

    def get(self, table='*'):
        return self.db(table).cursor()

    def db(self, table='*'):
        return self._sqlstore.get_db_by_table(table)

    def execute(self, sql, *args):
        cursor = self.get()
        cursor.execute(sql, args)
        return cursor

    def insert_id(self, table, **kwds):
        cursor = self.get(table)
        kwds = kwds.items()

        sql = 'INSERT INTO `%s` (%s) VALUES (%s)'%(
            table,
            '`%s`'%('`,`'.join(map(itemgetter(0), kwds))),
            ','.join(('%s', )*len(kwds))
        )
        cursor.execute(sql, map(itemgetter(1), kwds))
        return cursor.lastrowid

    def fetchone(self, sql, *args):
        cursor = self.execute(sql, *args)
        return cursor.fetchone()

    def fetchall(self, sql, *args):
        cursor = self.execute(sql, *args)
        return cursor.fetchall()


    def fetch0(self, sql, *args):
        r = self.fetchone(sql, *args)
        if r:
            return r[0]
        return 0

    def commit(self):
        cursor = self.get()
        cursor.connection.commit()




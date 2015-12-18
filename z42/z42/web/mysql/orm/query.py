#coding:utf-8
import _env
from z42.config import DEBUG
from time import time
import logging
from operator import itemgetter
from MySQLdb import escape_string

itemgetter0 = itemgetter(0)

def _is_null(kwargs, _condition_str):
    kwds = {}
    for k, v in kwargs.iteritems():
        if v is None:
            _condition_str.append('`%s` is NULL'%k)
        else:
            kwds[k] = v
    return kwds

class Query(object):

    def __init__(self, query_type='SELECT *', args=(), conditions={}, model=None, db=None):
        #from zorm.model import Model
        self.type = query_type
        if args:
            self._condition_str = [args[0]]
            self._conditions_para = list(args[1:])
        else:
            self._condition_str = []
            self._conditions_para = []

        self.conditions = _is_null(conditions, self._condition_str)

        self.order = ''
        self.limit = ()
        self.cache = None
        self.model = model

        if db:
            self.__db__ = db
        elif model:
            self.__db__ = model.__db__

    def __getitem__(self, k):
        if self.cache != None:
            return self.cache[k]

        if isinstance(k, (int, long)):
            self.limit = (k, 1)
            lst = self._data()
            if not lst:
                return None
            return lst[0]
        elif isinstance(k, slice):
            if k.start == 0 and  k.stop is None:
                self.limit = ()
            elif k.start is not None:
                assert k.stop is not None, 'Limit must be set when an offset is present'
                assert k.stop >= k.start, 'Limit must be greater than or equal to offset'
                self.limit = k.start, (k.stop - k.start)
            elif k.stop is not None:
                self.limit = 0, k.stop

        return self._data()

    def __len__(self):
        return len(self._data())

    def __iter__(self):
        return iter(self._data())

    def __repr__(self):
        return repr(self._data())

    def count(self, what='*'):
        if self.cache is None:
            result = Query.execute(
                'SELECT COUNT(%s) FROM %s %s' % (
                    what,
                    self.model.__table__,
                    self._keys() or ''
                ),
                self._values(),
                self.__db__
            )

            #奇怪,DBUtils不这样写返回的就是None
            result = result.fetchone()
            if result:
                result = result[0]
            else:
                result = 0
        else:
            result = len(self.cache)

        return result



    def where(self, *args, **kwargs):
        if args:
            self._condition_str.append(args[0])
            self._conditions_para.extend(args[1:])
        kwds = _is_null(kwargs, self._condition_str)
        self.conditions.update(kwds)

        return self

    def order_by(self, field):
        self.order = 'ORDER BY %s' % field
        return self

    def _keys(self):
        if len(self.conditions) or len(self._condition_str):
            return 'WHERE %s' % ' AND '.join(
                ['`%s`=%%s' % k for k in self.conditions]+self._condition_str
            )

    def _values(self):
        return list(self.conditions.itervalues())+self._conditions_para

    def _query(self):
        return '%s FROM %s %s %s %s' % (
            self.type,
            self.model.__table__,
            self._keys() or '',
            self.order,
            self._limit() or '',
        )

    def _limit(self):
        if len(self.limit):
            return 'LIMIT %s' % ','.join(str(l) for l in self.limit)

    def _data(self):
        if self.cache is None:
            self.cache = list(self.iterator())
        return self.cache

    def iterator(self):
        q = self._execute()
        q = q.fetchall()
        for row in q:
            obj = self.model(*row)
            obj._is_new = False
            yield obj

    def _execute(self):
        values = self._values()
        sql = self._query()
        return Query.execute(sql, values, self.__db__)

    def update(self, *args, **kwds):
        values = self._values()
        update_set = []
        if args:
            update_set.append(args[0])
            values = args[1:]+values
        if kwds:
            update_set.append(
                ','.join(
                    '`%s`=%%s'%k for k in kwds.keys()
                )
            )
            values = list(kwds.values())+values
        if update_set:
            Query.execute(
                'UPDATE %s SET %s %s' % (
                    self.model.__table__,
                    ','.join(update_set),
                    self._keys() or ''
                ),
                values,
                self.__db__
            )

    def delete(self):
        values = self._values()
        Query.execute(
            'DELETE FROM %s %s' % (
                self.model.__table__,
                self._keys() or ''
            ),
            values,
            self.__db__
        )


    @classmethod
    def execute(cls, sql, values, db):
        cursor = db.cursor()
        if DEBUG:
            begin_time = time()
        try:
            cursor.execute(sql, values)
        except Exception, ex:
            logging.error(
                '%s\n%s\nException: %s'%(
                    sql, values, ex
                )
            )
            raise
        if DEBUG:
            if type(values) not in (list , tuple):
                values = ( values , )

            logging.info(
                 '%.2f\n\t%s ;'%(
                    1000*(time() - begin_time),
                    sql.strip()%tuple(map(escape_string, map(str, values)))
                )
            )
        return cursor

    def column(self, column='id', limit=None, offset=None, ):
        self.type = 'SELECT %s' % column
        self.limit = _limit = []
        if limit is not None:
            if offset is not None:
                _limit.append(offset)
            _limit.append(limit)
        r = self._execute().fetchall()

        if r and len(r[0]) == 1:
            return map(itemgetter0, r)

        return r





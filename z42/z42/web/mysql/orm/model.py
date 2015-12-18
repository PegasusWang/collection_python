#coding:utf-8

from query import Query, itemgetter0
from z42.web.memcache import mc
from _db import DB
try:
    from msgpack import packb, unpackb
except:
    from marshal import dumps as packb, loads as unpackb
from time import time
from array import array
from hashlib import md5
from intstr import IntStr

MC_KEYER = IntStr(
    '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
)

if not DB.execute(""" select count(TABLE_NAME) from `INFORMATION_SCHEMA`.`TABLES` where `TABLE_NAME`='ZwebOrmTableMcKey' """).fetchone()[0]:
    DB.execute('''
    CREATE TABLE IF NOT EXISTS `ZwebOrmTableMcKey` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `md5` binary(16) NOT NULL,
    `table` varchar(128) NOT NULL,
    `time` bigint(20) unsigned NOT NULL,
    `database` varchar(128) NOT NULL, 
    PRIMARY KEY (`id`),
    UNIQUE KEY `md5` (`md5`) USING BTREE
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
    ''')



def _key_by_table(db, table, cursor):
    db = db._config
    db_table = '%s@%s:%s.%s'%(db['user'], db['host'], db['port'] , table)

    key = [ db_table ]

    if cursor.description:
        for i in cursor.description:
            key.append('%s:%s'%(i[0], i[1]))

    key = ' '.join(key)
    keyd = md5(key).digest()
    mckey = DB.fetch0('SELECT id FROM ZwebOrmTableMcKey where `md5`=%s', keyd)
    if not mckey:
        id = DB.insert_id(
            'ZwebOrmTableMcKey',
            md5=keyd,
            database=db['db'],
            time=int(time())
        )
        mckey = MC_KEYER.encode(id)
    return str(mckey)

@classmethod
def _commit(cls):
    db = cls.__db__
    DB.commit()

class _Model(type):
    def __new__(cls, name, bases, attrs):
        base0 = bases[0]
        if base0 is object:
            return super(_Model, cls).__new__(cls, name, bases, attrs)

        new_class = type.__new__(cls, name, bases, attrs)

        new_class.__table__ = table = name
        new_class.__db__ = db = DB.db(table)


        q = Query.execute('SELECT * FROM %s LIMIT 1' % name, (), db)
        new_class.__column__ = column = map(itemgetter0, q.description)

        if base0 is ModelMc:
            new_class.__key__ = '%s&%%s'%(_key_by_table(
                db, name, q
            ).replace('%', '%%'))
        return new_class

def _delete(self):
    Query.execute(
        'DELETE FROM %s WHERE id=%%s' % self.__table__ ,
        self.id,
        self.__db__
    )
    return True



@classmethod
def _where(cls, *args, **kwargs):
    return Query(
        model=cls,
        args=args,
        conditions=kwargs
    )


@classmethod
def _count(cls, *args, **kwargs):
    return Query(
        model=cls,
        args=args,
        conditions=kwargs
    ).count(1)

@classmethod
def _iter(cls, id=0, where=None, limit=500):
    while True:
        if where:
            r = cls.where(where)
        else:
            r = cls

        r = r.where('id>%s', id).order_by('id')
        total = tuple(r[:limit])
        if total:
            for i in total:
                #print i.id
                yield i
            id = total[-1].id
        else:
            break

def __ne__(self, other):
    return not (self == other)

def __eq__(self, other):
    if other is not None:
        sid = self.id
        oid = other.id
        if sid is not None and oid is not None:
            return sid == oid
    return False

@classmethod
def _execute(cls, sql, values=()):
    return Query.execute(sql, values, cls.__db__)

@classmethod
def _max_id(cls):
    c = cls.execute(
        'select max(id) from %s'%cls.__table__
    )
    id = c.fetchone()
    if id:
        return id[0]
    return 0

def __init__(self, *args, **kwargs):
    'Allows setting of fields using kwargs'
    self.__dict__['id'] = None

    self._is_new = True

    for i, arg in enumerate(args):
        self.__dict__[self.__column__[i]] = arg

    for i in self.__column__[len(args):]:
        self.__dict__[i] = kwargs.get(i)

    self.__dict__['_updated'] = set()

def __setattr__(self, name, value):
    dc = self.__dict__
    if name[0] != '_' and name in self.__column__:
        dc_value = dc[name]
        if dc_value is None:
            self._updated.add(name)
        else:
            if value is not None:
                value = type(dc_value)(value)
            if dc_value != value:
                self._updated.add(name)
        dc[name] = value
    else:
        attr = getattr(self.__class__, name, None)
        if attr and hasattr(attr, 'fset'):
            attr.fset(self, value)
        else:
            dc[name] = value

def _update(self):
    query = [
        'UPDATE %s SET ' % self.__table__,
        ','.join(['`%s`=%%s'%f for f in self._updated]),
        ' WHERE id=%s '
    ]

    values = [getattr(self, f) for f in self._updated]
    values.append(self.id)

    cursor = Query.execute(' '.join(query), values, self.__db__)

def _insert(self):
    'Uses SQL INSERT to create new record'

    id = self.id
    fields = [
        '`%s`'%f for f in self.__column__
        if id is not None or f != 'id'
    ]
    values = [getattr(self, f, None) for f in self.__column__ if id is not None or f != 'id']


    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
           self.__table__,
           ','.join(fields),
           ','.join(['%s'] * len(fields) )
    )
    cursor = Query.execute(query, values, self.__db__)

    if id is None:
        self.id = cursor.lastrowid

    return True

def _save(self):
    if self._is_new:
        self._insert()
        self._is_new = False
    elif self._updated:
        self._update()
    self._updated.clear()
    return self


@classmethod
def _get_or_create(cls, **kwargs):
    ins = cls.get(**kwargs)
    if ins is None:
        ins = cls(**kwargs)
    return ins


@classmethod
def _get(cls, id=None, **kwargs):
    if id is None:
        if not kwargs:
            return
    else:
        kwargs = {
            'id': id
        }
    q = Query(model=cls, conditions=kwargs)
    q.limit = (0, 1)
    q = q._execute()
    q = q.fetchone()
    if q:
        obj = cls(*q)
        obj.__dict__['_is_new'] = False
        return obj


class Model(object):
    """
能把 mysql 自动映射为 python 的 类 , 比如

mysql数据库中有 User 表 , 结构如下 ::

    CREATE TABLE  `UserMail` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `mail` varchar(128) ,
      PRIMARY KEY (`id`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

Model 定义如下

::

    class UserMail(Model):
        pass


#. 新插入一行 ::

    mail = UserMail(mail="zsp007@gmail.com")
    mail.save()
    
    等价于 SQL ::
        
        insert into UserMail (mail) values ("zsp007@gmail.com")

#. 根据id , 获取一行 ::
   
    mail = UserMail.get(12)
    
    等价于 SQL ::

        select * from UserMail where id = 12 
 
#. 插入或修改一行 ::
    
        user_mail = UserMail.get_or_create(id=21, mail='zsp007@gmail.com')
        user_mail.mail = 'test@example.com'
        user_mail.save()

#. 执行 execute
    
    使用execute方法可以直接执行SQL语句，注意表名大小写 ::

        UserMail.execute('select count(*) from UserMail').fetchone()


#. 删除id为21的行 ::

        UserMail.where(id=21).delete()

    等价于 SQL ::

        DELETE FROM UserMail WHERE id=21

#. 获取最大的id值 ::

        UserMail.max_id()

    等价于 SQL ::

        select max(id) from UserMail

#. 修改一行 ::

    UserMail.where(id=21).update(mail='test@example.com')

    等价于 SQL ::

        UPDATE UserMail SET `mail`=%s WHERE `id`=%s     ['test@example.com', 21]

    """


    __metaclass__ = _Model

    __ne__ = __ne__
    __eq__ = __eq__
    __init__ = __init__

    execute = _execute
    max_id = _max_id
    count = _count
    iter = _iter
    where = _where
    __setattr__ = __setattr__
    save = _save
    get = _get
    _insert = _insert
    get_or_create = _get_or_create

    delete = _delete
    _update = _update

    commit = _commit



def _dumps(self):
    dict = self.__dict__

    value = tuple(
        dict.get(i, None)
        for i in self.__column__
    )

    return packb(value)

class ModelMc(object):

    __metaclass__ = _Model

    __ne__ = __ne__
    __eq__ = __eq__
    __init__ = __init__
    execute = _execute
    max_id = _max_id
    count = _count
    iter = _iter
    where = _where
    __setattr__ = __setattr__
    _insert = _insert
    save = _save
    get = _get
    get_or_create = _get_or_create

    @classmethod
    def _loads(cls, value):
        value = unpackb(value)
        value = cls(*value)
        value._is_new = False
        return value

    @classmethod
    def mc_bind(cls, li, property, key='id'):
        d = []
        e = []
        for i in li:
            k = getattr(i, key)
            if k:
                d.append(k)
                e.append((k, i))
            else:
                i.__dict__[property] = None

        r = cls.mc_get_dict(set(d))
        for k, v in e:
            v.__dict__[property] = r.get(k)




    def delete(self):
        _delete(self)
        self.mc_flush()

    def mc_flush(self):
        mc.delete(self.__key__%self.id)

    @classmethod
    def mc_delete(cls, id):
        mc.delete(cls.__key__%id)

    def _update(self):
        _update(self)
        self.mc_set()


    def mc_set(self):
        key = self.__key__%self.id
        mc.set_msgpack(key, self, dumps=_dumps)

    @classmethod
    def mc_get(cls, id):
        if id:
            key = str(cls.__key__%id)
            value = mc.get_msgpack(key, cls._loads)
            if value is None:
                value = cls.get(id)
                if value:
                    value.mc_set()
            return value

    @classmethod
    def mc_get_dict(cls, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = cls.__key__
        result = mc.get_dict_msgpack([mc_key%i for i in id_list], cls._loads)
        r = {}
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                if i:
                    t = cls.get(i)
                    if t:
                        t.mc_set()
            r[i] = t
        return r

    @classmethod
    def mc_get_list(cls, id_list):
        if type(id_list) not in (array, list, tuple, dict):
            id_list = tuple(id_list)
        mc_key = cls.__key__
        result = mc.get_dict_msgpack([mc_key%i for i in id_list], cls._loads)
        r = []
        for i in id_list:
            t = result.get(mc_key%i)
            if t is None:
                if i:
                    t = cls.get(i)
                    if t:
                        t.mc_set()
                    else:
                        import logging
                        logging.error("mc_get_list 无效用户id：%s" % i)
                        continue
            r.append(t)
        return r

    commit = _commit


if __name__ == '__main__':
    pass


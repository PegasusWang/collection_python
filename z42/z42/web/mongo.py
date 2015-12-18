#!/usr/bin/env python
#coding:utf-8
import _env
import mongokit.connection



class CallableMixin(object):
    """
    brings the callable method to a Document. usefull for the connection's
    register method
    """
    def __call__(self, doc=None, gen_skel=False, lang='en', fallback_lang='en'):
        return self._obj_class(
            doc=doc,
            gen_skel=gen_skel,
            collection=self.collection,
            lang=lang,
            fallback_lang=fallback_lang
        )
mongokit.connection.CallableMixin = CallableMixin

from z42.config import MONGO_CONFIG, APP
from bson.objectid import ObjectId
from mongokit import Document, Connection
from mongokit.document import DocumentProperties
from jsob import JsOb

_iterables = (list, tuple, set, frozenset)


#print MONGO_CONFIG
mongo = Connection(**MONGO_CONFIG)

class MetaDoc(DocumentProperties):
    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaDoc, cls).__new__( cls, name, bases, attrs)
        if bases[0] is not Document:


            new_cls.__mongo__ = mongo
            if not new_cls.__name__.startswith('Callable'):
                new_cls.__collection__ =  (name[0].lower()+name[1:])
                new_cls = mongo.register(new_cls)
                new_cls = getattr(mongo, name)
            else:
                new_cls._protected_field_names.append("_collection")
                _  = getattr(new_cls.__mongo__, new_cls.__database__)
                _  = getattr( _ , new_cls.__collection__)
                new_cls._collection = _

        return new_cls

class Doc(Document):
    __metaclass__ = MetaDoc
    __database__ = APP
    use_dot_notation = True
    use_autorefs = False
    skip_validation = True

    def __init__(self, doc={}, gen_skel=None, *args, **kwds):
        '''
        gen_skel为True的时候设置default value, 否则不设置
        '''
        if doc is None:
            doc = {}
        else:
            if isinstance(doc, JsOb):
                doc = doc.__dict__
        super(Doc, self).__init__(doc, *args, **kwds)
        for i in self.structure:
            if i not in doc:
                self[i]=None

        if gen_skel:
            if self.default_values:
                self._set_default_fields(self, self.structure)

    def upsert(self, spec):

        if isinstance(spec,basestring):
            spec = {'_id': ObjectId(spec)}
        #self.update(spec)
        update = dict((k,v) for k,v in self.iteritems() if v is not None )
        update.update(spec)
        self.collection.update(
            spec,
            {'$set': update},
            upsert=True
        )
        #print spec
        #print {'$set': dict((k,v) for k,v in self.iteritems() if v is not None )},
        return self

    def save(self, *args, **kwds):
        if "_id" in self:
            _id = self['_id']
            if isinstance(_id, basestring):
                self['_id'] = ObjectId(_id)
        super(Doc, self).save(*args,**kwds)
        return self

    @classmethod
    def count(cls, *args, **kwds):
        return cls._collection.find(*args, **kwds).count()

    @classmethod
    def find(cls, *args, **kwds):
        result = []
        for i in cls._collection.find(*args, **kwds):
            i['_id'] = str(i['_id'])
            result.append(i)
        return map(lambda doc:cls(doc, collection=cls._collection), result)

#find_one(self, spec_or_id=None, *args, **kwargs) method of mongokit.collection.Collection instance

    @classmethod
    def find_one(cls, spec_or_id=None, *args, **kwds):
        if isinstance(spec_or_id,basestring):
            spec_or_id = ObjectId(spec_or_id)
        o = cls._collection.find_one(spec_or_id, *args,**kwds)
        if o:
            o['_id']=str(o['_id'])
            return cls(o, collection=cls._collection)

    def delete(self):
        if self._collection:
            self._collection.remove({'_id': ObjectId(self['_id'])})

    @classmethod
    def remove(cls, spec_or_id, safe=None, multi=True, **kwargs):
        if isinstance(spec_or_id,basestring):
            spec_or_id = ObjectId(spec_or_id)
        if spec_or_id:
            cls._collection.remove(spec_or_id=spec_or_id, safe=safe, multi=multi, **kwargs)


if __name__ == "__main__":
    pass
    # mongo.SITE.abc.insert(dict(a=1, b=2))
    # print C.bbb
    # print C.__table__


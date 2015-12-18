#!/usr/bin/env python
#coding:utf-8
import _env
from zapp._WEB.model._db import redis, Doc
from gid import gid
from z42.config import HOST, QINIU
from attrcache import attrcache


class Ob(Doc):
    structure = dict(
        id=int,
        name=str,
        ico=str,
    )
    indexes = [
        {'fields':['id']}
    ]


    @staticmethod
    def new(name):
        id = gid()
        o = Ob(dict(id=id, name=str(name), ico=''))
        o.save()
        return id

    def ico_new(self, ico, crop=None):
        self.ico = ico
        self.save()

    @property
    def ico_url(self):
        #TODO
        return ''

    @property
    def url(self):
        #TODO
        return "//%s.%s"%(self.id, HOST)

    @staticmethod
    def by_id_list(li):
        if li:
            return Ob.find({"id":{"$in":map(int,li)}}) 
        return []

def ob_name_ico_by_id(id):
    ob = Ob.find_one({'id':id})
    return ob.name, ob.ico or 0

def ob_name_by_id(id):
    return Ob.find_one({'id':id}).name

def name_ico_dict_by_id_list(li):
    result = {}
    for i in Ob.by_id_list(li):
        result[i.id] = (str(i.name), i.ico or 0) 
    return result

def name_dict_by_id_list(li):
    result = {}
    for i in Ob.by_id_list(li):
        result[i.id] = str(i.name)
    return result

if __name__ == '__main__':
    for i in Ob.find():
        print i

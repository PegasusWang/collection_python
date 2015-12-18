#!/usr/bin/env python
#coding:utf-8

import _env
from time import time as _time
from enum import IntEnum
from bson.objectid import ObjectId

from z42.web.mongo import Doc

class AdminLog(Doc):
    structure = dict(
            obj_id=ObjectId,
            time=int,
            admin_id=int,
            txt=basestring,
            )

    default_values = {
            'time' : lambda : int(_time()),
            }

    indexes = [{
        'fields' : ['obj_id'],
        'fields' : ['obj_id','time'],
        }]


def admin_log_new(obj_id, admin_id, txt="管理员操作"):
    AdminLog(dict(
        obj_id=ObjectId(obj_id),
        admin_id=admin_id,
        txt=txt),True).save()


def admin_log_list(obj_id, limit=0, offset=0):
    return AdminLog.find(dict(obj_id=ObjectId(obj_id)),sort=[('time',-1),], limit=limit, skip=offset)


if __name__ == "__main__":
    pass


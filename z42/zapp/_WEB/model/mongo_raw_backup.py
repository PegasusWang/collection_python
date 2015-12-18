#!/usr/bin/env python
# coding:utf-8

import _env
from z42.web.mongo import Doc, ObjectId
from time import time


class MongoRowBackup(Doc):
    structure = dict(
        id=ObjectId,
        time=int,
        user_id=int,
        raw=dict,
    )
    default_values = {
        'time': lambda: int(time())
    }
    indexes = [
        {'fields': ['id'], },
    ]


def mongo_raw_backup(user_id, raw):
    id = raw['_id']
    del raw['_id']
    MongoRowBackup(dict(
        user_id=user_id,
        id=ObjectId(id),
        raw=raw
    )).save()

if __name__ == "__main__":
    for i in MongoRowBackup.find():
        print i.id
        print i.raw

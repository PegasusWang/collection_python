#!/usr/bin/env python
# coding:utf-8


import _env
from z42.web.mongo import Doc
from zapp._WEB.model._db import redis, R


class Sign(Doc):
    structure = dict(
        id=int,
        txt=str,
    )

    @staticmethod
    def new(user_id, txt):
        if txt:
            Sign(dict(txt=str(txt))).upsert(dict(id=int(user_id)))


    @staticmethod
    def by_user_id(user_id):
        s = Sign.find_one(dict(id=int(user_id)))
        return s.txt if s else ""




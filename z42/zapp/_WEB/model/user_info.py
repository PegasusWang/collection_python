#!/usr/bin/env python
#coding:utf-8
import _env
import time
from zapp._WEB.model._db import redis, R, Doc
from zapp._WEB.model.gid import gid 

R_USER_INFO_ID = R.USER_INFO_ID() #HSET

def user_info_id_get(user_id):
    return int(redis.hget(R_USER_INFO_ID, user_id) or 0)

def user_info_id_new(user_id):
    id = gid()
    redis.hset(R_USER_INFO_ID, user_id, id)
    return id

def user_info_id_set(user_id, id):
    redis.hset(R_USER_INFO_ID, user_id, id)
    return id

class UserInfo(Doc):
    structure = dict(
        id=int,
        time=int,
    )

    default_values = dict(
        time=lambda: int(time.time())
    )
    
    
if __name__ == "__main__":
    user_id = 1111
    name = 'Kane3'
    age = 11
    UserInfo(dict(
        user_id=user_id,
        data=dict(
            name=name,
            age=age))).save()
    print UserInfo.find_one().to_json()


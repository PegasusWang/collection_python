#!/usr/bin/env python
#coding:utf-8
import _env
from enum import IntEnum
from time import time
import re

from z42.web.mongo import Doc
from zapp._WEB.model._db import redis, R

from zapp._WEB.model.gid import gid
from zapp._WEB.model.admin_log import admin_log_new


R_USER_GROUP_ZSET = R.USER_GROUP_ZSET('%d')
R_GROUP_USER_ZSET = R.GROUP_USER_ZSET('%d')

class GodGroup(Doc):
    structure = dict(
        group_name = basestring,
        group_id = int,
        create_time = int,
        permit = list,
    )

    indexes = [
        {'fields': 'group_id'},
        {'fields': 'permit'},
    ]

    default_values = {
        'create_time':lambda : int(time()),
    }


    @classmethod
    def new(cls, group_name, permit, admin_id=0, group_id=0):
        if not group_id:
            group_id = gid()
        group = GodGroup(dict(permit=permit, group_name=group_name), True)
        group.upsert(dict(group_id=group_id))

        # admin_log_new(group._id, admin_id, "添加分组%s"%ob.name)
        return group


    @classmethod
    def group_list(cls, permit_list=None, limit=0, offset=0, sort=[('create_time', -1)]):
        q = {}
        if permit_list:
            q.update(dict(permit={"$in":permit_list}))
        return GodGroup.find(q, limit=limit, skip=offset, sort=sort)


    # @classmethod
    # def member_list_by_group_id(cls, group_id):
    #     pass


    @classmethod
    def permit_list_by_user_id(cls, user_id):
        permit_list = []

        if not user_id:
            return []

        group_id_list = map(int,redis.zrange(R_USER_GROUP_ZSET%user_id, 0, -1))

        for group in GodGroup.find(dict(group_id={"$in":group_id_list})):
            permit_list += group.permit
        
        return permit_list
    

    @classmethod
    def has_permit(cls, user_id, path):
        authorized = False

        for permit in cls.permit_list_by_user_id(user_id):
            if re.search(permit, path):
                authorized = True
                break

        return authorized


    def member_new(self, user_id, admin_id):
        redis.zadd(R_GROUP_USER_ZSET%self.group_id, int(time()), user_id)
        redis.zadd(R_USER_GROUP_ZSET%user_id, int(time()), self.group_id)
        # admin_log_new(self._id, admin_id, "将%s添加到分组%s"%(ob_name_by_id(user_id), ob_name_by_id(self.group_id)))


    def member_rm(self, user_id, admin_id):
        redis.zrem(R_GROUP_USER_ZSET%self.group_id, user_id)
        redis.zrem(R_USER_GROUP_ZSET%user_id, self.group_id)
#        admin_log_new(self._id, admin_id, "将%s从分组%s删除"%(ob_name_by_id(user_id), ob_name_by_id(self.group_id)))


    def member_id_list(self, limit=0, offset=0):
        return map(int, redis.zrange(R_GROUP_USER_ZSET%self.group_id, offset, limit+offset-1))


    def rm(self, admin_id=0):
        for member_id in self.member_id_list():
            self.member_rm(member_id, admin_id)
        redis.delete(R_GROUP_USER_ZSET%self.group_id)
        GodGroup.remove(self._id)
        


    @property
    def member_count(self):
        return redis.zcard(R_GROUP_USER_ZSET%self.group_id)


if __name__ == "__main__":
    group = GodGroup.find_one(dict(group_id=12877748))
    group.rm()
    # group = GodGroup.new("com_group",['/j/com'])
    # print group.group_name
    # group = GodGroup.find_one(dict(group_id = 12877747))
    # group.member_new(10878765)

    # GodGroup.permit_list_by_user_id(10878765)
    # print GodGroup.is_authorized(10878765, '/test')
    # print GodGroup.is_authorized(10878765, '/j/com')
    # print GodGroup.group_list(permit_list=['/j/com', '/j/user'])
    pass

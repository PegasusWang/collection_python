#!/usr/bin/env python
#coding:utf-8

#redis

class UserGroup(object):
    def __init__(self, id):
        self.id = id

    @classmethod
    def new(cls, user_id, name, id=None):
        pass

    def member_new(self, user_id, admin_id):
        pass

    def member_rm(self, user_id, admin_id):
        pass

    def admin_new(self, user_id, admin_id):
        pass

    def admin_rm(self, user_id, admin_id):
        pass


    def has_member(self, user_id):
        pass

    def has_admin(self, user_id):
        pass


#   ADMIN_GROUP = Group(1023223)
#
#    ADMIN_GROUP.has_member(user_id)
#    ADMIN_GROUP.has_admin(user_id)

# 后台可以显示组的列表
# 后台管理员可以修改组

"""

# zapp.TECH2IPO.view.acl.editor_group
# from z42.config import EDITOR_GROUP_ID
EDITOR_GROUP = AclGroup(EDITOR_GROUP_ID)

from zapp._WEB.view.acl.god_group import GOD_GROUP

@GOD_GROUP.is_admin
def xxx(self):
    pass


@GOD_GROUP.is_member
def xxx(self):
    pass
"""



if __name__ == "__main__":
    pass


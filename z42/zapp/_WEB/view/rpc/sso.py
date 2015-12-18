#!/usr/bin/env python
# coding:utf-8
import _env
from _route import route
from zapp._WEB.model.session import Session
from zapp._WEB.view._rpc.client import ClientRpcView as View
from zapp._WEB.model.sso_sign import sso_sign
from zapp._WEB.model.id_by_sso import id_by_sso_id, sso_id_by_id
from zapp._WEB.model.ob_mail import ob_mail_set 
from zapp._WEB.view._rpc import RpcView, rpc_url, Err, logined, LoginedRpcView
from zapp._WEB.model.sign import Sign
from zapp._WEB.model.user_info import user_info_id_get, user_info_id_set
from z42.config import HOST
from zapp._WEB.model.ob import Ob

@route("sso")
class _(View):
    def login(self, session, user_info_id, expires_days):
        sso_id, binary = Session.decode(session, False)

        user_id = id_by_sso_id(sso_id)
        self.set_cookie("S", Session.set(user_id, binary), domain="."+HOST, expires_days=expires_days)

        if user_info_id != user_info_id_get(sso_id):
            self.redirect(
                sso_sign(
                    sso_id,
                    binary,
                    "user.sync",
                    dict(
                        info = "mail name ico sign phone",
                    )
                )
            )

    def sync( self, sso_id, user_info_id, mail=None, ico=None, name=None, sign=None, phone=None,):
        user_id = id_by_sso_id(sso_id)
        ob = Ob.find_one(dict(id=user_id))
        if ob is None:
            ob = Ob(dict(id=user_id))

        if ico:
            ob.ico = ico

        if name:
            ob.name = name

        ob.save()

        if sign:
            Sign.new(user_id, sign)

        if mail is not None:
            ob_mail_set(user_id, mail)

        user_info_id_set(sso_id, user_info_id)



if __name__ == "__main__":
    pass
#    print user_info_id_get(9912698)
#        print sso_id, user_id, "!!!!!!!", type(user_id), ob.name



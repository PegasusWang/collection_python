#!/usr/bin/env python
#coding:utf-8
import _env
from zapp._WEB.model.client_sign import ClientSign
from zapp._WEB.model.session import Session 
from z42.config import SSO

def sso_sign(sso_id, session, path,  o):
    o['sso_id']=sso_id
    o['app_id']=SSO.ID
    session = str(session)
 
    return "//%s/rpc/%s?%s"%(
        SSO.HOST,
        path,
        ClientSign.url(session+SSO.SECRET,o)
    ) 


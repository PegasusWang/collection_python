#!/usr/bin/env python
import _env
from zapp._WEB.model._db import Doc, redis
from zapp._WEB.model.ob import Ob
from zapp._WEB.model.user_info import user_info_id_new
from zapp._WEB.model.password import password_new

class ObMail(Doc):
    structure = dict(
        id=int,
        mail=str,
    )
    indexes = [
        {'fields':['id']}
    ]

def ob_mail_by_id(id):
    o = ObMail.find_one(dict(id=int(id)))
    if o:
        return o.mail

def ob_mail_by_id(id):
    o = ObMail.find_one(dict(id=int(id)))
    if o:
        return o.mail

def ob_id_by_mail(mail):
    mail = mail.strip().lower()
    o = ObMail.find_one(dict(mail=mail))
    id = o.id if o else 0
    return id

def ob_new_by_mail(name, mail, password):
    id = Ob.new(name)
    ob_mail_set(id, mail)
    password_new(id, password)
    user_info_id_new(id)
    return id

def ob_mail_set(id, mail):
    mail = mail.strip().lower()
    ObMail(dict(mail=mail)).upsert(dict(id=int(id)))


if __name__ == '__main__':
    for i in ObMail.find():
        print i.mail, i.id
    print ob_id_by_mail('zsp007@gmail.com')


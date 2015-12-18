#!/usr/bin/env python
#coding:utf-8

import Cookie
import string

_Morsel = Cookie.Morsel

class MorselHook(_Morsel):
    """
    >>> import inspect
    >>> (inspect.getargspec(MorselHook.set)[3])[0]
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'*+-.^_`|~:"
    >>> cookie = Cookie.SimpleCookie()
    >>> cookie.load("ys-tab:entrance:e=abc; webpy_session_id=75eb60dcc83e2d902146af0bb7f47afe61fbd2b2")
    >>> print cookie
    Set-Cookie: webpy_session_id=75eb60dcc83e2d902146af0bb7f47afe61fbd2b2;
    Set-Cookie: ys-tab:entrance:e=abc;
    """
    def set(self, key, val, coded_val,
            LegalChars=Cookie._LegalChars+':,',
            idmap=string._idmap,
            translate=string.translate):
        return super(MorselHook, self).set(key, val,
                coded_val, LegalChars, idmap, translate)

Cookie.Morsel = MorselHook



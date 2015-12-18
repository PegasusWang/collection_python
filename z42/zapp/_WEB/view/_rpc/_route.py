#!/usr/bin/env python
#coding:utf-8
import _env
from z42.web.route import Route as _Route
from z42.config import HOST
from zapp.TECH2IPO.view._route import ROUTE_LIST 


class Route(_Route):
 
    def __call__(self, url, **kwds):

        return super(Route,self).__call__("/rpc/%s\\.(.*)"%url, **kwds)

route = Route(host=HOST.replace(".","\\."))

ROUTE_LIST.append(route)

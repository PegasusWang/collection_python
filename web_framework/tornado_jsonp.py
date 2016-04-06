#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.json_tools import bson_to_json
from tornado.web import RequestHandler
from tornado.escape import json_encode
from pprint import pprint


class RestHandler(RequestHandler):

    def write_json(self, data_dict):
        """根据是否含有callback请求参数自动返回json或者jsonp调用"""
        callback = self.get_query_argument('callback', None)

        if callback is not None:    # jsonp
            jsonp = "{jsfunc}({json});".format(jsfunc=callback,
                                               json=json_encode(data_dict))
            self.write(jsonp)    # call_set header after call write
            self.set_header("Content-Type", "application/javascript; charset=UTF-8")
        else:   # json
            self.write(data_dict)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

    def write_object(self, code, message, obj_dict, error=None):
        """写入mongodb数据库的一个doc对象
        code, message must not empty"""
        res = {}
        res['code'] = code
        res['message'] = message
        data = bson_to_json(obj_dict)
        res['data'] = data
        self.write_json(res)

    def write_batches(self, code, message, obj_dict_list, error=None):
        """写入mongodb数据库的一个doc对象
        code, message must not empty"""
        res = {}
        res['code'] = code
        res['message'] = message
        data = []
        for obj_dict in obj_dict_list:
            d = bson_to_json(obj_dict)
            data.append(d)
        res['data'] = data
        self.write_json(res)


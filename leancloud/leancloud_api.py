#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import leancloud
from leancloud import Object, Query, File
from StringIO import StringIO
from config import leancloud_config
import os
import mimetypes
import random
import time
import traceback
import requests
import jieba


class LeanCloudApi(object):

    def __init__(self, class_name):
        leancloud.init(leancloud_config.LeanCloud.WeiboApp_APP_ID,
                       master_key=leancloud_config.LeanCloud.WeiboApp_APP_MASTER_KEY)
        self._class = Object.extend(class_name)
        self._query = Query(self._class)

    def save_obj(self, obj_dict):
        c = self._class
        obj = c()
        for k, v in obj_dict.iteritems():
            obj.set(k, v)
        obj.save()

    def get_skip_obj_list(self, skip_num=0, limit_num=30):
        query = self._query
        query.descending('ID')
        query.skip(skip_num*limit_num)
        query.limit(limit_num)
        try:
            res = query.find()
            return res
        except:
            traceback.print_exc()
            return []

    def add_img_info(self, obj_id):
        query = self._query
        obj = query.get(obj_id)
        img_url = obj.get('File').url
        img_info_url = img_url + '?imageInfo'
        r = LeanCloudApi.fetch_data(img_info_url)
        if not r:
            return
        img_info = r.json()
        width = img_info.get('width', None)
        height = img_info.get('height', None)

        try:
            obj.set('height', height)
            obj.set('width', width)
            obj.save()
        except:
            time.sleep(1)
            obj.set('height', height)
            obj.set('width', width)
            obj.save()

    def get_recent_obj_list(self, num):
        query = self._query
        query.descending('ID')
        query.limit(num)
        try:
            obj_list = query.find()
            return obj_list
        except:
            time.sleep(2)
            obj_list = query.find()
            return obj_list or []

    def solve_nums_class_obj(self, callback, nums, skip_num=0, limit_num=500):
        """solve nums of class objs"""
        query = self._query
        query.descending('ID')
        skip_total = skip_num * limit_num
        query.skip(skip_total)

        query.limit(min(nums, limit_num))
        try:
            obj_list = query.find()
        except:
            time.sleep(2)
            obj_list = query.find()
            traceback.print_exc()

        callback(obj_list)

        if nums > (skip_total+limit_num):
            time.sleep(1)
            self.solve_nums_class_obj(callback, nums, skip_num+1, limit_num)

    def solve_all_class_obj(self, callback, skip_num=0, limit_num=500):
        """callback is a function that solve list of class object"""
        query = self._query
        query.descending('ID')
        query.skip(skip_num*limit_num)
        query.limit(limit_num)
        try:
            obj_list = query.find()
        except:
            time.sleep(2)
            obj_list = query.find()
            traceback.print_exc()

        callback(obj_list)

        if len(obj_list) >= limit_num:
            time.sleep(1)
            self.solve_all_class_obj(callback, skip_num+1, limit_num)

    def get_obj_by_ID(self, obj_ID):
        query = self._query
        query.equal_to('ID', obj_ID)
        obj = query.first()
        url = obj.get('File').url
        pic = StringIO(requests.get(url).content)
        content = obj.get('filename').split('.')[0]
        return {'pic': pic, 'content': content}

    def get_obj_by_rangeID(self, beg, end):
        query = self._query
        query.less_than_or_equal_to('ID', end)
        query.greater_than_or_equal_to('ID', beg)
        file_list = query.find()
        file_obj = random.choice(file_list)
        url = file_obj.get('File').url
        pic = StringIO(requests.get(url).content)
        content = file_obj.get('filename').split('.')[0]
        return {'pic': pic, 'content': content}

    def get_imgfile_by_recent_ID(self, nums=50, skips=0):
        query = self._query
        query.descending('ID')
        if skips:
            query.skip(skips)
        query.limit(nums)
        file_list = query.find()
        file_obj = random.choice(file_list)
        url = file_obj.get('File').url
        pic = StringIO(requests.get(url).content)
        content = file_obj.get('filename').split('.')[0]
        return {'pic': pic, 'content': content}

    def exist_file(self, filename):
        """filename have suffix, judge by filename, maybe other field"""
        query = self._query
        query.equal_to('filename', filename)
        try:    # finded
            obj = query.first()
            print filename, '----existed----'
            return True
        except:    # not find
            return False

    @staticmethod
    def fetch_data(url, retries=5):
        try:
            data = requests.get(url, timeout=5)
        except:
            if retries > 0:
                print 'fetch...', retries, url
                time.sleep(3)
                return LeanCloudApi.fetch_data(url, retries-1)
            else:
                print 'fetch failed', url
                data = None
                return data
        return data

    def upload_file_by_url(self, filename, url, tag_list=None):
        """tag_list is tag of string list"""
        data = LeanCloudApi.fetch_data(url)
        if not data:
            return
        data = data.content
        f = File(filename, StringIO(data))
        img_file = self._class()
        img_file.set('File', f)
        img_file.set('filename', filename)
        if tag_list:
            img_file.set('tag_list', tag_list)
        try:
            img_file.save()
            print filename, '----uploaded----'
            self.add_img_info(img_file.id)    # save img_info after save
        except:
            print 'save file failed', url
            time.sleep(5)
            return

    def upload_file(self, file_abspath):
        filename = os.path.basename(file_abspath)    # filename have suffix
        with open(file_abspath, 'r') as f:
            upload_file = File(filename, f)
            upload_file.save()
            print 'uploaded', file_abspath
            img_file = self._class()
            img_file.set('File', upload_file)
            img_file.set('filename', filename)
            tag_list = LeanCloudApi.get_tag_list(filename)
            img_file.set('tag_list', tag_list)
            img_file.save()
            self.add_img_info(img_file.id)    # save img_info after save

    @staticmethod
    def is_img_file(filename):
        suffix = filename.split('.')[-1].lower()    # note: remember ingore case
        img_types = set(['jpg', 'png', 'gif', 'jpeg', 'bmp'])
        return suffix in img_types

    @staticmethod
    def get_tag_list(filename):
        txt = filename.split('.')[0]
        jieba.setLogLevel(60)
        seg_list = jieba.cut(txt)
        return [i for i in seg_list if len(i) >= 2]


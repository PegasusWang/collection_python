#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import json
import re
import requests
import sys
import traceback
from _db import DB
from time import time
from urlparse import urlparse
from hashlib import md5
from extract import extract, extract_all

"""
from _redis import redis, R

R_GID = R.GID()

if not redis.exists(R_GID):
    redis.set(R_GID, 9912499)

def gid():
    return redis.incr(R_GID)
"""

def get_article(html):
    article = extract('<div class="article-content">', '</div>',html)
    return article


def get_logo_url(html):
    logo = extract('<span class="profile_avatar">', '</span>', html)
    logo = extract('<img src="', '"', logo)
    return logo

class ToutiaoSpider(object):
    def __init__(self, db):
    ¦   self._db = db

    def fetch(self, url):
    ¦   try:
    ¦   ¦   html = requests.get(url, timeout=10).text
    ¦   except:
    ¦   ¦   html = ''
    ¦   ¦   traceback.print_exc()
    ¦   return html


    def parse_data(self, json_str):
    ¦   data = json.loads(json_str).get('data')
    ¦   site_to_get_field = ['media_name', 'media_url', 'url', 'display_url']
    ¦   post_to_get_field = ['title', 'abstract', 'keywords', 'digg_count', 'bury_count', 'comment_count', 'article-url']
    ¦   res_site = []
    ¦   res_post = []

    ¦   for each in data:
    ¦   ¦   media_name = each.get('media_name')
    ¦   ¦   if not media_name:
    ¦   ¦   ¦   continue
    ¦   ¦   site = {}
    ¦   ¦   site['name'] = each.get('media_name')
    ¦   ¦   site['id'] = each.get('media_url')
    ¦   ¦   site['gid'] = 1    #gid()
    ¦   ¦   site['url'] = urlparse(each.get('url')).netloc
    ¦   ¦   url = each.get('display_url')
    ¦   ¦   html = requests.get(url).text
    ¦   ¦   site['logo'] = get_logo_url(html)
    ¦   ¦   res_site.append(site)

    ¦   ¦   post = {}
    ¦   ¦   for k in post_to_get_field:
    ¦   ¦   ¦   post[k] = each.get(k)
    ¦   ¦   post['html'] = get_article(html)
    ¦   ¦   post['source_gid'] = site['gid']
    ¦   ¦   res_post.append(post)

    ¦   return [res_site, res_post]

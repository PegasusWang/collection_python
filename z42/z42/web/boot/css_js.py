# coding:utf-8

import _env
from os.path import join, dirname, abspath, exists, splitext
from os import walk, mkdir, remove, makedirs
from collections import defaultdict
from hashlib import md5
from glob import glob
from base64 import urlsafe_b64encode
import envoy
import os
from tempfile import mktemp
from json import dumps
from z42.web.lib.qbox.uploader import QINIU
import re
from z42.config import QINIU as _QINIU, DEBUG
from extract import extract_map



def css_remove_background_url(path, css):
    dirpath = dirname(path[len(_env.PREFIX):])

    def _(img_url):
        if 'data:image' in img_url or img_url.strip('\'")').endswith('.css'):
            return img_url

        img_url = img_url.replace("'", '').replace('"', '')
        img_url = img_url[4:-1].strip()
        if not (img_url.startswith('https://') or img_url.startswith('http://')):
            if not img_url.startswith('/'):
                img_url = join(dirpath, img_url)
            if img_url in CSS_IMG2URL:
                print img_url, CSS_IMG2URL[img_url]
                img_url = CSS_IMG2URL[img_url]
            elif img_url.startswith('//'):
                pass
            elif not exists(join(BULID, img_url)):
                raise Exception('css error : %s\n%s not exist' % (path, img_url))
        return 'url(%s)' % img_url
    css = extract_map('url(', ')', css, _)
    css = extract_map("url(\"", "\")", css, _)
    css = extract_map("url('", "')", css, _)
    return css

# for k, v in CSS_IMG2URL.iteritems():
#    txt = txt.replace(k, v)

BULID = '/tmp/%s'%_QINIU.HOST
BULID_EXIST = set(glob(BULID + '/*'))
PATH2HASH = {}
if not exists(BULID):
    mkdir(BULID)
    os.chmod(BULID, 0777)

#with open(join(_env.PREFIX, 'js/_lib/google_analytics.js'), 'w') as google_analytics:
#    google_analytics.write(
#        """_gaq=[['_setAccount', '%s'],['_trackPageview']];""" % GOOGLE_ANALYTICS)


CSS_IMG2URL = {}


def dirwalk(dirname):
    base = join(_env.PREFIX, dirname)
    merge = []
    file = []
    suffix = '.%s' % dirname
    for dirpath, dirnames, filenames in walk(base, followlinks=True):
        for i in filenames:
            path = abspath(join(dirpath, i))
            if i == 'merge.conf':
                merge.append((path, merge_conf(path, base)))
            if i.endswith(suffix):
                file.append(path)
            elif dirname == 'css':
                filesuffix = splitext(path)[-1][1:]
                if filesuffix not in ('py', 'pyc', 'orig', 'swp', 'conf', 'txt', 'rst', 'html'):
                    url = path[len(_env.PREFIX):]
                    with open(path, 'rb') as infile:
                        filemd5 = urlsafe_b64encode(
                            md5(infile.read()).digest()).rstrip('=')
                        CSS_IMG2URL[url] = filemd5
                        cache_path = join(BULID, filemd5)
                        if not exists(cache_path) and not DEBUG:
                            print 'upload %s > //%s/%s'% (url, _QINIU.HOST, filemd5)
                            r = QINIU.upload( filemd5, path)
                            _hash = r.get('hash', None)
                            if _hash:
                                with open(cache_path, 'w') as c:
                                    c.write(_hash)
                            else:
                                print r
    return file, merge


def merge_conf(file, base):
    ft = defaultdict(list)
    p = None
    dirpath = dirname(file)
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line[0] == '/':
                path = base + line
            else:
                path = join(dirpath, line)
            if line.endswith(':'):
                p = path[:-1].strip()
            elif line and p:
                ft[p].append(path)
    return ft

#@import url(ctrl/main.css);
#@import url(ctrl/zsite.css);
#@import url(ctrl/feed.css);


def merge_css(src_list):
    result = []
    for i in src_list:
        result.append("""@import url(/css%s);""" % (i[len(_env.PREFIX) + 4:]))
    return result


def merge_js(src_list):
    result = [
        '''function LOAD(js){ document.write('<script src="'+js+'"></'+"script>") }'''
    ]

    for i in src_list:
        result.append("""LOAD('/js%s')""" % (
                      i[len(_env.PREFIX) + 3:]))
    return result


def run(suffix):
    file_list, merge_list = dirwalk(suffix)
    file_set = set(file_list)

    to_merge = defaultdict(list)
    for merge_conf, merge in merge_list:
        for to_file, src_list in merge.iteritems():
            if to_file in file_set:
                file_set.remove(to_file)
            for i in src_list:
                if exists(i):
                    to_merge[to_file].append(i)
                else:
                    print merge_conf, 'ERROR'
                    print '\t', i, 'NOT EXIST'

    if suffix == 'css':
        merger = merge_css
        cmd = 'java -jar %s --charset=utf-8 --type css  -o %%s %%s' % join(
            _env.PREFIX, 'static/yuicompressor.jar')
    else:
        merger = merge_js
        #cmd = 'uglifyjs -b -o %s %s '
        cmd = 'uglifyjs -c -o %s %s '
    for i in file_set:
        base = join(_env.PREFIX, suffix)
        with open(i) as infile:
            hash = hash_name(infile.read(), i)
            path = join(BULID, hash) + '.' + suffix
            if path not in BULID_EXIST:
                envoy_run(hash, cmd, path, i)

    for to_file, src_list, in to_merge.iteritems():

        dirpath = dirname(to_file)
        if not exists(dirpath):
            makedirs(dirpath)

        r = merger(src_list)
        with open(to_file, 'w') as to:
            r = '\n'.join(r)
            to.write(r)

        r = []
        for i in src_list:
            build = join(BULID, PATH2HASH[i] + '.' + suffix)
            if exists(build):
                with open(build) as t:
                    r.append(t.read())
        r = '\n'.join(r)
        hash = hash_name(r, to_file)
        path = join(BULID, hash) + '.' + suffix
        # print path
        if path not in BULID_EXIST:
            tmp = mktemp()
            with open(tmp, 'w') as f:
                f.write(r)
            envoy_run(hash, cmd, path, tmp)


def envoy_run(hash, cmd, path, tmp):
    if DEBUG:
        return
    if exists(path):
        return
    t = cmd % (path, tmp)
    print t
    envoy.run(t)
    suffix = path.rsplit('.', 1)[-1]
    if suffix == 'css':
        content_type = 'text/css'
    elif suffix == 'js':
        content_type = 'application/javascript'
    path = '%s/%s.%s' % (BULID, hash, suffix)

    if suffix == 'css':
        with open(path) as css:
            txt = css.read()
            remove(path)
            txt = css_remove_background_url(tmp, txt)
        with open(path, 'w') as css:
            css.write(txt)
    QINIU.upload(hash, path, content_type)


def hash_name(content, path):
    hash = urlsafe_b64encode(md5(content).digest()).rstrip('=')
    PATH2HASH[path] = hash
    return hash

run('css')
run('js')

# for i in BULID_EXIST - set(BULID + '/' + i for i in PATH2HASH.itervalues()):
#    if i.endswith('.css') or i.endswith('.js'):
#        print 'remove', i
#        remove(i)

init = defaultdict(list)
for file_name, hash in PATH2HASH.iteritems():
    dirname, file_name = file_name[len(_env.PREFIX) + 1:].split('/', 1)
    init[dirname].append((file_name.rsplit('.', 1)[0], hash))

for suffix, flist in init.iteritems():
    with open(join(_env.PREFIX, suffix, '_hash_.py'), 'w') as h:
        h.write("""#coding:utf-8\n
import _env

__HASH__ =  {
""")
        for name, hash in flist:
            h.write(
                """    "%s" : '%s', #%s\n""" % (
                    name,
                    hash,
                    name.rsplit('.', 1)[0].replace(
                        '.', '_').replace('-', '_').replace('/', '_')
                )
            )
        h.write('}')

        h.write("""


from z42.config import DEBUG, HOST, QINIU 
from os.path import dirname,basename,abspath
__vars__ = vars()

def _():
    for file_name, hash in __HASH__.iteritems():

        if DEBUG:
            suffix = basename(dirname(__file__))
            value = "/%s/%s.%s"%(suffix,   file_name, suffix)
        else:
            value = "//%s/%s"%(QINIU.HOST, hash)

        name = file_name.replace('.', '_').replace('-', '_').replace('/', '_')

        __vars__[name] = value

_()

del __vars__["_"]
""")

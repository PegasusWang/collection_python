#!/usr/bin/env python
#coding:utf-8
import _env
from os.path import join,exists
from os import makedirs,remove
import types
from datetime import datetime
import gzip
from z42.config import HOST, APP
from single_process import single_process


SITEMAP_INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</sitemapindex>
"""
SITEMAP_INDEX_ITEM = """
   <sitemap>
      <loc>http://%s/misc/sitemap/%s.gz</loc>
      <lastmod>%s+08:00</lastmod>
   </sitemap>
"""

SITEMAP_FILE = []

PWD = join(_env.PREFIX, "zapp", APP, "static", "sitemap")

if not exists(PWD):
    makedirs(PWD)

def save(filename, ormiter, seq=1):
    f = "%s_%s"%(filename, seq)
    SITEMAP_FILE.append(f)

    f = join(PWD, f)
    ft = f+".txt"

    is_over = True
    with open(ft, "w") as output:
        for c, i in enumerate(ormiter):
            output.write(i)
            output.write("\n")
            if c > 49990:
                is_over = False
                break

    with open(ft, "rb") as output:
        with open('%s.gz'%f, "wb") as gzfile:
            f_out = gzip.GzipFile(filename="sitemap.txt", fileobj=gzfile)
            f_out.writelines(output)
            f_out.close()
    remove(ft)
    if is_over is False:
        save(filename, ormiter, seq+1)

@single_process
def run(sitemap):
    for k, v in sitemap.iteritems():
        if type(v) is types.FunctionType and k.startswith("sitemap_"):
            k = k[8:]
            save(k, v())

    NOW = datetime.now().isoformat()[:19]
    with open(join(PWD, "sitemap.xml"), "w") as index:
        index.write(SITEMAP_INDEX%("".join(SITEMAP_INDEX_ITEM%(HOST, i, NOW) for i in SITEMAP_FILE)))


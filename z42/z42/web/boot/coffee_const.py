#!/usr/bin/env python
#coding:utf-8
from glob import glob
import _env
from z42.config import APP
from mako.lookup import TemplateLookup
from os.path import join, abspath
from os import walk


RENDER_PATH = [_env.PREFIX]

template_lookup = TemplateLookup(
    directories=tuple(RENDER_PATH),
    disable_unicode=True,
    encoding_errors='ignore',
    default_filters=['str', ],
    filesystem_checks=True,
    input_encoding='utf-8',
    output_encoding='',
)


def render(htm, **kwds):
    mytemplate = template_lookup.get_template(htm)
    return mytemplate.render(**kwds)

PREFIX = join('coffee', APP.upper())
for (dirpath, dirnames, filenames) in walk(PREFIX):
    for i in glob(join(dirpath, '*.mako')):
        print i
        path = i.rsplit('.', 1)[0]
        with open(join(_env.PREFIX, path), 'wc') as output:
            output.write(
                render(i)
            )

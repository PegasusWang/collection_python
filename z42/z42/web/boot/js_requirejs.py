#!/usr/bin/env python
# coding:utf-8
import _env
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'release':
    import z42.config
    z42.config.DEBUG = False
from z42.config import DEBUG, QINIU
from js._hash_ import __vars__, __HASH__
from os.path import join


result = ['''

PATH = {
''']

result.append("""
""")

for filename in __HASH__.iterkeys():
    if filename == 'require.js/config':
        continue
    path = __vars__[filename.replace('-', '_').replace('/', '_').replace('.', '_')]
    if DEBUG:
        path = path.rsplit('.')[0]
        result.append("    '%s' : '%s.js'" % (filename, path))
    else:
        path = path.rsplit('/', 1)[-1]
        result.append("    '%s' : '%s'" % (filename, path))

result.append("}")

if not DEBUG:
    result.append("""
for k,v of PATH
    PATH[k]="//%s/#{v}"
"""%QINIU.HOST)

result.append("""
require.config(
    paths : PATH
)
""")

with open(join(_env.PREFIX, 'coffee/require.js/config.coffee'), 'w') as require:
    require.write('\n'.join(result))


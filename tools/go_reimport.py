#!/usr/bin/env python3
# https://github.com/appscodelabs/libbuild/blob/master/reimport3.py
# Needed for antipackage with python 2
from __future__ import absolute_import

import datetime
import fnmatch
import glob
import io
import json
import os
import os.path
import re
import socket
import subprocess
import sys
from collections import OrderedDict
from os.path import expandvars

def reimport(prj_pkg, *paths):
    if not prj_pkg.endswith("/"):
        prj_pkg += "/"
    for p in paths:
        if os.path.isfile(p):
            print('Reimporting file: ' + p)
            _reimport(prj_pkg, p)
        elif os.path.isdir(p):
            print('Reimporting dir: ' + p)
            for dir, _, files in os.walk(p):
                for f in fnmatch.filter(files, '*.go'):
                    _reimport(prj_pkg, dir + '/' + f)
        else:
            for f in glob.glob(p):
                print('Reimporinting file: ' + f)
                _reimport(prj_pkg, f)


BEGIN_IMPORT_REGEX = ur'import \(\s*'
END_IMPORT_REGEX = ur'\)\s*'

PKG_MAP = {
    'k8s.io/apimachinery/pkg/api/testing/roundtrip': ['k8s.io/apimachinery/pkg/api/apitesting/roundtrip']
}

def _detect_pkg_alias(line):
    parts = line.strip().split()
    if len(parts) == 2:
        alias = parts[0]
        pkg = parts[1].strip('"')
    else:
        pkg = parts[0].strip('"')
        dirs = pkg.rsplit('/')
        alias = dirs[len(dirs) - 1]
    return pkg, alias

def _reimport(prj_pkg, fname):
    with open(fname, 'r+') as f:
        content = f.readlines()
        out = []
        replacements = {}
        import_block = False
        for line in content:
            c = line.strip()
            if import_block:
                if c == '':
                    continue
                elif re.match(END_IMPORT_REGEX, c) is not None:
                    import_block = False
                else:
                    cur_pkg, cur_alias = _detect_pkg_alias(c)
                    if cur_pkg in PKG_MAP:
                        rep = PKG_MAP[cur_pkg]
                        if len(rep) == 2:
                            out.append('%s "%s"\n' % (rep[1], rep[0]))
                            if rep[1] != cur_alias:
                                replacements[cur_alias] = rep[1]
                        else:
                            nu_pkg, nu_alias = _detect_pkg_alias(rep[0])
                            out.append('"%s"\n' % (rep[0]))
                            if nu_alias != cur_alias:
                                replacements[cur_alias] = nu_alias
                        continue
            elif re.match(BEGIN_IMPORT_REGEX, c) is not None:
                    import_block = True
            out.append(line)

        content = out
        out = []

        pre = []
        std_imps = []
        prj_imps = []
        ext_imps = []
        post = []

        for line in content:
            c = line.strip()
            if import_block:
                if c == '':
                    continue
                elif re.match(END_IMPORT_REGEX, c) is not None:
                    import_block = False
                    post.append(line)
                else:
                    if "." not in line:
                        std_imps.append(line)
                    elif prj_pkg in line:
                        prj_imps.append(line)
                    else:
                        ext_imps.append(line)
            elif re.match(BEGIN_IMPORT_REGEX, c) is not None:
                    import_block = True
                    pre.append(line)
            else:
                for cur, nu in replacements.iteritems():
                    line = line.replace(cur+'.', nu+'.')
                if len(post) > 0:
                    post.append(line)
                else:
                    pre.append(line)

        f.seek(0)
        f.writelines(pre)
        f.writelines(std_imps)
        f.writelines(["\n"])
        f.writelines(prj_imps)
        f.writelines(["\n"])
        f.writelines(ext_imps)
        f.writelines(post)
        f.truncate()


if __name__ == "__main__":
    reimport(sys.argv[1], *sys.argv[2:])
    # if len(sys.argv) > 1:
    #     # http://stackoverflow.com/a/834451
    #     # http://stackoverflow.com/a/817296
    #     globals()[sys.argv[1]](*sys.argv[2:])
    # else:
    #     help()

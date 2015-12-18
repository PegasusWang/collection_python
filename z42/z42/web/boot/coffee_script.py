#!/usr/bin/env python
#coding:utf-8
import _env
from z42.web.lib.replace_line import replace, link_path
import envoy
from os.path import join, dirname, isdir, abspath, basename, islink
import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_MOVED_TO
from os.path import exists
import sys
from tempfile import mkdtemp
from hashlib import md5
from collections import defaultdict
from shutil import copy
from os import makedirs as _makedirs, remove
from shutil import rmtree
from single_process import single_process

HG_IGNORE = set()


def makedirs(path):
    r = []
    while 1:
        dirpath = dirname(path)
        if exists(path):
            break
        else:
            r.append(path)
        path = dirpath
    map(_makedirs, reversed(r))

TMP_DIR = '/tmp/%s' % _env.PREFIX.replace('/', '_')
if not exists(TMP_DIR):
    makedirs(TMP_DIR)

IMPORT_BY = defaultdict(set)

def import_by_line(path, line):
    r = []
    ln = 0
    if line.strip().startswith('#include '):
        ln = line.index('#include')
        line = line.strip().split(' ', 1)[-1]
        for name in line.split(','):
            name = name.strip()
            if name.startswith('/'):
                name = join(_env.PREFIX, 'coffee', name[1:])
            else:
                name = join(path, name)
            name = name + '.coffee'
            r.append(name)
    return r, ln


"""编译coffee文件并返回对应的js文件的路径
"""
def compile(filename, print_path=False):
    realfile = filename
    dirpath = dirname(filename) + '/'
    outpath = join(
        dirpath.replace('/coffee/', '/js/', 1), basename(realfile)[:-7] + '.js')

    with open(filename) as coffeescript:
        m = []
        for l in coffeescript:
            import_by, ln = import_by_line(dirpath, l)
            if import_by:
                for name in import_by:
                    add_import(name, realfile)
                    if exists(name):
                        with open(name) as js:
                            m.append('#--- %s\n' % name)
                            for line in js:
                                m.append(' '* ln + line)
                            m.append('#--- %s\n' % name)
                    else:
                        print '\t#include %s NOT EXIST' % name
                filename = None
            else:
                m.append(l)

        m = ''.join(m)
        filename = join(TMP_DIR, md5(m).hexdigest() + '.coffee')
        print realfile
        if not exists(filename):
            with open(filename, 'w') as output:
                output.write(m)

    if filename.endswith('.coffee'):
        jspath = filename[:-7]
    else:
        jspath = filename

    jspath += '.js'

    if print_path:
        print realfile

    if outpath not in HG_IGNORE:
        write_ignore(outpath)


    if not exists(jspath):
        cmd = 'coffee -c %s' % (filename)
        r = envoy.run(cmd)
        err = r.std_err
        if err:
            print ''
            print realfile
            print err.split('\n')[0].split(',', 1)[-1].strip()
            print ''

    if exists(jspath):
        makedirs(outpath)
        if exists(outpath):
            try:
                rmtree(outpath)
            except OSError:
                pass
        makedirs(dirname(outpath))
        copy(jspath, outpath)

    for i in IMPORT_BY[realfile]:
        compile(i, False)

"""
接受一个文件路径参数，路径从z42目录开始
"""
def write_ignore(ignore):
    with open(join(get_hgignore_path(ignore), '.hgignore'), 'a') as hgignore:
        hgignore.write(get_ignore_by_app(ignore)+"\n")

"""
根据要忽略文件的路径获取对应hgignore文件的路径
"""
def get_hgignore_path(file_to_ignore):
    if "zapp" in file_to_ignore:
        if not file_to_ignore.startswith('zapp'):
            file_to_ignore = 'zapp' + file_to_ignore.split('zapp')[1]
        path_to_hgignore = join(_env.PREFIX, join(*file_to_ignore.split('/',2)[0:2]))
        ignore_by_app = file_to_ignore.split('/',2)[2]
    else:
        path_to_hgignore = _env.PREFIX
    return path_to_hgignore

def sort_ignore(hgignore):
    
    pass


def add_import(i, path):
    if i in IMPORT_BY[path]:
        print Exception('循环引用 %s %s' % (path, i))
    else:
        IMPORT_BY[i].add(path)

def main():
    # 扫描并编译coffee文件

    for path, content in replace(join(_env.PREFIX, 'coffee'), 'coffee'):
        for line in content:
            import_by, _ = import_by_line(dirname(path), line)
            for i in import_by:
                add_import(i, path)
        compile(path)



    #对hgignore文件进行排序，并加入set中
    ignore_list = []

    for hgignore_path, hgignore in replace(_env.PREFIX,suffix_list=('hgignore')):
        hgignore_prefix = hgignore_path.split('.')[0]
        for line in hgignore:
            line = line.strip()
            if not line or line=='syntax: glob':
                continue
            #转换为完整路径防止app之间互相影响
            line = "%s%s"%(hgignore_prefix, line)
            if line not in HG_IGNORE:
                HG_IGNORE.add(line)
                ignore_list.append(line)

    ignore_list.sort()
    # #写入排序后的hgignore文件

    flush_list = []
    for ignore in ignore_list:
        ignore = ignore.strip()
        if not ignore:
            continue
        hgignore_path = join(get_hgignore_path(ignore),'.hgignore')
        if not hgignore_path in flush_list:
            hgignore = open(hgignore_path, 'w')
            flush_list.append(hgignore_path)
            hgignore.flush()
            hgignore.write('syntax: glob\n\n')
            hgignore.close()
        hgignore = open(hgignore_path, 'a+')
        hgignore.write('%s\n'%get_ignore_by_app(ignore))
    

def get_ignore_by_app(ignore):
    if "zapp" in ignore:
        if not ignore.startswith('zapp'):
            ignore = ignore.split('zapp')[1]
        ignore = ignore.split('/',2)[2]
    else:
        ignore = ignore.split('%s/'%_env.PREFIX)[1]
    return ignore

class EventHandler(ProcessEvent):
    def compress(self, event):
        path = event.path
        filename = join(path, event.name)
        if not filename.endswith('.coffee'):
            return
        compile(filename)
        sys.stdout.flush()

    process_IN_MOVED_TO = process_IN_MODIFY = compress

@single_process
def FSMonitor(path='.'):
    wm = WatchManager()
    mask = IN_CREATE | IN_MODIFY | IN_MOVED_TO
    notifier = Notifier(wm, EventHandler())
    path = join(_env.PREFIX, 'coffee')
    for i in os.listdir(path):
        p = join(path, i)
        if not isdir(p):
            continue
        p = link_path(p)
        wm.add_watch(p, mask, rec=True)
    wm.add_watch(path, mask, rec=True)

    print '开始实时编译 COFFEE SCRIPT %s' % (path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break
if __name__ == "__main__":
    main()
    import sys
    if sys.argv[1:] and sys.argv[1] == '-once':
        pass
    else:
        FSMonitor()
    pass



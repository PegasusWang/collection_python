#!/usr/bin/env python
#
# Copied from somewhere, I don't know wherefrom anymore.  What it does is
# convert from ``\r\n`` to just ``\n`` in case you've got files with windows
# line endings.
#
# TODO:
#
# - Clean up a bit, make it pep8-compliant.
#
# - Check that it works (as I had the impression it didn't work all the time).

from string import join
from string import split
import getopt
import os
import re
import shutil
import sys


def dos2unix(filename):
    import sys
    text = open(filename, 'rb').read().replace('\r\n', '\n')
    open(filename, 'wb').write(text)


def dos2unix(data):
    return join(split(data, '\r\n'), '\n')


def unix2dos(data):
    return join(split(dos2unix(data), '\n'), '\r\n')


def confirm(file_):
    s = raw_input('%s? ' % file_)
    return s and s[0] == 'y'


def usage():
    print """\
USAGE
    dos2unix.py [-iuvnfcd] [-b extension] file {file}
DESCRIPTION
    Converts files from unix to dos and reverse. It keeps the
    mode of the file.
    Binary files are not converted unless -f is specified.
OPTIONS
    -i      interactive (ask for each file)
    -u      unix2dos (inverse functionality)
    -v      print files that are converted
    -n      show but don't execute (dry mode)
    -f      force. Even if the file is not ascii convert it.
    -b ext  use 'ext' as backup extension (default .bak)
    -c      don't make a backup
    -d      keep modification date and mode
"""
    sys.exit()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "fniuvdc")
        args[0]
    except:
        usage()
    force = 0
    noaction = 0
    convert = dos2unix
    verbose = 0
    copystat = shutil.copymode
    backup = '.bak'
    nobackup = 0
    interactive = 0
    for k, v in opts:
        if k == '-f':
            force = 1
        elif k == '-n':
            noaction = 1
            verbose = 1
        elif k == '-i':
            interactive = 1
        elif k == '-u':
            convert = unix2dos
        elif k == '-v':
            verbose = 1
        elif k == '-b':
            backup = v
        elif k == '-d':
            copystat = shutil.copystat
        elif k == '-c':
            nobackup = 1
    asciiregex = re.compile('[ -~\r\n\t\f]+')
    for file_ in args:
        if not os.path.isfile(file_) or file_[-len(backup):] == backup:
            continue
        fp = open(file_)
        head = fp.read(10000)
        if force or len(head) == asciiregex.match(head):
            data = head+fp.read()
            newdata = convert(data)
            if newdata != data:
                if verbose and not interactive:
                    print file_
                if not interactive or confirm(file_):
                    if not noaction:
                        newfile = file_+'.@'
                        f = open(newfile, 'w')
                        f.write(newdata)
                        f.close()
                        copystat(file_, newfile)
                        if backup:
                            backfile = file_+backup
                            os.rename(file_, backfile)
                        else:
                            os.unlink(file_)
                        os.rename(newfile, file_)
                        if nobackup:
                            os.unlink(backfile)


try:
    main()
except KeyboardInterrupt:
    pass

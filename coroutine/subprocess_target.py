#!/usr/bin/env python
# -*- coding:utf-8 -*-


def coroutine(func):
    def start(*args, **kwargs):
        rc = func(*args, **kwargs)
        rc.next()
        return rc
    return start

# bridge two coroutine over a file/pipe

@coroutine
def sendto(f):
    try:
        while True:
            item = yield
            pickle.dump(item, f)
            f.flush()
    except StopIteration:
        f.close()


def fecvfrom(f, target):
    try:
        while True:
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-


def debug():
    import traceback
    traceback.print_exc()
    from pprint import pprint
    pprint(locals())

if __name__ == '__main__':
    try:
        raise Exception()
    except Exception as e:
        debug()

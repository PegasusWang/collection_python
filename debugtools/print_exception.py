#!/usr/bin/env python
# -*- coding:utf-8 -*-


debug_s = """__import__('traceback').print_exc();__import__('pprint').pprint(locals())"""
if __name__ == '__main__':
    try:
        raise Exception()
    except Exception as e:
        exec debug_s

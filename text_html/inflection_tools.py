#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install inflection

import inflection


def underscore(name='CamelCase'):
    """ 骆驼表示法变成下滑线加上小写字母表示
    http://inflection.readthedocs.io/en/latest/"""
    return inflection.underscore(name)

if __name__ == '__main__':
    print(underscore())
    print(underscore('CamelCase'))

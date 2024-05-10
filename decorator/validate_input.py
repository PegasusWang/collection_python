#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   validate_input.py
@Time    :   2023/09/23 20:39:11
@Author  :   jumploop
@Version :   1.0
'''


def validate_input(func):
    def wrapper(*args, **kwargs):
        # your data validation logic here
        if valid_date:
            return func(*args, **kwargs)
        else:
            raise ValueError('Invalid data. Please check your inputs.')

    return wrapper


@validate_input
def my_func(data):
    pass

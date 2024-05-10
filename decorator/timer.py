#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time=time.time()
        result=func(*args, **kwargs)
        end_time=time.time()
        print(f'{func.__name__} took {end_time-start_time:.2f} seconds to execute.')
        return  result
    return wrapper

@timer
def my_func():
    time.sleep(3)
    print('hello world')
    return "ok"


if __name__ == '__main__':
    print(my_func())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Debugging {func.__name__} - args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper


@debug
def complex_data_processing(data, threshold=0.5):
    # Your complex data processing code here
    return data


if __name__ == "__main__":
    print(complex_data_processing(1))

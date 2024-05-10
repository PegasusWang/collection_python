#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings


def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated and will be removed in future versions.",
            DeprecationWarning,
        )
        return func(*args, **kwargs)

    return wrapper


@deprecated
def old_data_processing(data):
    # Your old data processing code here
    return data


if __name__ == "__main__":
    print(old_data_processing("foo"))

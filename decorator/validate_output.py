#!/usr/bin/env python
# -*- coding: utf-8 -*-


def valid_output(data):
    return isinstance(data, int)


def validate_output(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if valid_output(result):
            return result
        else:
            raise ValueError("Invalid output. Please check your function logic.")

    return wrapper


@validate_output
def clean_data(data):
    # Your data cleaning code here
    return data


if __name__ == "__main__":
    clean_data("12")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
def suppress_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None

    return wrapper


@suppress_errors
def preprocess_data(data):
    # Your data preprocessing code here
    return data / 0


if __name__ == "__main__":
    preprocess_data(123)

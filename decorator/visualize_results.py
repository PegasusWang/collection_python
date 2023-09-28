#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def visualize_results(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        plt.figure()
        # Your visualization code here
        plt.show()
        return result

    return wrapper


@visualize_results
def analyze_and_visualize(data):
    # Your combined analysis and visualization code here
    return data


if __name__ == "__main__":
    print(analyze_and_visualize("data"))

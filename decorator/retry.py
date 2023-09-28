#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests


def retry(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"Attempt {attempts + 1} failed. Retrying in {delay} seconds."
                    )
                    attempts += 1
                    time.sleep(delay)
            raise Exception("Max retry attempts exceeded.")

        return wrapper

    return decorator


@retry(max_attempts=3, delay=2)
def fetch_data_from_api(api_url):
    # Your API data fetching code here
    response = requests.get(api_url)
    return response.json()


if __name__ == "__main__":
    print(fetch_data_from_api("https://www.google.com/"))

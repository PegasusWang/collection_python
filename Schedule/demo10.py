#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools

import schedule

"""
Schedule 不会自动捕捉异常，它遇到异常会直接抛出，这会导致一个严重的问题：后续所有的作业都会被中断执行，因此我们需要捕捉到这些异常。
"""


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=True)
def bad_task():
    return 1 / 0

@catch_exceptions(cancel_on_failure=True)
def job():
    print("i'm working...")


schedule.every(5).seconds.do(bad_task)
schedule.every(7).seconds.do(job)

while True:
    schedule.run_pending()

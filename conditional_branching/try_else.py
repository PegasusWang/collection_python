#!/usr/bin/env python
# -*- coding: utf-8 -*-
def do_the_first_thing():
    pass


def do_the_second_thing():
    pass


def do_stuff():
    first_thing_successed = False
    try:
        do_the_first_thing()
        first_thing_successed = True
    except Exception as e:
        print("Error while calling do_some_thing")
        return

    # 仅当 first_thing 成功完成时，做第二件事
    if first_thing_successed:
        return do_the_second_thing()


def do_stuff():
    try:
        do_the_first_thing()
    except Exception as e:
        print("Error while calling do_some_thing")
        return
    else:
        return do_the_second_thing()

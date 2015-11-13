#!/usr/bin/env python
# -*- coding:utf-8 -*-



def coroutine(func):
    def start(*args, **kwargs):
        rc = func(*args, **kwargs)
        rc.next()
        return rc
    return start


@coroutine
def threaded(target):
    messages = Queue()    # message queue
    def run_target():
        while True:
            item = messages.get()    # A thread loop forever.pulling items out of
                                     # the message queue and sending to the
                                     # target

            if item is GeneratorExit:    # handle close so that thread shuts down correctly
                target.close()
                return
            else:
                target.send(item)
        Thread(target=run_target).start()

        try:
            while True:
                item = yield    # receive items and pass them into the
                                # thread (via the queue)
                messages.put(item)
        except GeneratorExit:
            messages.put(GeneratorExit)


if __name__ == '__main__':
    main()

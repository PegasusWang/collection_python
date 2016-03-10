import time
import threading
from functools import wraps

def rate_limited(max_per_second, mode='wait', delay_first_call=False):
    """
    Decorator that make functions not be called faster than

    set mode to 'kill' to just ignore requests that are faster than the
    rate.

    set delay_first_call to True to delay the first call as well
    """
    lock = threading.Lock()
    min_interval = 1.0 / float(max_per_second)
    def decorate(func):
        last_time_called = [0.0]
        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            def run_func():
                lock.release()
                ret = func(*args, **kwargs)
                last_time_called[0] = time.perf_counter()
                return ret
            lock.acquire()
            elapsed = time.perf_counter() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if delay_first_call:
                if left_to_wait > 0:
                    if mode == 'wait':
                        time.sleep(left_to_wait)
                        return run_func()
                    elif mode == 'kill':
                        lock.release()
                        return
                else:
                    return run_func()
            else:
                # Allows the first call to not have to wait
                if not last_time_called[0] or elapsed > min_interval:
                    return run_func()
                elif left_to_wait > 0:
                    if mode == 'wait':
                        time.sleep(left_to_wait)
                        return run_func()
                    elif mode == 'kill':
                        lock.release()
                        return
        return rate_limited_function
    return decorate

@rate_limited(2, mode='wait')
def print_num_wait(num):
    print (num )

@rate_limited(1/2, mode='kill')
def print_num_kill(num):
    print(num)

@rate_limited(2, mode='kill', delay_first_call=True)
def print_num_kill_delay(num):
    print(num)

@rate_limited(1/3, mode='wait', delay_first_call=True)
def print_num_wait_delay(num):
    print(num)

@rate_limited(1/3, mode='refresh_timer')
def print_num_wait_refresh(num):
    print(num)
if __name__ == "__main__":
    print('Rate limited at 2 per second at most')
    print()
    print("Mode is Kill")
    print("1 000 000 print requests sent to decorated function")
    for i in range(1,1000000):
        print_num_kill(i)

    print()
    print('Mode is Wait - default')
    print("10 print requests sent to decorated function")
    for i in range(1,11):
        print_num_wait(i)

    print()
    print('Mode is Kill with Delay on first request')
    print("1 000 000 print requests sent to decorated function")
    for i in range(1, 1000000):
        print_num_kill_delay(i)

    print()
    print('Mode is Wait with Delay on first request')
    print("5 print requests sent to decorated function")
    for i in range(1, 6):
        print_num_wait_delay(i)

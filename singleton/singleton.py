
# 方法一：使用装饰器实现单例模式。

from calendar import c
from functools import wraps
from tkinter.messagebox import NO


def singleton(cls):
    """单例类装饰器"""
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class President:
    pass

# test


p1 = President()
p2 = President()

print(p1 is p2)
# output: True


# 方法二：使用元类实现单例模式。

class SingletonMeta(type):
    """自定义单例元类"""
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class President(metaclass=SingletonMeta):
    pass

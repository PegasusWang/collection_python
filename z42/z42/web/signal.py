#coding:utf-8
import _env
from types import FunctionType
from z42.config._signal import SIGNAL_IMPORT

def _call(func, args):
    if type(args) is not tuple:
        args = args,
    if type(func) is FunctionType:
        args = args[:func.func_code.co_argcount]
    func(*args)

class Signal(object):
    def __init__(self, name):
        self._li = []
        self.name = name

    # SINGAL.xxxxxx.rm(func)
    def rm(self, func):
        self._li.remove(func)

    def __lshift__(self, args):
        name = self.name
        if name in SIGNAL_IMPORT:
            for i in SIGNAL_IMPORT[name]:
                __import__(i)
            del SIGNAL_IMPORT[name]

        for func in self._li:
            _call(func, args)

    def __call__(self, func):
        self._li.append(func)
        return func


class _(object):
    def __getattr__(self, name):
        d = self.__dict__
        if name not in d:
            d[name] = Signal(name)
        return d[name]



signal = _()

if __name__ == "__main__":


    @signal.follow_new
    def _(a,b=5):
        print a,b

    signal.follow_new << (2 , 3)
    signal.follow_new << 1 




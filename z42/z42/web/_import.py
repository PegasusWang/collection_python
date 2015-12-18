#coding:utf-8
import sys

def _import(name):
    components = name.split('.')

    r = []
    for i in xrange(1, len(components)+1):
        key = '.'.join(components[:i])
        if key in sys.modules:
            _mod = sys.modules[key]
            if _mod:
                r.append((key, _mod))
            del sys.modules[key]

    if len(components) == 1:
        mod = __import__(name, globals(), locals(), [], -1)
    else:
        mod = __import__('.'.join(components[:-1]), globals(), locals(), [components[-1]], -1)

        for i in components[1:]:
            if hasattr(mod, i):
                mod = getattr(mod, i)
            else:
                mod = None
                break

    for key, _mod in r:
        sys.modules[key] = _mod

    return mod


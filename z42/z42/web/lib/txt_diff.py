#coding:utf-8
#coding:utf-8
from diff_match_patch import diff_match_patch
def diff_get(txt1, txt2):
    diff = diff_match_patch()
    _diff = diff.diff_compute(txt1, txt2, True, 3)
    result = ''
    for i in _diff:
        num, content = i
        if num < 0:
            result += ('-    ' + content + '\n')
        if num > 0:
            result += ('+    ' + content + '\n')
    return result

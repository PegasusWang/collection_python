#!/usr/bin/env python
#coding:utf-8
import re
import time

DATE_FORMATS = (
    ('%Y-%m-%d', 'day'), # 114264
    ('%Y', 'year'), # 6667
    ('%d %B, %Y', 'day'), # 5032
    ('%Y年%m月%d日', 'day'), # 1488
    ('%Y.%m.%d', 'day'), # 992
    ('%B %d, %Y', 'day'), # 798
    ('%Y/%m/%d', 'day'), # 703
    ('%Y年%m月', 'month'), # 361
    ('%Y年', 'year'), # 254
    ('%m/%d/%Y', 'day'), # 211
    ('%Y-%m', 'month'), # 189
    ('%Y.%m', 'month'), # 167
    ('%d.%m.%Y', 'day'), # 138
    ('%b %d, %Y', 'day'), # 119
    ('%d %b %Y', 'day'), # 77
    ('%b %Y', 'month'), # 57
    ('%d-%m-%Y', 'day'), # 51
    ('%B %Y', 'month'), # 45
    ('%d. %B %Y', 'day'), # 44
    ('%d %B %Y', 'day'), # 42
    ('%d/%m/%Y', 'day'), # 41
    ('%Y%m%d', 'day'), # 41
    ('%b.%Y', 'month'), # 33
    ('%Y/%m', 'month'), # 31
    ('%Y %m %d', 'day'), # 28
    ('%y.%m.%d', 'day'), # 25
    ('%Y 年 %m 月 %d 日', 'day'), # 23
    ('%b %d %Y', 'day'), # 15
    ('%Y.%m.%d.', 'day'), # 13
    ('%m/%Y', 'month'), # 12
    ('%b-%d-%Y', 'day'), # 12
    ('%Y %m', 'month'), # 11
    ('%B, %Y', 'month'), # 10
    ('%Y年 %m月', 'month'), # 10
    ('%d-%b-%Y', 'day'), # 10
    ('%dth %B %Y', 'day'), # 8
    ('%m-%d-%y', 'day'), # 7
    ('%B %dth %Y', 'day'), # 5
    ('%B %dth, %Y', 'day'), # 5
    ('%Y 年', 'year'), # 5
    ('%Y.%m.', 'month'), # 5
    ('%b. %Y', 'month'), # 5
    ('%Y - %m - %d', 'day'), # 5
    ('%m.%d.%Y', 'day'), # 4
    ('%y', 'year'), # 4
    ('%B %d %Y', 'day'), # 4
    ('%b. %d, %Y', 'day'), # 3
    ('%y年', 'year'), # 3
    ('%y年%m月', 'month'), # 3
    ('%b-%Y', 'month'), # 3
    ('%m/%d/%y', 'day'), # 3
    ('%b. %Y/%d', 'day'), # 3
    ('%Y. %m', 'month'), # 2
    ('Date of Release  %Y', 'year'), # 2
    ('%Y/%m/', 'month'), # 2
    ('%Y年%m月%d号', 'day'), # 2
    ('%d-%b-%y', 'day'), # 2
    ('%dth %B, %Y', 'day'), # 2
    ('%Y年%m月%d', 'day'), # 2
    ('%d, %B, %Y', 'day'), # 2
    ('%m-%d-%Y', 'day'), # 2
    ('%Y %b %d', 'day'), # 2
    ('%Y.', 'year'),
    #('(%B %d, %Y)', 'day'), # 2
    #('%B %drd, %Y', 'day'), # 1
    #('%Y %B', 'month'), # 1
    #('%B %dth, %Y.', 'day'), # 1
    #('%y,%m,%d', 'day'), # 1
    #('%b /%Y', 'month'), # 1
    #('%m.%Y', 'month'), # 1
    #('(%Y/%m/%d', 'day'), # 1
    #('%b, %y', 'month'), # 1
    #('%Y 年%m月', 'month'), # 1
    #('%Y-%m.%d', 'day'), # 1
    #('%dst %B %Y', 'day'), # 1
    #('%Y/%m/%d(日本)', 'day'), # 1
    #('%dth of %B %Y', 'day'), # 1
    #('%Y;%m.%d', 'day'), # 1
    #('出版日期：%Y年%m月', 'month'), # 1
    #('%Y年重版', 'year'), # 1
    #('首发：%Y年%m月%d日', 'day'), # 1
    #('%Y, %m', 'month'), # 1
    #('Release Date: %b %d, %Y', 'day'), # 1
    #('%d.%B.%Y', 'day'), # 1
    #('%Y-%m-%d (GER/AUT/CH)', 'day'), # 1
    #('%Y,%m,%d', 'day'), # 1
    #('%B %d, %Y (Mountain View, CA)', 'day'), # 1
    #('%b. %d %Y', 'day'), # 1
    #('%Y年%m月%d日（全亚洲同步发行唱片）', 'day'), # 1
    #('(%Y/%m/%d)', 'day'), # 1
    #('%Y%m-%d', 'day'), # 1
    #('%drd %B, %Y', 'day'), # 1
    #('%Y.%m.%dRELEASE', 'day'), # 1
    #('%Y %m.%d', 'day'), # 1
    #('%Y %b. %d', 'day'), # 1
    #('%Y.%m.%d ON SALE', 'day'), # 1
    #('%dth, %b %Y', 'day'), # 1
    #('%B %d,%y', 'day'), # 1
    #('%b.%Y.', 'month'), # 1
    #('%d-%B-%Y', 'day'), # 1
    #('%Y引进', 'year'), # 1
    #('Original Release Date: %Y', 'year'), # 1
    #('%m/%y', 'month'), # 1
    #('%d,%m,%Y', 'day'), # 1
    #('%m / %d / %Y', 'day'), # 1
    #('%B %d, %Y)', 'day'), # 1
    #('%b.%drd.%Y', 'day'), # 1
    #('(%d %b %Y)', 'day'), # 1
    #('%y-%m-%d', 'day'), # 1
    #('%Y %b', 'month'), # 1
    #('%B %dnd, %Y', 'day'), # 1
    #('%b, %Y', 'month'), # 1
    #('%m/%d-%Y', 'day'), # 1
    #('%Y‧%m‧%d', 'day'), # 0
    #('%b %d,%Y', 'day'), # 0
    #('%b %dth %Y', 'day'), # 0
    #('%Y年%m月%d曰', 'day'), # 0
    #('%Y年%m月%d日発売', 'day'), # 0
    #('%Y　%m', 'month'), # 0
    #('%Y／%m／%d', 'day'), # 0
    #('%Y．%m', 'month'), # 0
    #('%Y．%m．%d', 'day'), # 0
    #('%Y。%m。%d', 'day'), # 0
    #('%Y－%m－%d', 'day'), # 0
    #('%Y/%m/%d 発売', 'day'), # 0
    #('%Y年發行', 'year'), # 0
    #('%Y－%m', 'month'), # 0
    #('%Y—%m—%d', 'day'), # 0
    #('%Y.%m. 發行', 'month'), # 0
    #('%b %Y', 'month'), # 0
    #('%Y年%m月發行', 'month'), # 0
)

multi_replace_map = {
        '／': '/',
        '－': '-',
        '—': '-',
        '—': '-',
        '零': '0',
        '一': '1',
        '二': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9',
        '十一': '11',
        '十二': '12',
        '十': '10',
        '０': '0',
        '１': '1',
        '２': '2',
        '３': '3',
        '４': '4',
        '５': '5',
        '６': '6',
        '７': '7',
        '８': '8',
        '９': '9',
        '。': '.',
        '，': ',',
        '  ': ' ',
        '　': ' ',
        '．': '.',
        '．': '.',
        '‧': '.',
        '(': '',
        ')': '',
        "'": '',
        '"': '',
        ';': '.',
        '曰': '日',
        '発売': '',
        '發行': '',
}

class MultiReplace(object):
    """
    >>> multi_replace_map = {
    ...   'a': 'A',
    ...   'B': 'b',
    ...   'c': '',
    ...   '(': '',
    ... }
    >>> a=MultiReplace(multi_replace_map)
    >>> a('abc(ABC)')
    'AbAbC)'
    """

    def __init__(self, replace_map):
        self.map = replace_map
        def multi_replace_repl(obj):
            return replace_map[obj.group(0)]
        multi_replace_re = re.compile('|'.join(re.escape(r) for r in
            replace_map.keys()))
        multi_replace = lambda s: multi_replace_re.sub(multi_replace_repl, s)
        self._replace = multi_replace

    def __call__(self, s):
        return self._replace(s)

class PublishDateParser(object):
    def __init__(self):
        self.replace = MultiReplace(multi_replace_map)

    def date_parser(self, date_str):
        date_str = self.replace(date_str).strip()
        t = None
        for f, precision in DATE_FORMATS:
            try:
                t = time.strptime(date_str, f)
                #date = "%4d-%02d-%02d" % (t[0], t[1], t[2])
                break
            except:
                pass
        if t:
            #return precision, date
            return int(time.mktime(t))
        else:
            return None

    __call__ = date_parser

dateparser = PublishDateParser()


if __name__ == '__main__':
    print dateparser('2007-04-25')
    print dateparser('2007年04月25')
    print dateparser('2007年')
    print dateparser('2007')




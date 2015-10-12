#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 模仿百度蜘蛛
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
}
r = requests.get(url, headers=headers)


Baiduspider：
Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)

360Spider：
Mozilla/5.0+(compatible;+MSIE+9.0;+Windows+NT+6.1;+Trident/5.0);+360Spider

Sogouspider：
Sogou+web+spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)


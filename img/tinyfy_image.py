"""
压缩图片

pip install --upgrade tinify

https://tinypng.com
申请 api key ，每月有免费几百张额度
https://tinypng.com/developers/reference/python
参考：
https://blog.csdn.net/weixin_41010198/article/details/106544789
"""

import tinify
tinify.key = ""

source = tinify.from_file("test.png")
source.to_file("test.png")

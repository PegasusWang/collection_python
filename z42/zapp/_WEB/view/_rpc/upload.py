#!/usr/bin/env python
#coding:utf-8

@route('/j/upload_token')
class _(JsonErrView):
    def get(self):
        self.finish(QINIU_TOKEN.new(
            returnBody="""{
"key":$(key),
"w": $(imageInfo.width),
"h": $(imageInfo.height),
"fn": $(fname)
}""",
            saveKey=str(gid())))


if __name__ == "__main__":
    pass


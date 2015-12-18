#coding:utf-8
import _env
from os.path import exists, join
import os

def prepare(o):
    o.DEBUG = True

    o.PORT = 8942
    o.ADMIN_PORT = o.PORT + 42

    o.DISABLE_LOCAL_CACHED = False 

    #登录后 SEE YOUR USER ID IN https://42sso.sinaapp.com/
    o.MONGO_CONFIG = {
         #host = "mongodb://root:32dwwwzz49G@1.9.9.1:27017",
    }

    class SMTP:
        USERNAME = SENDER = 'postmaster@sandboxd36df46598b24c98a667970a291b5a34.mailgun.org'
        SENDER_NAME = '天使汇'
        HOST = 'smtp.mailgun.org'
        PORT = 25
        PASSWORD = 'IzUbyJALhH9rsGjk' # 在 SITE/misc/config/_host/vps你的机器编号.py 下面配置

    o.SMTP = SMTP

    class QINIU:

        ACCESS_KEY = 'U8Wfxvc49TE4xuL2sNpX_ZpMx5km3RGEwACRF3Hn'
        SECRET_KEY = 'Ynp5ll-X9aHbi3X2ok9yv56oxd6QpBmzhz0C0EXx'
        BUCKET = 'ac-test'
        HOST = 'ac-test.qiniudn.com'

    o.QINIU = QINIU

    class TWILIO:
        SID = ""
        TOKEN = ""

    o.TWILIO = TWILIO

    class SMS:
        ACCOUNT = '8a48b55147397601014742d5003003d9';

        #主帐号Token
        TOKEN= '8f168a8f8b5a4bf7bb2eae2844415134';

        #应用Id
        APP_ID = '8a48b55147397601014742dbf44703e3'

        TEMPLATE_ID = 1

        #请求地址
        URL ='https://sandboxapp.cloopen.com';

        #请求端口
        PORT ='8883';

        #REST版本号
        VERISON='2013-12-26';



    o.SMS = SMS

    o.BUGSNAG_KEY = ""
    o.TEST_MAIL = ''


def finish(o):
    if not o.DEBUG:
        import bugsnag
        bugsnag.configure( api_key = o.BUGSNAG_KEY , project_root = _env.PREFIX )



    o.TITLE = o.HOST

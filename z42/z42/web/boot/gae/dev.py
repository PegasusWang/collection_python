# coding:utf-8
from _env import PREFIX
from z42.config import HOST, PORT, ADMIN_PORT
import envoy
import sys

CMD = 'dev_appserver.py --host 0.0.0.0 --show_mail_body yes --enable_sendmail --skip_sdk_update_check --admin_host 0.0.0.0 --admin_port=%s  --port %s ' % (PORT+42, PORT)
if len(sys.argv) > 1 and sys.argv[1] == '-c':
    CMD += ' --clear_datastore=yes '
CMD += PREFIX
print CMD
print '# http://%s:%s'%(HOST, PORT)

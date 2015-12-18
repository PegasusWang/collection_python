# coding:utf-8
import _env
import json
#from z42.web.memcache import mc
import sys
import httplib
import traceback
import tornado
import tornado.web
from z42.config import APP
from os.path import join
from tornado.httpclient import HTTPClient, HTTPError
from z42.config import DEBUG
import yajl
from tornado import escape

def json_encode(value):
    """JSON-encodes the given Python object."""
    # JSON permits but does not require forward slashes to be escaped.
    # This is useful when json data is emitted in a <script> tag
    # in HTML, as it prevents </script> tags from prematurely terminating
    # the javscript.  Some json libraries do this escaping by default,
    # although python's standard library does not, so we do it here.
    # http://stackoverflow.com/questions/1580647/json-why-are-forward-slashes-escaped
    try:
        s = yajl.dumps(value)
    except:
        s = json.dumps(value, ensure_ascii=False)
    return s.replace("</", "<\\/")

escape.json_encode = json_encode
#    if not self._finished:
#        self.finish()



def write_error(self, status_code, **kwargs):
    if status_code == 404:
        from z42.web.render import render as _render
        import js
        import css
        path = join(APP, '_base/404.html')
        html = _render(path, css=css, js=js)
        return self.write(html)
    if self.settings.get('debug') and ('exc_info' in kwargs or 'exception' in kwargs):
        # in debug mode, try to send a traceback
        self.set_header('Content-Type', 'text/plain')
        for line in traceback.format_exception(*sys.exc_info()):
            self.write(line)
    else:
        message = kwargs.get('message', httplib.responses[status_code])
        html = '<html><title>%(code)s : %(message)s</title><body>%(code)s : %(message)s</body></html>' % {
                'code': status_code,
                'message': message,
                }
        self.write(html)

tornado.web.RequestHandler.write_error = write_error 

if DEBUG:
    RequestHandler = tornado.web.RequestHandler
else:
    from z42.config import BUGSNAG_KEY
    import bugsnag
    bugsnag.configure( api_key = BUGSNAG_KEY , project_root = _env.PREFIX )

    from tornado.web import RequestHandler as _RequestHandler
    from tornado.web import HTTPError
    import bugsnag


    class RequestHandler(_RequestHandler):
        def _handle_request_exception(self, exc):

            options = {
                "user": {"ip": self.request.remote_ip, "id": getattr(self, "current_user_id", 0)},
                "context": self._get_context(),
                "request": {
                    "url": self.request.full_url(),
                    "method": self.request.method,
                    "arguments": self.request.arguments,
                }
            }

            # Notify bugsnag, unless it's an HTTPError that we specifically want to ignore
            should_notify_bugsnag = True
            if type(exc) == HTTPError:
                if (exc.status_code<500 and exc.status_code>=400):
                    should_notify_bugsnag = False

            if should_notify_bugsnag:
                bugsnag.auto_notify(exc, **options)

            # Call the parent handler
            _RequestHandler._handle_request_exception(self, exc)

        def _get_context(self):
            return "%s %s" % (self.request.method, self.request.uri.split('?')[0])

class View(RequestHandler):
    def prepare(self):
        #mc.reset()
        super(View, self).prepare()

    def decode_argument(self, value, name=None):
        return value

    def redirect(self, url, permanent=False):
        """Sends a redirect to the given (optionally relative) URL."""
        if self._headers_written:
            raise Exception('Cannot redirect after headers have been written')
        self.set_status(301 if permanent else 302)
        self.set_header('Location', url)
        self.finish()

    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            #if self.request.method not in ('GET', 'HEAD', 'OPTIONS') and \
            #   self.application.settings.get('xsrf_cookies'):
            #    self.check_xsrf_cookie()
            self.prepare()
            if not self._finished:
                args = [self.decode_argument(arg) for arg in args]
                kwargs = dict((k, self.decode_argument(v, name=k))
                              for (k, v) in kwargs.iteritems())
                if hasattr(self, 'init'):
                    getattr(self, 'init')(*args, **kwargs)
                getattr(self, self.request.method.lower())(*args, **kwargs)
                if self._auto_finish and not self._finished:
                    self.finish()
        except Exception, e:
            self._handle_request_exception(e)


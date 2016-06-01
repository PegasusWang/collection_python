# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urlparse,gettext,threading,locale, collections, __builtin__
import logging,os,functools
import simplejson as json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError, asynchronous
from tornado.httpclient import HTTPRequest
from tornado.options import define, options
import mako.lookup
import mako.template
try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import SimpleAsyncHTTPClient as AsyncHTTPClient
relpath = lambda *a: os.path.join(os.path.dirname(__file__), *a)

SERVER_EN, SERVER_CN = range(2)
SERVER_LANG = SERVER_CN

LOCALE_ROOT = relpath('locales')
DEFAULT_LANG = 'zh_CN' if SERVER_LANG==SERVER_CN else 'en'

class Translator(collections.defaultdict):
    def __missing__(self, key):
        return gettext.translation('messages', LOCALE_ROOT, [key, 'en'])
translations = Translator()

class LocaleObject(threading.local):
    def __init__(self):
        self._lang = DEFAULT_LANG
    def setlang(self, lang):
        self._lang = lang or DEFAULT_LANG
    def getlang(self):
        return self._lang
    lang = property(getlang,setlang)
    def translate(self, s, lang=None):
        if not s: return ''
        ret = translations[lang or self._lang].gettext(s)
        if type(ret) is unicode: ret = ret.encode('utf8','ignore')
        return ret
i18n = LocaleObject()


__builtin__.__dict__['_'] = i18n.translate



define("port", default=8888, help="run on the given port", type=int)
define("api_protocol", default="http", help="proxy server protocol")
define("api_host", default="pre3.papayamobile.com", help="proxy server host")
define("api_port", default="1201", help="proxy server port")
define("api_path", default="",type=str, help="proxy router map local file path")
define("debug", default=True, type=bool, help="use debug")
define("path", default="", help="your project path")

SETTINGS={
    "static_path":None,
    "API_SETTINGS":{},
    "STATIC_SETTINGS":{},
    "MAIN_SETTINGS":{},
    "cookie_secret": "cxP6yKNYQZyhAtJ5/1gxCq1BCwD+qUnzqiHHYt2GvNY="
    }

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, file_name):
        self.file_name = file_name

    def get(self):
        self.render(self.file_name)

class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self):
        template_path = relpath() #self.get_template_path()

        self.lookup = mako.lookup.TemplateLookup(directories=[template_path], input_encoding='utf-8', output_encoding='utf-8',cache_enabled = False)

    def render_string(self, filename, **kwargs):
        template = self.lookup.get_template(filename)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)

    def render(self, filename, **kwargs):
        self.finish(self.render_string(filename, **kwargs))


    @asynchronous
    def get(self):
        # enable API GET request when debugging

        if options.debug:
            return self.post()
        else:
            raise HTTPError(405)

    @asynchronous
    def post(self):
        protocol = options.api_protocol
        host = options.api_host
        port = options.api_port

        # port suffix
        port = "" if port == "80" else ":%s" % port

        uri = self.request.uri

        url = "%s://%s%s%s" % (protocol, host, port, uri)

        # update host to destination host
        headers = dict(self.request.headers)
        #headers["Host"] = self.request.host
        headers["If-Appflood-Api"] = "true"
        try:
            a=AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            request_timeout=120000,
                            follow_redirects=False),
                self._on_proxy)

        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)


    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            host=self.request.host
            content_json=False
            data=dict()
            tmpl_path=''
            for header in response.headers.keys():
                v = response.headers.get(header)
                if header=='Location' and v:
                    uri=list(urlparse.urlparse(v))
                    if uri[1]==options.api_host:
                        uri[1]=host
                    v=urlparse.urlunparse(uri)
                    self.set_header(header, v)
                    return self.finish()

                if v and header!='Content-Length':
                    self.set_header(header, v)
                if header=='Content-Type' and v.find('json')>-1:
                    content_json=True

		if content_json==False or content_json==True:
                    print response.body
                    try:
                        data=json.loads(response.body)
                        if data.get('G',None):i18n.setlang(data['G']['lang'])
                        data["_"] = i18n.translate
                        tg_tmpl=data.get('tg_template',None)
                        if tg_tmpl:
                            tmpl_path=tg_tmpl[tg_tmpl.find('templates'):].replace('.','/')+'.mako';
                        else:
                            self.set_header('Content-Type','application/json');
                            #return self.finish(response.body)
                    except Exception, e:
                        print e
                        #return self.finish(response.body)

            if tmpl_path:
                self.render(tmpl_path,**data)

            if response.body:
                self.write(response.body)
            self.finish()





def main():
    tornado.options.parse_command_line()
    i18n.LOCALE_ROOT=relpath('locales')
    #static_path=options.path+'static/'
    urls=[]
    path_settings=json.loads(open('urls.json').read())
    SETTINGS["API_SETTINGS"]=path_settings.get('mako',{})
    SETTINGS["STATIC_SETTINGS"]=path_settings.get('static',{})
    SETTINGS["MAIN_SETTINGS"]=path_settings.get('main',{})
    if len(SETTINGS["STATIC_SETTINGS"].keys()):
        for name in SETTINGS["STATIC_SETTINGS"].keys():
            value=SETTINGS["STATIC_SETTINGS"][name]
            urls.append((name,tornado.web.StaticFileHandler, {"path":value}))
        '''
        urls=[
            (r"/images/(.*)",tornado.web.StaticFileHandler, {"path": static_path+'images'}),
            (r"/js/(.*)",tornado.web.StaticFileHandler, {"path": static_path+'js'}),
            (r"/css/(.*)",tornado.web.StaticFileHandler, {"path": static_path+'css'}),
            (r"/fonts/(.*)",tornado.web.StaticFileHandler, {"path": static_path+'fonts'})
        ]
        '''

    if len(SETTINGS["MAIN_SETTINGS"].keys()):
        for name in SETTINGS["MAIN_SETTINGS"].keys():
            value=SETTINGS["MAIN_SETTINGS"][name]
            urls.append((name,MainHandler, {"file_name": options.path+value}))

    urls.append((r"/.*", ProxyHandler))
    application = tornado.web.Application(handlers =urls,**SETTINGS)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

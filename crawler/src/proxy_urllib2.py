#!/usr/bin/env python
# -*- coding:utf-8 -*-

from six.moves.urllib import request as urllib2
import logging, time, MySQLdb, random, socket, struct, httplib, ssl, itertools

__all__ = ['addr', 'handler', 'SocksException']

class SocksException(Exception):
    pass

class socksocket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, _sock=None):
        socket.socket.__init__(self,family,type,proto,_sock)
        self.__proxy = (None, None)
        self.__proxysockname = None
        self.__proxypeername = None

    def __recvall(self, bytes):
        data = ""
        while len(data) < bytes:
            buf = self.recv(bytes-len(data))
            if not buf: break
            data = data + buf
        if len(data) < bytes:
            raise SocksException()
        return data

    def setproxy(self, addr=None, port=None):
        self.__proxy = (addr, port)

    def __negotiatesocks5(self, destaddr, destport):
        req = '!jfq4#%@3f3(WC'
        try:
            ipaddr = socket.inet_aton(destaddr)
            req = req + ipaddr
        except socket.error:
            ipaddr = socket.inet_aton(socket.gethostbyname(destaddr))
            req = req + ipaddr
        req = req + struct.pack(">H",destport)
        self.sendall(req)

    def connect(self, destpair):
        if (type(destpair) in (list,tuple)==False) or (len(destpair)<2) or (type(destpair[0])!=str) or (type(destpair[1])!=int):
            raise SocksException()
        socket.socket.connect(self, (self.__proxy[0], self.__proxy[1]))
        self.__negotiatesocks5(destpair[0], destpair[1])

class SocksHTTPConnection(httplib.HTTPConnection):
    def __init__(self, saddr, sport, *args, **kwargs):
        self.proxyargs = (saddr, sport)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float) or isinstance(self.timeout, int):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        if self._tunnel_host:
            self._tunnel()

class SocksHTTPSConnection(httplib.HTTPSConnection):
    def __init__(self, saddr, sport, *args, **kwargs):
        self.proxyargs = (saddr, sport)
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float) or isinstance(self.timeout, int):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        if self._tunnel_host:
            self._tunnel()
        self.sock = ssl.wrap_socket(self.sock, self.key_file, self.cert_file)

class SocksHandler(urllib2.HTTPHandler, urllib2.HTTPSHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)
        urllib2.HTTPSHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksHTTPConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

    def https_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksHTTPSConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)


def get_random_proxy():
    db = MySQLdb.connect('app3.c0w2erpkwmkh.us-west-2.rds.amazonaws.com', 'proxy', 'p0r9o8x7y6!AXW', 'server')
    cur = db.cursor()
    cur.execute('select ip,port from proxy where status=0 and country= "USA"')
    ret = [tuple(i) for i in cur.fetchall()]   # (addr, ip) tuple list
    cur.close()
    db.close()
    return random.choice(ret)


def addr():
    db = MySQLdb.connect('app3.c0w2erpkwmkh.us-west-2.rds.amazonaws.com', 'proxy', 'p0r9o8x7y6!AXW', 'server')
    cur = db.cursor()
    cur.execute('select ip,port from proxy where status=0 and country= "USA"')
    ret = [tuple(i) for i in cur.fetchall()]   # (addr, ip) tuple list
    cur.close()
    db.close()
    while 1:
        yield random.choice(ret)


proxy_handler_iterator = itertools.starmap(SocksHandler, addr())


def proxy_get_html(*args, **kwargs):
    opener = urllib2.build_opener(next(proxy_handler_iterator))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3 12')]
    return opener.open(*args, **kwargs).read()

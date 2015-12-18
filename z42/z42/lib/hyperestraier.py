'''HyperEstraier
Hiroki Ohtani
"HyperEstraier Pure Python Implementation."
http://coderepos.org/share/wiki/PyHyperEstraier
'''


import StringIO
import base64
import httplib
import urllib
import urllib2
import re

__version__  = '0.10.10'
__author__ = "Hiroki Ohtani (liris.pp [at] gmail.com)"
__copyright__ = "Copyright (c) 2006 Hiroki Ohtani"
__license__ = "LGPL"


COMPATIBLE_WITH_09 = False

class HyperestraierError(Exception):
    '''Base exception for Hyperestraier client.'''

class Document(object):
    '''Document class for hyperestrair.
    '''
    __slots__ = ["attrs", "dtexts", "htexts", "kwords", "score",
                 "id"]
    def __init__(self, draft = None):
        '''constructor of document.
        draft is the hyperestraier document dump string.
        '''
        self.attrs = {}
        self.dtexts = []
        self.htexts = []
        self.kwords = {}
        self.score = -1
        self.id = -1

        if draft:
            lines = draft.splitlines()
            splitPos = lines.index("", 1)
            for line in lines[:splitPos]:
                if line.startswith("%"):
                    if line.startswith("%VECTOR\t"):
                        fields = line[len("%VECTOR\t"):].split("\t")
                        keys = fields[::2]
                        values = fields[1::2]
                        self.kwords = dict(zip(keys, values))
                    elif line.startswith("%SCORE\t"):
                        self.score = int(line.split("\t")[1])
                else:
                    line = _normalize(line)
                    fields = line.split("=", 1)
                    if len(fields) == 2:
                        self.attrs[fields[0]] = fields[1]

            for line in lines[splitPos+1:]:
                if line:
                    if line[0] == "\t":
                        self.htexts.append(line[1:])
                    else:
                        self.dtexts.append(line)


    def add_attr(self, name, value):
        '''add an attribute.
        name specifies the name of the attribute.
        value specifies the value of the attribute.
        If value is None, the attribute is removed.
        name and value  must be utf-8 encoding string or unicode.
        '''
        name = _normalize(name)
        value = _normalize(value)
        self.attrs[name] = value

    def add_text(self, text):
        '''Add a sentence of text.
        text specifies a sentence of text.
        text must be utf-8 encoding string or unicode.
        '''
        text = _normalize(text)
        if text:
            self.dtexts.append(text)

    def add_hidden_text(self, text):
        '''Add a hidden sentence of text.
        text specifies a hidden sentence of text.
        text must be utf-8 encoding string or unicode.
        '''
        text = _normalize(text)
        if text:
            self.htexts.append(text)

    def set_keywords(self, kwords):
        '''Attach keywords.
        kwrods specifieds a dictionary object.
        key of the dictionary should be keywords of the document
        and values shuuld be their scores in decimal string.
        '''
        self.kwords = kwords

    def set_score(self, score):
        '''set the substinute score.
        score specifies the substitute score.
        Negative value make the substitue score setting null.
        '''
        self.score = score

    def attr(self, name):
        '''get the value of the attribute.
        name specifies the name of an attribute.
        The return value is the value of the attribute or None if it does not exist.

        Please access 'attrs' object properity, directly for more pythonic.
        '''
        return self.attrs.setdefault(name, None)

    def attr_names(self):
        ''' Get the array of the attrube names of the document.
        The return value is an array object of the attribute name.
        '''
        l = self.attrs.keys()
        l.sort()
        return l

    def cat_texts(self):
        '''Concatenate the sentences of the text of the document.
        The return value is concatenated sentence.
        '''
        return " ".join(self.dtexts)

    def dump_draft(self):
        '''Dump draft data of the document.
        The return value is draft data(UTF-8 encoded string).
        '''
        buf = StringIO.StringIO()
        for key in self.attr_names():
            buf.write(u"%s=%s\n" % (key, _enc(self.attrs[key])))
        if self.kwords:
            buf.write("%%VECTO")
            for key, value in self.kwords.iteritems():
                buf.write(u"\t%s\t%s" % (key, value))
            buf.write("\n")
        if self.score >= 0:
            buf.write("%%SCORE\t%d\n"%self.score)
        buf.write("\n")
        if self.dtexts:
            buf.write("\n".join(self.dtexts))
            buf.write("\n")
        if self.htexts:
            buf.write("\t")
            buf.write("\n\t".join(self.htexts))
            buf.write("\n")
        #print buf.getvalue()
        return buf.getvalue().encode("utf-8")



class Condition(object):
    # option: check every N-gram key
    SURE = 1 << 0
    # option: check N-gram keys skipping by one
    USUAL = 1 << 1
    # option: check N-gram keys skipping by two
    FAST = 1 << 2
    # option: check N-gram keys skipping by three
    AGITO = 1 << 3
    # option: without TF-IDF tuning
    NOIDF = 1 << 4
    # option: with the simplified phrase
    SIMPLE = 1 << 10
    # option: with the rough phrase
    ROUGH = 1 << 11
    # option: with the union phrase
    UNION = 1 << 15
    # option: with the intersection phrase
    ISECT = 1 << 16

    def __init__(self):
        """
        create condtion object.
        """
        self.phrase = None
        self.attrs = []
        self.order = None
        self.max = -1
        self.skip = 0
        self.options = 0
        self.auxiliary = 32
        self.distinct = None
        self.mask = 0

    def set_phrase(self, phrase):
        """
        Set the search phrase.
        'phrase' specifies a search phrase.
        """
        phrase = _normalize(phrase)
        self.phrase = phrase

    def add_attr(self, expr):
        """
        Add an expression for an attribute
        'expr'  specifies an expression for an attribute.
        """
        expr = _normalize(expr)
        self.attrs.append(expr)

    def set_order(self, expr):
        """
        Set the order of a condition object.
        'expr' specifies an expression for the order.
        By default, the order is by score descending.
        """
        expr = _normalize(expr)
        self.order = expr

    def set_max(self, max):
        """
        Set the maximum number of retrieval.
        'max' specifies the maximum number of retrieval.
        By default, the number of retrieval is not limited.
        """
        if max >= 0:
            self.max = max

    def set_skip(self, skip):
        """
        Set the number of skipped documents.
        'skip' specifies the umber of documents to be skipped in the search result.
        """
        if skip >= 0:
            self.skip = skip

    def set_options(self, options):
        """
        Set options of retrieval.
        `options' specifies options:

        `Condition.SURE' specifies that it checks every N-gram key,

        `Condition.USUAL', which is the default,
        specifies that it checks N-gram keys with skipping one key,

        `Condition.FAST' skips two keys,

        `Condition.AGITO' skips three keys,

        `Condition.NOIDF' specifies not to perform TF-IDF tuning,

        `Condition.SIMPLE' specifies to use simplified phrase,

        `Condition.ROUGH' specifies to use rough phrase,

        `Condition.UNION' specifies to use union phrase,

        `Condition.ISECT' specifies to use intersection phrase.
        Each option can be specified at the same time by bitwise or.
        If keys are skipped, though search speed is improved,
        the relevance ratio grows less.
        """
        self.options |= options

    def set_auxiliary(self, min):
        """
        Set permission to adopt result of the auxiliary index.
        `min' specifies the minimum hits to adopt result of the auxiliary index.
        If it is not more than 0, the auxiliary index is not used.
        By default, it is 32.
        """
        self.auxiliary = min

    def set_distinct(self, name):
        """
        Set the attribute distinction filter.
        `name' specifies the name of an attribute to be distinct.
        """
        name = _normalize(name)
        self.distinct = name

    def set_mask(self, mask):
        """
        Set the mask of targets of meta search.
        `mask' specifies a masking number.
        1 means the first target,
        2 means the second target,
        4 means the third target,
        and power values of 2 and their summation compose the mask.
        """
        self.mask = mask

class ResultDocument(object):
    """ Abstraction of document in result set """
    def __init__(self, uri, attrs, snippet, keywords):
        self.attrs = attrs
        self.uri = uri
        self.snippet = snippet
        self.keywords = keywords

    def attr_names(self):
        """
        Get an array of attribute names.
        Return value is an string array of attribue names.
        """
        l = self.attrs.keys()
        l.sort()
        return l

    def attr(self, name):
        """
        Get the value of an attribute.
        The return value is the value of the attribute
        or None if it does not exists.
        """
        return self.attrs.get(name, None)

class NodeResult(object):
    """ Abstraction of result set from node. """
    def __init__(self, docs, hints):
        self.docs = docs
        self.hints = hints

    def doc_num(self):
        """
        Get the number of documents.
        The return value is the number of documents.
        """
        return len(self.docs)

    def get_doc(self, index):
        """
        Get the value of hint information.
        The return value is a result document object
        or None if the index is out of bounds.
        """
        if index < 0 or index >= self.doc_num():
            return None
        return self.docs[index]

    def hint(self, key):
        """
        Get the value of hint information.
        `key' specifies the key of a hint.
        'VERSION', 'NODE', 'HIT', 'HINT#n', 'DOCNUM', 'WORDNUM',
        'TIME', 'TIME#n', 'LINK#n', and 'VIEW' are provided for keys.
        The return value is the hint or None if the key does not exist.
        """
        return self.hints[key]


def _success(result):
    return True

def _err(result):
    if not COMPATIBLE_WITH_09:
        raise HyperestraierError(result)
    else:
        return False


class UrlNotSpecifiedException(Exception):
    pass

class Transport(object):
    def __init__(self):
        self.url = None
        self.pxhost = None
        self.pxport = 0
        self.timeout = 0
        self.auth = None

    def extract(self, callback):
        return callback(None)

    def sendAndExtract(self, command, callback, errback, extractCallback,
                       headers = {}, body=None, autoContentType = True):
        result = self.send(command, callback, errback,
                           headers, body, autoContentType)
        return extractCallback(result)

    def send(self, command, callback, errback,
             headers = {}, body=None, autoContentType = True):
        # return self._send(command, headers, body)
        try:
            status, result = self._send(command, headers, body)
            return callback(result)
        except urllib2.HTTPError, e:
            status, result = e.code, str(e)
        except Exception, e:
            status, result =  -1, str(e)
        return errback(result)


    def _send(self, command, headers = {}, body=None, autoContentType=True):
        if not self.url:
            raise UrlNotSpecifiedException

        url = self.url + "/" + command
        headers = headers.copy()
        if "Content-Type" not in headers and autoContentType:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        if self.auth:
            encodedAuth = base64.encodestring(self.auth).replace("\n", "")
            headers["Authorization"] = "Basic " + encodedAuth
        if body:
            headers["Content-Length"] = "%d" % len(body)
        headers["User-Agent"] = "HyperEstraierForPython/1.0.0"

        # TODO: set timeout
        request = urllib2.Request(url)
        if self.pxhost and self.pxport:
            request.set_proxy(self.pxhost, self.pxport)
        request.add_data(body)
        for k,v in headers.iteritems():
            request.add_header(k, v)
        response = urllib2.urlopen(request)
        result = response.read()
        code = response.code

        return code, result.decode("utf-8", "replace")

try:
    from twisted.internet import defer, reactor
    from twisted.web.client import getPage

    def unicodeFromUTF8(result):
        return result.decode("utf-8")

    class AsynTransport(object):
        """
        Asynchornous hyperestraier support.
        If you use this transport,
        All Node API can run asynchonously and always return deferred object.
        """
        def __init__(self):
            self.url = None
            self.pxhost = None
            self.pxport = 0
            self.timeout = 0
            self.auth = None

        def extract(self, callback):
            deferred = defer.Deferred()
            def _f():
                deferred.callback(callback(None))

            reactor.callLater(0, _f)
            return deferred

        def sendAndExtract(self, command, callback, errback, extractCallback,
                 headers = {}, body=None, autoContentType = True):
            deferred = self.send(command, callback, errback,
                               headers, body, autoContentType)
            return deferred.addCallback(extractCallback)

        def send(self, command, callback, errback,
                 headers = {}, body=None, autoContentType = True):
            if not self.url:
                raise UrlNotSpecifiedException

            headers = headers.copy()
            url = self.url + "/" + command
            if not headers.has_key("Content-Type") and autoContentType:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            if self.auth:
                encodedAuth = base64.encodestring(self.auth).replace("\n", "")
                headers["Authorization"] = "Basic " + encodedAuth
            if body:
                headers["Content-Length"] = "%d" % len(body)
            headers["User-Agent"] = "HyperEstraierForPython/1.0.0"

            deferred = getPage(url, method = (body and "POST" or "GET"),
                               headers = headers, postdata = body)
            deferred.addCallback(
                unicodeFromUTF8).addCallback(
                callback).addErrback(
                errback)
            return deferred



except:
    pass

class Node(object):
    """
    Abstraction of connection to P2P node.
    """
    def __init__(self, transport = None):
        if transport:
            self.transport = transport
        else:
            self.transport = Transport()
        self.name = None
        self.label = None
        self.dnum = -1
        self.wnum = -1
        self.size = -1.0
        self.admins = None
        self.users = None
        self.links = None
        self.wwidth = 480
        self.hwidth = 96
        self.awidth = 96

    def set_url(self, url):
        """
        Set the URL of a node server.
        `url' specifies the URL of a node.
        """
        self.transport.url = url

    def set_proxy(self, host, port):
        """
        Set the proxy information.
        `host' specifies the host name of a proxy server.
        `port' specifies the port number of the proxy server.
        """
        self.transport.pxhost = host
        self.transport.pxport = port

    def set_timeout(self, sec):
        """
        Set timeout of a connection.
        `sec' specifies timeout of the connection in seconds.
        """
        self.transport.timeout = sec

    def set_auth(self, name, password):
        """
        Set the authentication information.
        `name' specifies the name of authentication.
        `passwd' specifies the password of the authentication.
        """
        self.transport.auth = ":".join((name, password))

    def sync(self):
        """
        Synchronize updating contents of the database.
        The return value is True if success, else it is False.
        """
        return  self.transport.send("sync", _success, _err)


    def optimize(self):
        """
        Optimize the database.
        The return value is True if success, else it is False.
        """
        return self.transport.send("optimize", _success, _err)


    def put_doc(self, doc):
        """
        Add a document.
        `doc' specifies a document object.
        The document object should have the URI attribute.
        The return value is True if success, else it is False.
        """
        return  self.transport.send(
            "put_doc",
            _success, _err,
            {"Content-Type":"text/x-estraier-draft"},
            doc.dump_draft())

    def out_doc(self, id):
        """
        Remove a document.
        `id' specifies the ID number of a registered document.
        The return value is True if success, else it is False.
        """
        return self.transport.send(
            "out_doc",
            _success, _err,
            body = "id=" + str(id))

    def out_doc_by_uri(self, uri):
        """
        Remove a document specified by URI.
        `uri' specifies the URI of a registered document.
        The return value is True if success, else it is False.
        """
        body = "uri=" + _escape(uri)
        return self.transport.send(
            "out_doc",
            _success, _err,
            body = body)

    def edit_doc(self, doc):
        """
        Edit attributes of a document.
        `doc' specifies a document object.
        The return value is True if success, else it is False.
        """
        return self.transport.send(
            "edit_doc",
            _success, _err,
            {"Content-Type":"text/x-estraier-draft"},
            doc.dump_draft())

    def get_doc(self, id):
        """
        Retrieve a document.
        `id' specifies the ID number of a registered document.
        The return value is a document object.  On error, None is returned.
        """
        body = "id=" + str(id)
        def success(result):
            return Document(result)

        def err(result):
            return None

        return self.transport.send("get_doc", success, err, body = body)

    def get_doc_by_uri(self, uri):
        """
        Retrieve a document.
        `uri' specifies the URI of a registered document.
        The return value is a document object.  On error, None is returned.
        """
        body = "uri=" + _escape(uri)
        def success(result):
            return Document(result)

        def err(result):
            return None

        return  self.transport.send("get_doc", success, err, body = body)

    def get_doc_attr(self, id, name):
        """
        Retrieve the value of an attribute of a document.
        `id' specifies the ID number of a registered document.
        `name' specifies the name of an attribute.
        The return value is the value of the attribute
        or None if it does not exist.
        """
        body = "id=" + str(id) + "&attr=" + _escape(name)
        def success(result):
            return result.strip()

        def err(result):
            return None

        return self.transport.send("get_doc_attr", success, err, body = body)

    def get_doc_attr_by_uri(self, uri, name):
        """
        Retrieve the value of an attribute of a document specified by URI.
        `uri' specifies the URI of a registered document.
        `name' specifies the name of an attribute.
        The return value is the value of the attribute
        or None if it does not exist.
        """
        body = "uri=" + _escape(uri) + "&attr=" + _escape(name)
        def success(result):
            return result.strip()

        def err(result):
            return None

        return self.transport.send("get_doc_attr", success, err, body = body)

    def etch_doc(self, id):
        """
        Extract keywords of a document.
        `id' specifies the ID number of a registered document.
        The return value is a hash object of keywords and their scores in decimal string
        or None on error.
        """
        body = "id=" + str(id)
        def success(result):
            kwords = {}
            for line in result.splitlines():
                pair = line.split("\t")
                if len(pair) > 1:
                    kwords[pair[0]] = pair[1]
            return kwords

        def err(result):
            return None

        return self.transport.send("etch_doc", success, err, body = body)

    def etch_doc_by_uri(self, uri):
        """
        Extract keywords of a document specified by URI.
        `uri' specifies the URI of a registered document.
        The return value is a hash object of keywords and their scores in decimal string
        or None on error.
        """
        body = "uri=" + _escape(uri)
        def success(result):
            kwords = {}
            for line in result.splitlines():
                pair = line.split("\t")
                if len(pair) > 1:
                    kwords[pair[0]] = pair[1]
            return kwords

        def err(result):
            return None

        return self.transport.send("etch_doc", success, err, body = body)

    def uri_to_id(self, uri):
        """
        Get the ID of a document specified by URI.
        `uri' specifies the URI of a registered document.
        The return value is the ID of the document.  On error, -1 is returned.
        """
        body = "uri=" + _escape(uri)
        def success(result):
            return int(result)
        def err(result):
            return None

        return  self.transport.send("uri_to_id", success, err, body = body)

    def get_name(self):
        """
        Get the name.
        The return value is the name.  On error, None is returned.
        """
        def get(result):
            return self.name

        if self.name == None:
            return self._set_info(get)
        #return self.name
        return self.transport.extract(get)

    def get_label(self):
        """
        Get the label.
        The return value is the label.  On error, None is returned.
        """
        def get(result):
            return self.label

        if self.label == None:
            self._set_info(get)
        return self.transport.extract(get)

    def get_doc_num(self):
        """
        Get the number of documents.
        The return value is the number of documents.  On error, -1 is returned.
        """
        def get(result):
            return self.dnum

        if self.dnum < 0:
            return self._set_info(get)
        return self.transport.extract(get)

    def get_word_num(self):
        """
        Get the number of unique words.
        The return value is the number of unique words.  On error, -1 is returned.
        """
        def get(result):
            return self.wnum

        if self.wnum < 0:
            return self._set_info(get)
        return self.transport.extract(get)

    def get_size(self):
        """
        Get the size of the datbase.
        The return value is the size of the datbase.  On error, -1.0 is returned.
        """
        def get(result):
            return self.size

        if self.size < 0:
            return self._set_info(get)
        return self.transport.extract(get)

    def get_cache_usage(self):
        """
        Get the usage ratio of the cache.
        The return value is the usage ratio of the cache.
        On error, -1.0 is returned.
        """
        def err(result):
            return -1.0

        def success(result):
            return float(result)

        return self.transport.send("cacheusage",
                                   success, err,
                                   autoContentType = False)

    def get_admins(self):
        """
        Get an array of names of administrators.
        The return value is an array object of names of administrators.
        On error, None is returned.
        """
        def get(result):
            return self.admins

        if self.admins != None:
            return self._set_info(get)
        return self.transport.extract(get)

    def get_users(self):
        """
        Get an array of names of users.
        The return value is an array object of names of users.
        On error, None is returned.
        """
        def get(result):
            return self.users

        if self.users != None:
            return self._set_info(get)
        return self.transport.extract(get)

    def get_links(self):
        """
        Get an array of expressions of links.
        The return value is an array object of expressions of links.
        Each element is a TSV string and has three fields of
        the URL, the label, and the score.
        On error, None is returned.
        """
        def get(result):
            return self.links

        if self.links != None:
            return self._set_info(get)
        return self.transport.extract(get)

    def search(self, condition, depth = 0):
        """
        Search for documents corresponding a condition.
        `cond' specifies a condition object.
        `depth' specifies the depth of meta search.
        The return value is a node result object.  On error, None is returned.
        """
        def success(result):
            lines = result.splitlines()
            docs = []
            hints = {}
            nres = NodeResult(docs, hints)
            border = lines.pop(0)
            sections = result.split(border)
            if len(sections) < 3:
                return None
            sections = sections[1:-1]
            ehits = 0
            for line in sections[0].splitlines():
                elems = line.split("\t", 1)
                if len(elems) == 2:
                    hints[elems[0]] = elems[1]
                    if 'HIT' == elems[0]:
                        ehits = int(elems[1])
            for section in sections[1:]:
                lines = [line.strip() for line in section.splitlines()]
                if len(lines) < 4:
                    return None
                if lines[0] == '':
                    del lines[0]
                if lines[-1] == '':
                    del lines[-1]
                section = '\n'.join(lines)
                _split = section.split('\n\n', 1)
                if len(_split) != 2:
                    return None
                rdlines = _split[0].splitlines()
                sb = _split[1].splitlines()
                rdattrs = {}
                rdvector = ""
                for rdline in rdlines:
                    if rdline.startswith("%"):
                        vecelem = rdline.split("\t", 1)
                        if len(vecelem) == 2 and vecelem[0] == "%VECTOR":
                            rdvector = vecelem[1]
                    else:
                        elems = rdline.split("=", 1)
                        if len(elems)==2:
                            rdattrs[elems[0]] = elems[1]

                rduri = rdattrs.setdefault("@uri", None)
                rdsnippet = "\n".join(sb)
                if rduri:
                    rdoc = ResultDocument(rduri, rdattrs, rdsnippet, rdvector)
                    docs.append(rdoc)

            return nres

        def err(resutl):
            return None

        body = _condToQuery(condition, depth,
                                self.wwidth, self.hwidth, self.awidth)
        return self.transport.send("search", success, err, body=body)


    def set_snippet_width(self, wwidth, hwidth, awidth):
        """
        Set width of snippet in the result.
        `wwidth' specifies whole width of a snippet.
        By default, it is 480.  If it is 0, no snippet is sent.
        If it is negative, whole body text is sent instead of snippet.
        `hwidth' specifies width of strings picked up
        from the beginning of the text.
        By default, it is 96.
        If it is negative 0, the current setting is not changed.
        `awidth' specifies width of strings picked up around each highlighted word.
        By default, it is 96.
        If it is negative, the current setting is not changed.
        """
        self.wwidth = wwidth
        if hwidth >= 0:
            self.hwidth = hwidth
        if awidth >= 0:
            self.awidth = awidth

    def set_user(self, user, mode):
        """
        Manage a user account of a node.
        `name' specifies the name of a user.
        `mode' specifies the operation mode.
        0 means to delete the account.
        1 means to set the account as an administrator.
        2 means to set the account as a guest.
        The return value is true if success, else it is false.
        """
        body = "name=" + _escape(name) + "&mode=" + str(mode)
        return self.transport.send("_set_user", _success, _err, body=body)

    def set_link(self, url, label, credit):
        """
        Manage a link of a node.
        `url' specifies the URL of the target node of a link.
        `label' specifies the label of the link.
        `credit' specifies the credit of the link.
        If it is negative, the link is removed.
        The return value is true if success, else it is false.
        """
        body = "url=" + _escape(url) + "&label=" + label
        if credit >= 0:
            body += "&credit=" + str(credit)

        return self.transport.send("_set_link", _success, _err, body=body)

    def _set_info(self, callback):
        def err(result):
            pass

        def success(result):
            lines = result.splitlines()
            line = lines.pop(0)
            elems = line.split("\t")
            if len(elems) != 5:
                return
            self.name = elems[0]
            self.label = elems[1]
            self.dnum = int(elems[2])
            self.wnum = int(elems[2])
            self.size = int(elems[2])


            self.admins = []
            self.users = []
            self.links = []
            currentScope = (self.admins, lambda x: x)
            remainQueue = [(self.users, lambda x: x),
                           (self.links, lambda x: x.split("\t", 3))]
            for line in lines:
                if not line:
                    if len(remainQueue):
                        currentScope = remainQueue.pop(0)
                    else:
                        break
                else:
                    currentScope[0].append(currentScope[1](line))

            return self


        return  self.transport.sendAndExtract("inform",
                                              success, err, callback,
                                              autoContentType = False)


SNIP_PATTERN = re.compile(u"[ \t\r\n\v\f]+")
SPC_PATTERN = re.compile(u" +")
def _normalize(value):
    if type(value) == str:
        value = value.decode("utf-8")
    value = SNIP_PATTERN.sub(u" ", value)
    value = SPC_PATTERN.sub(u" ", value)
    return value

def _condToQuery(cond, depth, wwidth, hwidth, awidth):
    buf = []
    if cond.phrase:
        buf.append(("phrase", _escape(cond.phrase)))
    for i in range(0, len(cond.attrs)):
        buf.append(("attr" + str(i+1), _escape(cond.attrs[i])))
    if cond.order:
        buf.append(("order", _escape(cond.order)))
    if cond.max >= 0:
        buf.append(("max", str(cond.max)))
    else:
        buf.append(("max", str(1<<30)))
    if cond.options > 0:
        buf.append(("options", str(cond.options)))
    buf.append(("auxiliary", str(cond.auxiliary)))
    if cond.distinct:
        buf.append(("distinct", _escape(cond.distinct)))
    if depth>0:
        buf.append(("depth", str(depth)))
    buf.append(("wwidth", str(wwidth)))
    buf.append(("hwidth", str(hwidth)))
    buf.append(("awidth", str(awidth)))
    buf.append(("skip", str(cond.skip)))
    buf.append(("mask", str(cond.mask)))

    return "&".join(["%s=%s" % (e[0], e[1]) for e in buf])

def _escape(s):
    if type(s) == unicode:
        s = s.encode("utf-8")
    return urllib.quote(s)


def _enc(s):
    return s
#     if type(s) == str:
#         s = s.decode("utf-8")
#     return s

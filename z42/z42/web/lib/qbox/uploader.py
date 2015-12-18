# -*- encoding: utf-8 -*-

import json
import requests
import urllib
import urllib2
from base64 import urlsafe_b64encode
import config
from token import QINIU_TOKEN
from json import loads
import mimetypes
from os.path import basename

class Qbox(object):
    def __init__(self, token):
        self._token = token 
        self.scope = token._scope

    @property
    def token(self):
        t = self._token.new()
        return t

    def put(self, key, data, mimetype=None):
        if mimetype is None:
            mimetype = mimetypes.guess_type(key)[0] or ''
        scope = self.scope
        entryURI = scope + ':' + key
        action = '/rs-put/' + urlsafe_b64encode(entryURI) + '/mimeType/' + urlsafe_b64encode(mimetype)
        params = {'action': action}
        params['auth'] = self.token
        url = config.UP_HOST + '/upload'
        r = requests.post(url, params, files={
            'file':('0', data)
        })
        return json.loads(r.text)

    def upload(self, key, path, mimetype=None):
        if not mimetype:
            mimetype = mimetypes.guess_type(basename(path))[0] or ''
        with open(path, 'rb') as f:
            return self.put(key, f.read(), mimetype)


    def upload_data(self, key, data, mimetype=None, callback=None):
        if mimetype is None:
            mimetype = mimetypes.guess_type(key)[0] or ''

        return self.put(key, data, mimetype)


    def rm(self, key):
        scope = self.scope
        entryURI = scope + ':' + key
        url = config.UP_HOST + '/delete/'+urlsafe_b64encode(entryURI)
        headers = {'Authorization':self.token}
        return requests.post(url, headers=headers)


QINIU = Qbox(QINIU_TOKEN)



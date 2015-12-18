# -*- coding: utf-8 -*-

from tornado import gen
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.concurrent import Future
from tornado.auth import OAuth2Mixin, _auth_return_future, AuthError

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    import urllib.parse as urllib_parse
except ImportError:
    import urllib as urllib_parse

class WeiboMixin(OAuth2Mixin):
    """
    class AuthHandler(tornado.web.RequestHandler, WeiboMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='YOUR_REDIRECT_URI',
                client_id=self.settings['weibo_api_key'],
                client_secret=self.settings['weibo_api_secret'],
                code=self.get_argument('code'))
            self.render('weibo.html', user=user)
        else:
            self.authorize_redirect(
                redirect_uri='YOUR_REDIRECT_URI',
                client_id=self.settings['weibo_api_key']
                )

    """

    _OAUTH_ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    _OAUTH_AUTHORIZE_URL = 'https://api.weibo.com/oauth2/authorize?'
    
    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, grant_type='authorization_code', extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            }

        fields = set(['id', 'screen_name', 'profile_image_url'])

        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL, method='POST', 
                   body=urllib_parse.urlencode(args),
                   callback=lambda res : self._on_access_token(redirect_uri, client_id, client_secret, callback, fields, res))

    def _oauth_request_token_url(self, redirect_uri=None, client_id=None,
                                 client_secret=None, code=None,
                                 grant_type=None, extra_params=None):
        pass

    
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Weibo auth error %s' % str(response)))
            return

        args = escape.json_decode(escape.native_str(response.body))
        session = {
            'access_token': args['access_token'],
            'expires': args['expires_in'],
            'uid': args['uid'],
            }

        self.weibo_request(
            path='/users/show.json',
            callback=lambda user:self._on_get_user_info(future, session['expires'], session['access_token'], user),
            access_token=session['access_token'],
            uid=session['uid']
            )

    def _on_get_user_info(self, future, expires_in, access_token, user):
        if user is None:
            future.set_result(None)
            return

        user["access_token"] = access_token
        user["expires_in"] = expires_in
        future.set_result(user)

    @_auth_return_future
    def weibo_request(self, path, callback, access_token=None, uid=None, post_args=None, **args):
        url = "https://api.weibo.com/2" + path
        all_args = {}
        if access_token:
            all_args['access_token'] = access_token
        if uid:
            all_args['uid'] = uid
        if args:
            all_args.update(args)

        if all_args:
            url += '?' + urllib_parse.urlencode(all_args)
        wrapped_callback  = lambda res : self._on_weibo_request(callback, res)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=wrapped_callback)

    def _on_weibo_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response %s fetching %s',
                                           response.error, response.request.url))

            return

        future.set_result(escape.json_decode(response.body))
    
    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()

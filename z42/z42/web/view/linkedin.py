from tornado import auth, httpclient, httputil, escape
import urllib
from zapp.ANGELCRUNCH.model.host import host_id_by_host
from zapp.ANGELCRUNCH.model.ob import Ob


class LinkedInMixin(auth.OAuth2Mixin):
    """
    LinkedIn authentication using OAuth2.

    Example usage::

        class LinkedInLoginHandler(LoginHandler, LinkedInMixin):
            @tornado.gen.coroutine
            def get(self):
                code = self.get_argument("code", None)
                redirect_uri = "%s://%s%s" % (self.request.protocol, self.request.host, self.request.path)

                if not code:
                    # Generate a random state
                    state = binascii.b2a_hex(os.urandom(15))

                    self.set_secure_cookie("linkedin_state", state)

                    yield self.authorize_redirect(
                        redirect_uri=redirect_uri,
                        client_id=self.settings["linkedin_client_id"],
                        extra_params={
                            "response_type": "code",
                            "state": state,
                            "scope": "r_basicprofile r_emailaddress"
                        }
                    )

                    return

                # Validate the state
                if self.get_argument("state", None) != self.get_secure_cookie("linkedin_state"):
                    raise tornado.web.HTTPError(400, "Invalid state")

                user_data = yield self.get_authenticated_user(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["linkedin_client_id"],
                    client_secret=self.settings["linkedin_client_secret"],
                    code=code,
                    extra_fields=["formatted-name", "email-address"]
                )

                if not user_data:
                    raise tornado.web.HTTPError(400, "LinkedIn authentication failed")

                # Handle authenticated user
    """
    _OAUTH_ACCESS_TOKEN_URL = "https://www.linkedin.com/uas/oauth2/accessToken?"
    _OAUTH_AUTHORIZE_URL = "https://www.linkedin.com/uas/oauth2/authorization?"
    _OAUTH_NO_CALLBACKS = False


    @auth._auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, extra_fields=None):
        http = httpclient.AsyncHTTPClient()

        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "extra_params": {
                "grant_type": "authorization_code"
            }
        }

        fields = set(['id'])

        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._oauth_request_token_url(**args), method="POST", body="",
                callback=lambda response:self._on_access_token(redirect_uri, client_id, client_secret, callback, fields, response))

    def _on_access_token(self, redirect_uri, client_id, client_secret, future, fields, response):
        if response.error:
            future.set_exception(auth.AuthError('LinkedIn auth error (%s): %s' % (response.code, response.body)))
            return

        args = escape.json_decode(response.body)
        expires_in = args["expires_in"]
        access_token = args["access_token"]

        self.linkedin_request(
            path="/v1/people/~:(%s)" % ",".join(fields),
            callback=lambda user:self._on_get_user_info(future, expires_in, access_token, user),
            access_token=access_token,
        )

    def _on_get_user_info(self, future, expires_in, access_token, user):
        if user is None:
            future.set_result(None)
            return

        user["access_token"] = access_token
        user["expires_in"] = expires_in
        future.set_result(user)

    @auth._auth_return_future
    def linkedin_request(self, path, callback, method="GET", access_token=None, post_args=None, query_args=None):
        url = "https://api.linkedin.com" + path

        # Build the query parameters
        all_query_args = dict(query_args or {})

        if access_token:
            all_query_args["oauth2_access_token"] = access_token

        if all_query_args:
            url += "?" + urllib.urlencode(all_query_args)

        # Build the request body. Empty bodies must be either set to an empty
        # string or None based on the request method. This is because the
        # Tornado HTTP client aggressively throws errors based on the request
        # method / body content combination.
        if self.request.method in ("POST", "PATCH", "PUT"):
            if post_args:
                body = urllib.urlencode(post_args)
            else:
                body = ""
        else:
            body = None

        wrapped_callback = lambda response : self._on_linkedin_request(callback, response)
        http = httpclient.AsyncHTTPClient()

        # Ask linkedin to send us JSON on all API calls (not xml)
        headers = httputil.HTTPHeaders({"x-li-format":"json"})

        http.fetch(url, method=method, headers=headers, body=body, callback=wrapped_callback)

    def _on_linkedin_request(self, future, response):
        if response.error:
            future.set_exception(auth.AuthError("LinkedIn error (%s) when requesting %s: %s" % (response.code, response.request.url, response.body)))
        else:
            future.set_result(escape.json_decode(response.body))

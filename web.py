from __future__ import absolute_import, division, print_function, with_statement

import json
import urllib
import urllib2
import traceback

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import abort
from werkzeug.exceptions import HTTPException
from werkzeug.utils import redirect

from . import conf


urls = {
    '/'       : 'index',
    '/oauth2' : 'oauth2',
}
router = Map([ Rule(key, endpoint=urls[key]) for key in urls ])


class App(object):
    def __init__(self):
        self._access_token = conf.WEIBO_TOKEN

    def dispatch_request(self, request):
        adapter = router.bind_to_environ(request.environ)

        endpoint, values = adapter.match()
        return getattr(self, endpoint)(request, **values)

    def wsgi(self, environ, start_response):
        try:
            request = Request(environ)
            response = self.dispatch_request(request)

            return response(environ, start_response)
        except HTTPException as e:
            return e(environ, start_response)
        except Exception as e:
            traceback.print_exc()
            abort(500)

    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)

    def index(self, request, *args, **kwargs):
        return Response('OK')

    def oauth2(self, request, *args, **kwargs):
        if request.args.get('error'):
            return redirect('/')
        elif request.args.get('code'):
            _code = request.args['code']
            _api = 'https://api.weibo.com/oauth2/access_token'
            _params = {
                'client_id': conf.WEIBO_KEY,
                'client_secret': conf.WEIBO_SECRET,
                'grant_type': 'authorization_code',
                'code': _code,
                'redirect_uri': conf.OAUTH2_URL,
            }

            try:
                res = urllib2.urlopen(_api, urllib.urlencode(_params), timeout=10)
                data = json.load(res)

                assert not data.get('error_code')
                assert data['uid'] == conf.WEIBO_UID

                self._access_token = data['access_token']

                return Response('OAuth2 Success: %s' % self._access_token)
            except ValueError:
                traceback.print_exc()
                abort(500)
            except (urllib2.HTTPError, KeyError, AssertionError):
                abort(400)
        else:
            _api = 'https://api.weibo.com/oauth2/authorize'
            _params = {
                'client_id': conf.WEIBO_KEY,
                'redirect_uri': conf.OAUTH2_URL,
            }
            return redirect(_api + '?' + urllib.urlencode(_params))


application = App()


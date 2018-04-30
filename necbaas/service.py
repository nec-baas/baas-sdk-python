# -*- coding: utf-8 -*-
try:
    # for python 3
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
except ImportError:
    # for python 2
    import urllib2 as urllib_request
    import urllib as urllib_parse


class Service(object):
    """
    BaaS access service class
    """
    def __init__(self, param):
        """
        Constructor.

        params has following fields:
        | baseUrl: Base URL of BaaS API Server (ex: https://api.example.com/api)
        | tenantId: Tenant ID or Tenant Name
        | appId: App ID
        | appKey: App Key (or Master Key)
        | proxy:
        |   type: Proxy type ('http' or 'https')
        |   host: Proxy host ('hostname:port')

        :param dict param: Parameters
        """
        self.param = param
        self.sessionToken = None

    def execute_rest(self, method, path, query=None, data=None, headers=None):
        """
        Call REST API

        :param str method: HTTP method name
        :param str path: Path. The part after '/1/{tenantId}' of full path. Must be started with '/'.
        :param dict query: Query parameters in dictionary.
        :param data: Request body, in bytes, file-like object or iterable.
        :param dict headers: headers
        :return: file-like object
        """
        url = self.param["baseUrl"] + "/1/" + self.param["tenantId"] + path
        if query is not None:
            url += "?" + urllib_parse.urlencode(query)

        if headers is None:
            headers = {}

        headers["X-Application-Id"] = self.param["appId"]
        headers["X-Application-Key"] = self.param["appKey"]

        if self.sessionToken is not None:
            headers["X-Session-Token"] = self.sessionToken

        if "Content-Type" not in headers and data is not None:
            headers["Content-Type"] = "application/json"

        req = urllib_request.Request(url, data, headers)
        req.get_method = lambda: method

        if "proxy" in self.param:
            req.set_proxy(self.param["proxy"]["host"], self.param["proxy"]["type"])

        try:
            return self._urlopen(req)
        except Exception as e:
            raise e  # TODO:

    def _urlopen(self, req):
        return urllib_request.urlopen(req)

    def set_session_token(self, token):
        """
        Store session token in this service. The token is stored on memory only.

        :param str token: Session Token
        :return:
        """
        self.sessionToken = token

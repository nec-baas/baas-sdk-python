# -*- coding: utf-8 -*-
import requests
import json as Json


class Service(object):
    """
    BaaS access service class.

    Example::

        service = necbaas.Service({
            "baseUrl": "https://api.example.com/api",
            "tenantId": "tenant1",
            "appId": "0123456789abcdef",
            "appKey": "0123456789abcdef",
            "proxy": {
                "http": "proxy.example.com:8080",
                "https": "proxy.example.com:8080"
            }
        })

    :param dict param:
        Parameters, must have following format::

            baseUrl: Base URL of BaaS API Server (ex: https://api.example.com/api) (mandatory)
            tenantId: Tenant ID or Tenant Name (mandatory)
            appId: App ID (mandatory)
            appKey: App Key (or Master Key) (mandatory)
            proxy: (optional)
                http: Http Proxy (host:port)
                https: Https Proxy (host:port)

    """
    def __init__(self, param):
        """
        Constructor.
        """
        self.param = param
        self.sessionToken = None

    def execute_rest(self, method, path, query=None, data=None, json=None, headers=None):
        """
        Call REST API

        :param str method: HTTP method name
        :param str path: Path. The part after '/1/{tenantId}' of full path. Must be started with '/'.
        :param dict query: Query parameters in dictionary.
        :param data: Request body, in bytes, file-like object or iterable.
        :param dict json: Request JSON in dictionary.
        :param dict headers: headers
        :return: Response
        """
        args = {}

        args["url"] = self.param["baseUrl"] + "/1/" + self.param["tenantId"] + path

        if query is not None:
            args["params"] = query

        if json is not None:
            data = Json.dumps(json).encode("utf-8")  # Override data
        if data is not None:
            args["data"] = data

        if headers is None:
            headers = {}
        args["headers"] = headers

        headers["X-Application-Id"] = self.param["appId"]
        headers["X-Application-Key"] = self.param["appKey"]

        if self.sessionToken is not None:
            headers["X-Session-Token"] = self.sessionToken

        if "Content-Type" not in headers and data is not None:
            headers["Content-Type"] = "application/json"

        if "proxy" in self.param:
            args["proxies"] = self.param["proxy"]

        return self._do_request(method, **args)

    def _do_request(self, method, **kwargs):
        method = method.upper()
        if method == 'GET':
            res = requests.get(**kwargs)
        elif method == 'POST':
            res = requests.post(**kwargs)
        elif method == 'PUT':
            res = requests.put(**kwargs)
        elif method == 'DELETE':
            res = requests.delete(**kwargs)
        else:
            raise Exception('Unsupported method: ' + method)

        status = res.status_code
        if status >= 400:
            res.raise_for_status()
        return res


    def set_session_token(self, token):
        """
        Store session token in this service. The token is stored on memory only.

        :param str token: Session Token
        :return:
        """
        self.sessionToken = token

# -*- coding: utf-8 -*-
import requests
import json as Json
from requests import Response


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

    param = None
    # type: dict
    """Service parameters"""

    session_token = None
    # type: str
    """Session Token"""

    verify_server_cert = True
    """Verify server cert (default: True)"""

    def __init__(self, param):
        # (dict) -> None
        """
        Constructor.
        """
        self.param = param
        self.session_token = None

    def execute_rest(self, method, path, query=None, data=None, json=None, headers=None):
        # (str, str, dict, Any, dict, dict) -> Response
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
        args = {
            "url": self.param["baseUrl"] + "/1/" + self.param["tenantId"] + path
        }

        # query parameters
        if query is not None:
            args["params"] = query

        # headers
        if headers is None:
            headers = {}
        args["headers"] = headers

        headers["X-Application-Id"] = self.param["appId"]
        headers["X-Application-Key"] = self.param["appKey"]

        if self.session_token is not None:
            headers["X-Session-Token"] = self.session_token

        # set data and decide content-type
        content_type = None
        if json is not None:
            args["data"] = Json.dumps(json).encode("utf-8")  # Override data
            content_type = "application/json"
        if data is not None:
            args["data"] = data
            content_type = "application/octet-stream"

        if "Content-Type" not in headers and content_type is not None:
            headers["Content-Type"] = content_type

        if "proxy" in self.param:
            args["proxies"] = self.param["proxy"]

        if not self.verify_server_cert:
            args["verify"] = False

        return self._do_request(method, **args)

    @staticmethod
    def _do_request(method, **kwargs):
        # type: (str, **dict) -> Response
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
        # type: (str) -> None
        """
        Store session token in this service. The token is stored on memory only.

        :param str token: Session Token
        :return:
        """
        self.session_token = token

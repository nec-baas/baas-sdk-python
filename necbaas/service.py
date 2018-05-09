# -*- coding: utf-8 -*-
import requests
import json as Json
import logging
from requests import Response


class Service(object):
    """
    BaaS access service class.

    Examples:
        ::

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

    Args:
        param (dict): Parameters, must have following dict format::

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
    """Service parameters, passed by constructor argument."""

    session_token = None
    # type: str
    """Session Token"""

    verify_server_cert = True
    # type: bool
    """Verify server cert (default: True)"""

    logger = None
    # type: logging.Logger
    """Logger. You can change log level with setLevel()"""

    def __init__(self, param):
        # (dict) -> None
        """
        Constructor.
        """
        # verify params
        if "baseUrl" not in param:
            raise Exception("No baseUrl")
        if "tenantId" not in param:
            raise Exception("No tenantId")
        if "appId" not in param:
            raise Exception("No appId")
        if "appKey" not in param:
            raise Exception("No appKey")

        # normalise baseUrl
        base_url = str(param["baseUrl"])
        if base_url.endswith("/"):
            base_url = base_url[0:-1]
            param["baseUrl"] = base_url

        self.param = param
        self.session_token = None
        self.logger = logging.getLogger("necbaas")
        self.logger.setLevel(logging.NOTSET)

    def execute_rest(self, method, path, query=None, data=None, json=None, headers=None, stream=False):
        # (str, str, dict, Any, dict, dict) -> Response
        """
        Call REST API.

        Note:
            This is low level and internal method, so you should not use this.

        Args:
            method (str): HTTP method name
            path (str): Path. The part after '/1/{tenantId}' of full path.
            query (dict): Query parameters in dictionary.
            data (data): Request body, in bytes, file-like object, stream or iterable.
            json (dict): Request JSON in dictionary.
            headers (dict): headers
            stream (bool): Stream flag

        Returns:
            Response: Response
        """
        if not path.startswith("/"):
            path = "/" + path

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

        if stream:
            args["stream"] = True

        return self._do_request(method, **args)

    def _do_request(self, method, **kwargs):
        self.logger.debug("HTTP request: method=%s, url=%s", method, kwargs["url"])
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
            self.logger.warning("HTTP request error: status=%d, body=%s", status, res.content)
            res.raise_for_status()
        else:
            self.logger.debug("HTTP response: status=%d", status)
        return res

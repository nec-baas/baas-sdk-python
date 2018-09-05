# -*- coding: utf-8 -*-
"""
BaaS access service module
"""
import os
import sys
import io
import requests
import logging
import copy
import json as json_lib
import yaml
import time
from requests import Response

_is_py2 = (sys.version_info[0] == 2)


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

    Attributes:
        param (dict): Service parameters, passed by constructor argument.
        session_token (str): Session Token
        session_token_expire (int): Session Token expire time (unix epoch seconds)
        verify_server_cert (bool): Verify server cert (default: True)
        logger (logging.Logger): Logger. You can change log level with setLevel()
    """

    _config_files = (
        os.path.expanduser("~/.baas/python/python_config.yaml"),
        "/etc/baas/python/python_config.yaml")
    # type: tuple

    _SESSION_TOKEN_FILE_DIR = os.path.expanduser("~/.baas/python")
    # type: str

    _SESSION_TOKEN_FILE_NAME = "session_token.json"
    # type: str

    _SESSION_TOKEN_FILE_PATH = os.path.join(_SESSION_TOKEN_FILE_DIR, _SESSION_TOKEN_FILE_NAME)
    # type: str

    def __init__(self, param=None):
        # type: (dict) -> None
        """
        Constructor.
        """
        if param is None:
            param = Service._read_config_file()

        # verify params
        if "baseUrl" not in param:
            raise ValueError("No baseUrl")
        if "tenantId" not in param:
            raise ValueError("No tenantId")
        if "appId" not in param:
            raise ValueError("No appId")
        if "appKey" not in param:
            raise ValueError("No appKey")

        # normalise baseUrl
        if _is_py2:
            if isinstance(param["baseUrl"], unicode):
                base_url = unicode(param["baseUrl"])
            else:
                base_url = param["baseUrl"].decode("utf-8")
        else:
            base_url = str(param["baseUrl"])

        if base_url.endswith("/"):
            base_url = base_url[0:-1]

        param["baseUrl"] = base_url

        self.param = param
        self.session_token = None
        self.session_token_expire = None
        self.verify_server_cert = True
        self.logger = logging.getLogger("necbaas")
        self.logger.setLevel(logging.WARNING)

    @staticmethod
    def _read_config_file():
        # type: () -> dict
        for path in Service._config_files:
            try:
                with io.open(path, encoding="utf-8") as config_file:
                    return yaml.load(config_file)
            except Exception:
                pass
        raise Exception("No service parameters")

    def save_config(self, path):
        # type: (str) -> None
        """
        Save configuration to file.

        Args:
            path (str): file path
        """
        with io.open(path, "w", encoding="utf-8") as config_file:
            yaml.dump(self.param, config_file, default_flow_style=False, allow_unicode=True, encoding="utf-8")

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
            data (data): Request body, in dict (form-encoded), bytes or file-like object.
                This overrides 'json' argument.
            json (dict): Request JSON in dictionary.
            headers (dict): headers
            stream (bool): Stream flag

        Returns:
            Response: Response
        """
        if path.startswith("/"):
            path = path[1:]

        base_url = self.param["baseUrl"].encode("utf-8") if _is_py2 else self.param["baseUrl"]
        args = {
            "url": "{}/1/{}/{}".format(base_url, self.param["tenantId"], path)
        }

        # query parameters
        if query is not None:
            args["params"] = query

        # headers
        if headers is None:
            headers = {}
        else:
            headers = copy.copy(headers)  # shallow copy, do not change original
        args["headers"] = headers

        headers["X-Application-Id"] = self.param["appId"]
        headers["X-Application-Key"] = self.param["appKey"]

        if self.session_token is not None:
            headers["X-Session-Token"] = self.session_token

        # set data and decide content-type
        content_type = None
        if data is not None:
            args["data"] = data
            content_type = "application/octet-stream"
        elif json is not None:
            args["json"] = json

        if content_type is not None and "Content-Type" not in headers:
            headers["Content-Type"] = content_type

        if "proxy" in self.param:
            args["proxies"] = self.param["proxy"]

        if not self.verify_server_cert:
            args["verify"] = False

        if stream:
            args["stream"] = True

        return self._do_request(method, **args)

    def _do_request(self, method, **kwargs):
        # type: (str, **dict) -> Response
        self.logger.debug("HTTP request: method=%s, url=%s", method, kwargs["url"])
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

    def load_session_token(self):
        # type: () -> None
        """
        Load session token from file.
        If session token file does not exist, session token is cleared.
        """
        if not os.path.exists(Service._SESSION_TOKEN_FILE_PATH):
            self.session_token = None
            self.session_token_expire = None
            return

        with open(Service._SESSION_TOKEN_FILE_PATH, 'r') as token_file:
            token = json_lib.load(token_file)

        if "sessionToken" not in token:
            raise Exception("No sessionToken")
        if "sessionTokenExpire" not in token:
            raise Exception("No sessionTokenExpire")

        self.session_token = token["sessionToken"]
        self.session_token_expire = token["sessionTokenExpire"]

    def save_session_token(self):
        # type: () -> None
        """
        Save session token to file.
        """
        if not os.path.exists(Service._SESSION_TOKEN_FILE_DIR):
            os.makedirs(Service._SESSION_TOKEN_FILE_DIR)

        if self.session_token is None:
            raise Exception("No session token")

        with open(Service._SESSION_TOKEN_FILE_PATH, 'w') as token_file:
            session_token = {
                "sessionToken": self.session_token,
                "sessionTokenExpire": self.session_token_expire}
            json_lib.dump(session_token, token_file)

    @staticmethod
    def delete_session_token_file():
        # type: () -> None
        """
        Delete session token file.
        """
        if os.path.exists(Service._SESSION_TOKEN_FILE_PATH):
            os.remove(Service._SESSION_TOKEN_FILE_PATH)

    def verify_session_token(self):
        # type: () -> None
        """
        Verify session token in instance.
        """
        if self.session_token is None:
            raise Exception("No session token")
        if self.session_token_expire <= time.time():
            raise Exception("Session token is expired")

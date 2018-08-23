# -*- coding: utf-8 -*-
"""
API Gateway module
"""
from .service import Service
from requests import Response


class Apigw(object):
    """
    API Gateway instance.
    Create this instance for each API (apiname, method and subpath)

    Example:
        ::

            api = necbaas.Apigw(service, "api1", "GET", "a/b/c")

    Args:
        service (Service): Service
        apiname (str): API name
        method (str): Method (GET/POST/PUT/DELETE)
        subpath (str): Sub-path (optional)

    Attributes:
        service (Service): Service
        apiname (str): API name
        method (str): Method (GET/POST/PUT/DELETE)
        subpath (str): Sub-path (optional)
    """

    def __init__(self, service, apiname, method, subpath=None):
        # type: (Service, str, str, str) -> None
        if subpath.startswith("/"):
            subpath = subpath[1:]

        self.service = service
        self.apiname = apiname
        self.method = method
        self.subpath = subpath

    def execute(self, data=None, json=None, query=None, headers=None):
        # type: (any, dict, dict, dict) -> Response
        """
        Execute API Gateway.
        Return value is 'Response' object of 'requests' library.

        Example:
            ::

                res = api.execute(json={"temperature": 26.3})
                status = res.status()  # get status code
                json = res.json()  # response body of JSON as dict

        Args:
            data (any): Request body, in bytes or file-like object. This overrides 'json' argument. (optional)
            json (dict): Request body of JSON. (optional)
            query (dict): Query parameters. (optional)
            headers (dict): Headers. (optional)

        Returns:
            Response: Response of 'requests' library.
        """
        path = "api/" + self.apiname
        if self.subpath is not None:
            path = path + "/" + self.subpath
        return self.service.execute_rest(self.method, path, query=query, data=data, json=json, headers=headers)

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

    Example::
        api = necbaas.Apigw(service, "api1", "GET", "a/b/c")

    :param Service service: Service
    :param str apiname: API name
    :param str method: method (GET/POST/PUT/DELETE)
    :param str subpath: subpath (optional)
    """

    service = None
    # type: Service
    """Service instance"""

    def __init__(self, service, apiname, method, subpath = None):
        # type: (Service, str, str, str) -> None
        self.service = service
        self.apiname = apiname
        self.method = method
        self.subpath = subpath

    def execute(self, data=None, json=None, query=None, headers=None):
        # type: (any, dict, dict, dict) -> Response
        """
        Execute API Gateway.
        Return value is 'Response' object of 'requests' library.

        Example::
            res = api.execute(json={"sensor1": 45.2}, headers={"Content-Type": "application/json"}})
            status = res.status()  # get status code
            json = res.json()  # response body of JSON as dict

        :param any data: Request body (optional)
        :param dict json: Request body of JSON (optional)
        :param dict query: Query parameters (optional)
        :param dict headers: Headers (optional)
        :return: Response of 'requests' library.
        """
        path = self.apiname
        if self.subpath is not None:
            path = path + "/" + self.subpath
        return self.service.execute_rest(self.method, path, query=query, data=data, headers=headers)


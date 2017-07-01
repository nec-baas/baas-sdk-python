# -*- coding: UTF-8 -*-
try:
    import urllib.request as urllib_request  # for python3
except ImportError:
    import urllib2 as urllib_request


class Service():
    def __init__(self, param):
        self.param = param
        self.sessionToken = None

    def execute_request(self, method, path, data=None, content_type=None):
        url = self.param["baseUrl"] + "/1/" + self.param["tenantId"] + path

        headers = {
            "X-Application-Id": self.param["appId"],
            "X-Application-Key": self.param["appKey"]
        }

        if self.sessionToken is not None:
            headers["X-Session-Token"] = self.sessionToken

        if content_type is None and data is not None:
            content_type = "application/json"

        if content_type is not None:
            headers["Content-Type"] = content_type

        req = urllib_request.Request(url, data, headers)
        req.get_method = lambda: method
        
        if "proxy" in self.param:
            req.set_proxy(self.param["proxy"]["host"], self.param["proxy"]["type"])

        try:
            return urllib_request.urlopen(req)
        except Exception as e:
            raise e  # TODO:

    def set_session_token(self, token):
        self.sessionToken = token

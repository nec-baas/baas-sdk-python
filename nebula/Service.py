# -*- coding: UTF-8 -*-
try:
    # for python 3
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
except ImportError:
    # for python 2
    import urllib2 as urllib_request
    import urllib2 as urllib_parse


class Service:
    """
    BaaSアクセス用サービスクラス。
    """
    def __init__(self, param):
        """
        コンストラクタ。
        :param dict param: パラメータを指定する。
        """
        self.param = param
        self.sessionToken = None

    def execute_rest(self, method, path, query=None, data=None, headers=None):
        """
        REST API を実行する
        :param str method: HTTPメソッド名
        :param str path: パス。/1/{tenantId} の後のパス。先頭に '/' を付ける。
        :param dict query: クエリパラメータ。Dictionary で指定。
        :param data: 送信データ。bytes, file-like object, iterables のいずれか。
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
            return urllib_request.urlopen(req)
        except Exception as e:
            raise e  # TODO:

    def set_session_token(self, token):
        """
        セッショントークンを保存する。セッショントークンはメモリ上にのみ保持される。
        :param str token: セッショントークン
        :return:
        """
        self.sessionToken = token

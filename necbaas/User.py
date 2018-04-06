# -*- coding: utf-8 -*-
import json


class User(object):
    """
    ユーザ
    """

    def __init__(self, service):
        self.service = service
        self.username = None
        self.email = None
        self.password = None
        self.options = None

    @staticmethod
    def login_with_username(service, username, password):
        """
        ユーザ名でログインする
        :param service: Service
        :param str username: ユーザ名
        :param str password: パスワード
        :return:
        """
        return User.login(service, {
            "username": username,
            "password": password
        })

    @staticmethod
    def login_with_email(service, email, password):
        """
        E-mailでログインする
        :param service: Service
        :param str email: ユーザ名
        :param str password: パスワード
        :return:
        """
        return User.login(service, {
            "email": email,
            "password": password
        })

    @staticmethod
    def login(service, param):
        """
        ログインする。
        :param service: Service
        :param dict param: dictionary。JSON化されてサーバにそのまま送信される。通常は username, email のいずれかと、password を指定する
        :return:
        """
        f = service.execute_rest("POST", "/login", None, json.dumps(param).encode("utf-8"))
        res = json.loads(f.read())

        session_token = res["sessionToken"]
        service.set_session_token(session_token)
        return res

    @staticmethod
    def logout(service):
        """
        ログアウトする
        :param service: Service
        :return:
        """
        f = service.execute_rest("DELETE", "/login")
        res = json.loads(f.read())
        service.set_session_token(None)
        return res

    def register(self):
        """
        ユーザ登録する。
        username, email, password, options プロパティを設定しておくこと。
        :return: 登録情報(JSON)
        """
        body = {}
        if self.username is not None:
            body["username"] = self.username
        if self.email is not None:
            body["email"] = self.email
        if self.password is not None:
            body["password"] = self.password
        if self.options is not None:
            body["options"] = self.options

        f = self.service.execute_rest("POST", "/users", None, body)
        res = json.loads(f.read())
        return res

    @staticmethod
    def query(self, username=None, email=None):
        """
        ユーザ検索する
        :param username: ユーザ名
        :param email: E-mail
        :return:
        """
        query = {}
        if username is not None:
            query["username"] = username
        if email is not None:
            query["email"] = email

        f = self.service.execute_rest("GET", "/users", query)
        res = json.loads(f.read())
        return res

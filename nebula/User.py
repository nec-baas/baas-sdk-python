# -*- coding: UTF-8 -*-
import json


class User:
    """
    ユーザ
    """

    def __init__(self, service):
        self.service = service

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
        print(session_token)
        service.set_session_token(session_token)

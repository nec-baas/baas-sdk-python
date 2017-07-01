# -*- coding: UTF-8 -*-
import json

class User():
    def __init__():
        pass

    @staticmethod
    def login(service, param):
        """
        ログインする。
        :param service: Service
        :param param: dictionary。JSON化されてサーバにそのまま送信される。通常は username, email のいずれかと、password を指定する
        :return:
        """
        f = service.execute_rest("POST", "/login", None, json.dumps(param).encode("utf-8"))
        res = json.loads(f.read())

        session_token = res["sessionToken"]
        print(session_token)
        service.set_session_token(session_token)

# -*- coding: UTF-8 -*-
import json

class User():
    def __init__():
        pass

    @staticmethod
    def login(service, param):
        f = service.execute_request("POST", "/login", json.dumps(param).encode("utf-8"))
        res = json.loads(f.read())

        session_token = res["sessionToken"]
        print(session_token)
        service.set_session_token(session_token)

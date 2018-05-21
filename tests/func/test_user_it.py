import requests
import pytest
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class TestUser(object):
    service = None
    # type: baas.Service
    masterService = None
    # type: baas.Service

    def setup(self):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)
        util.remove_all_users()

    def register_user(self):
        u = baas.User(self.service)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "Passw0rD"
        u.options = {"realname": "Foo Bar"}
        u.register()
        return u

    def test_register(self):
        """
        ユーザ登録テスト(register)
        - 正常登録できること
        - ユーザ重複時に 409 エラーになること
        """
        u = baas.User(self.service)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "Passw0rD"
        u.options = {"realname": "Foo Bar"}

        res = u.register()
        print(res)

        with pytest.raises(HTTPError) as ei:
            u.register()
        e = ei.value
        s = e.response.status_code
        assert s == 409

    def test_query(self):
        """
        ユーザ検索テスト
        - 全件検索
        - ユーザ名指定検索
        - email指定検索
        - ユーザ存在しない
        """
        self.register_user()

        # query all
        users = baas.User.query(self.masterService)
        assert len(users) == 1

        # query by user id
        users = baas.User.query(self.masterService, username="user1")
        assert len(users) == 1
        assert users[0]["username"] == "user1"

        # query by email
        users = baas.User.query(self.masterService, email="user1@example.com")
        assert len(users) == 1
        assert users[0]["username"] == "user1"

        # no result
        with pytest.raises(HTTPError) as ei:
            baas.User.query(self.masterService, username="no_such_user")
        e = ei.value
        assert e.response.status_code == 404

    def test_login_logout(self):
        """
        正常ログイン
        """
        u = self.register_user()
        assert self.service.session_token is None

        res = baas.User.login(self.service, username=u.username, password=u.password)
        assert res["username"] == "user1"

        assert self.service.session_token is not None
        assert self.service.session_token_expire is not None

        res = baas.User.logout(self.service)

    def test_login_bad_password(self):
        """
        パスワード不正ログイン: 401 Unauthorized となること
        """
        u = self.register_user()

        with pytest.raises(HTTPError) as ei:
            baas.User.login(self.service, username=u.username, password="BAD_PASS")
        e = ei.value
        assert e.response.status_code == 401

    def test_logout(self):
        """
        正常ログアウト
        """
        u = self.register_user()
        baas.User.login(self.service, username=u.username, password=u.password)

        # 正常にログアウトできること
        baas.User.logout(self.service)
        assert self.service.session_token is None
        assert self.service.session_token_expire is None

        # 二重ログアウトは 401 になること
        with pytest.raises(HTTPError) as ei:
            baas.User.logout(self.service)
        e = ei.value
        assert e.response.status_code == 401

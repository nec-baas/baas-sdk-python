# -*- coding: utf-8 -*-
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
        res = u.register()
        return u, res

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

    @pytest.mark.parametrize("etag", [None, True])
    def test_update(self, etag):
        """
        ユーザ更新テスト(update)
        """
        _, reg_user = self.register_user()

        u = baas.User(self.masterService)
        u.username = "user2"
        u.email = "user2@example.com"
        u.password = "Passw0rD2"
        u.options = {"realname": "Foo Bar 2"}
        res = u.update(reg_user["_id"], etag if etag is None else reg_user["etag"])
        assert res["username"] == "user2"
        print(res)

    def test_update_etag_mismatch(self):
        """
        ユーザ更新テスト(update)： Etag不正の場合はエラーとなること
        """
        _, reg_user = self.register_user()

        u = baas.User(self.masterService)
        with pytest.raises(HTTPError) as ei:
            u.update(reg_user["_id"], "etag")
        e = ei.value
        assert e.response.status_code == 409

    def test_query_all(self):
        """
        ユーザ全件検索
        """
        self.register_user()

        users = baas.User.query(self.masterService)
        assert len(users) == 1

    def test_query_username(self):
        """
        ユーザ名検索
        """
        self.register_user()

        # query by user id
        users = baas.User.query(self.masterService, username="user1")
        assert len(users) == 1
        assert users[0]["username"] == "user1"

    def test_query_email(self):
        """
        E-mail検索
        """
        self.register_user()

        # query by email
        users = baas.User.query(self.masterService, email="user1@example.com")
        assert len(users) == 1
        assert users[0]["username"] == "user1"

    def test_query_not_exist(self):
        """
        存在しないユーザ検索
        """
        self.register_user()

        # no result
        with pytest.raises(HTTPError) as ei:
            baas.User.query(self.masterService, username="no_such_user")
        e = ei.value
        assert e.response.status_code == 404

    @pytest.mark.parametrize('username,email', [("user1", None), (None, "user1@example.com")])
    def test_login(self, username, email):
        """
        正常ログイン
        """
        u, _ = self.register_user()
        assert self.service.session_token is None

        res = baas.User.login(self.service, username=username, email=email, password=u.password)
        assert res["username"] == "user1"

        assert self.service.session_token is not None
        assert self.service.session_token_expire is not None

        baas.User.logout(self.service)

    def test_login_bad_password(self):
        """
        パスワード不正ログイン: 401 Unauthorized となること
        """
        u, _ = self.register_user()

        with pytest.raises(HTTPError) as ei:
            baas.User.login(self.service, username=u.username, password="BAD_PASS")
        e = ei.value
        assert e.response.status_code == 401

    def test_logout(self):
        """
        正常ログアウト / 二重ログアウト
        """
        u, _ = self.register_user()
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

    def test_get(self):
        """
        正常取得
        """
        _, reg_user = self.register_user()

        res = baas.User.get(self.masterService, reg_user["_id"])
        assert res["username"] == "user1"

    def test_remove(self):
        """
        正常削除
        """
        _, reg_user = self.register_user()

        res = baas.User.remove(self.masterService, reg_user["_id"])
        assert res["result"] == "ok"

        # 二重削除は 404
        with pytest.raises(HTTPError) as ei:
            baas.User.remove(self.masterService, reg_user["_id"])
        e = ei.value
        assert e.response.status_code == 404

    @pytest.mark.skip(reason='need to send email')
    def test_reset_password_by_username(self):
        """
        パスワードリセット要求正常(ユーザ名)
        """
        u, _ = self.register_user()

        res = baas.User.reset_password(self.service, username=u.username)
        assert res["result"] == "ok"

    @pytest.mark.skip(reason='need to send email')
    def test_reset_password_by_email(self):
        """
        パスワードリセット要求正常(E-mail)
        """
        u, _ = self.register_user()

        res = baas.User.reset_password(self.service, email=u.email)
        assert res["result"] == "ok"

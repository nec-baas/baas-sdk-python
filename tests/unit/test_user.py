# -*- coding: utf-8 -*-
import pytest

import necbaas as baas

from .util import *


class TestUser(object):
    def get_service(self):
        param = {
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        }
        return baas.Service(param)

    def test_init(self):
        """正常に初期化できること"""
        s = self.get_service()
        u = baas.User(s)
        assert u.service == s
        assert u.username is None
        assert u.email is None
        assert u.password is None
        assert u.options is None

    def test_register(self):
        """正常に登録できること"""
        mock_service = MagicMock()
        u = baas.User(mock_service)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "pass"
        u.options = {"realname": "Foo Bar"}

        u.register()

        args = mock_service.execute_rest.call_args
        assert args[0], ("POST" == "/users")
        json = args[1]["json"]
        assert json["username"] == "user1"
        assert json["email"] == "user1@example.com"
        assert json["password"] == "pass"
        assert json["options"] == {"realname": "Foo Bar"}

    def test_update(self):
        """正常に更新できること(etagなし)"""
        mock_service = MagicMock()
        u = baas.User(mock_service)
        u.username = "user2"
        u.email = "user2@example.com"
        u.password = "pass2"
        u.options = {"realname": "Foo Bar 2"}

        user_id = "userId"
        u.update(user_id)

        args = mock_service.execute_rest.call_args
        assert args[0], ("PUT" == "/users/" + user_id)
        query = args[1]["query"]
        assert len(query) == 0
        json = args[1]["json"]
        assert json["username"] == "user2"
        assert json["email"] == "user2@example.com"
        assert json["password"] == "pass2"
        assert json["options"] == {"realname": "Foo Bar 2"}

    def test_update_etag(self):
        """正常に更新できること(etagあり)"""
        mock_service = MagicMock()
        u = baas.User(mock_service)

        u.update("user01", "testEtag")

        args = mock_service.execute_rest.call_args
        assert args[0], ("PUT" == "/users/user01")
        query = args[1]["query"]
        assert query["etag"] == "testEtag"
        json = args[1]["json"]
        assert len(json) == 0

    def test_login_username(self):
        """username で正常にログインできること"""
        service = mock_service_json_resp({"sessionToken": "TOKEN", "expire": 12345})

        baas.User.login(service, username="user1", password="pass1")

        assert service.session_token == "TOKEN"
        assert service.session_token_expire == 12345

        json = get_rest_kwargs(service)["json"]
        assert json == {"username": "user1", "password": "pass1"}

    def test_login_email(self):
        """email で正常にログインできること"""
        service = mock_service_json_resp({"sessionToken": "TOKEN", "expire": 12345})

        baas.User.login(service, email="user1@example.com", password="pass1")

        assert service.session_token == "TOKEN"
        assert service.session_token_expire == 12345

        json = get_rest_kwargs(service)["json"]
        assert json == {"email": "user1@example.com", "password": "pass1"}

    def test_login_no_passwd_params(self):
        """password, params いずれも指定しないときに ValueError となること"""
        with pytest.raises(ValueError):
            baas.User.login(MagicMock(), username="user1")

    def test_login_no_username_email(self):
        """username, email いずれも指定しないときに ValueError となること"""
        with pytest.raises(ValueError):
            baas.User.login(MagicMock(), password="pass")

    def test_logout(self):
        """正常にログアウトできること"""
        service = mock_service_json_resp({})
        service.session_token = "TOKEN"
        service.session_token_expire = 12345

        baas.User.logout(service)

        assert service.session_token is None
        assert service.session_token_expire is None

        args = get_rest_args(service)
        assert args == ("DELETE", "/login")

    def test_query(self):
        """正常にクエリできること"""
        expected = [{"username": "user1"}, {"username": "user2"}]
        service = mock_service_json_resp({"results": expected})

        results = baas.User.query(service, username="user1", email="user1@example.com")
        assert results == expected

        assert get_rest_args(service) == ("GET", "/users")
        query = get_rest_kwargs(service)["query"]
        assert query == {"username": "user1", "email": "user1@example.com"}

    def test_get(self):
        """正常に取得できること"""
        expected = {"username": "user1", "email": "user1@example.com"}
        service = mock_service_json_resp(expected)

        results = baas.User.get(service, "user01")
        assert results == expected

        assert get_rest_args(service) == ("GET", "/users/user01")

    def test_remove(self):
        """正常にユーザ削除できること"""
        service = mock_service_json_resp({"_id": "user01"})

        result = baas.User.remove(service, "user01")
        assert result == {"_id": "user01"}

        assert get_rest_args(service) == ("DELETE", "/users/user01")

    def test_reset_password_username(self):
        """正常にユーザ名でパスワードリセット要求できること"""
        expected = {}
        service = mock_service_json_resp(expected)

        results = baas.User.reset_password(service, username="user01")
        assert results == expected

        assert get_rest_args(service) == ("POST", "/request_password_reset")
        json = get_rest_kwargs(service)["json"]
        assert json == {"username": "user01"}

    def test_reset_password_email(self):
        """正常にEmailでパスワードリセット要求できること"""
        expected = {}
        service = mock_service_json_resp(expected)

        results = baas.User.reset_password(service, email="user1@example.com")
        assert results == expected

        assert get_rest_args(service) == ("POST", "/request_password_reset")
        json = get_rest_kwargs(service)["json"]
        assert json == {"email": "user1@example.com"}

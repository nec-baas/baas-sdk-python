from mock import patch, MagicMock
import pytest

import necbaas as baas


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

    def _mock_response_json(self, json):
        """
        mock_service.execute_rest() の JSON 応答を mock する

        Args:
            mock_service: Mock Service
            json: Response Json
        """
        response = MagicMock()
        response.json.return_value = json

        service = MagicMock()
        service.execute_rest.return_value = response
        return service

    def test_login_username(self):
        """username で正常にログインできること"""
        service = self._mock_response_json({"sessionToken": "TOKEN", "expire": 12345})

        baas.User.login(service, username="user1", password="pass1")

        assert service.session_token == "TOKEN"
        assert service.session_token_expire == 12345

        json = service.execute_rest.call_args[1]["json"]
        assert json == {"username": "user1", "password": "pass1"}

    def test_login_email(self):
        """email で正常にログインできること"""
        service = self._mock_response_json({"sessionToken": "TOKEN", "expire": 12345})

        baas.User.login(service, email="user1@example.com", password="pass1")

        assert service.session_token == "TOKEN"
        assert service.session_token_expire == 12345

        json = service.execute_rest.call_args[1]["json"]
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
        service = self._mock_response_json({})
        service.session_token = "TOKEN"
        service.session_token_expire = 12345

        baas.User.logout(service)

        assert service.session_token is None
        assert service.session_token_expire is None

        args = service.execute_rest.call_args[0]
        assert args == ("DELETE", "/login")

    def test_query(self):
        """正常にクエリできること"""
        expected = [{"username": "user1"}, {"username": "user2"}]
        service = self._mock_response_json({"results": expected})

        results = baas.User.query(service, username="user1", email="user1@example.com")
        assert results == expected

        assert service.execute_rest.call_args[0] == ("GET", "/users")
        query = service.execute_rest.call_args[1]["query"]
        assert query == {"username": "user1", "email": "user1@example.com"}

    def test_remove(self):
        """正常にユーザ削除できること"""
        service = self._mock_response_json({"_id": "user01"})

        result = baas.User.remove(service, "user01")
        assert result == {"_id": "user01"}

        assert service.execute_rest.call_args[0] == ("DELETE", "/users/user01")

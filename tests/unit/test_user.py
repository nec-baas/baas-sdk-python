from mock import patch, MagicMock

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

        u.register()

        args = mock_service.execute_rest.call_args
        assert args[0], ("POST" == "/users")
        json = args[1]["json"]
        assert json["username"] == "user1"
        assert json["email"] == "user1@example.com"
        assert json["password"] == "pass"

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

    def test_login(self):
        """正常にログインできること"""
        service = self._mock_response_json({"sessionToken": "TOKEN", "expire": 12345})

        baas.User.login(service, username="user1", password="pass1")

        assert service.session_token == "TOKEN"
        assert service.session_token_expire == 12345








from unittest import TestCase
from mock import patch

import necbaas as baas


class ServiceTestCase(TestCase):
    def get_sample_param(self):
        """テスト用のサンプルパラメータを返す"""
        return {
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        }

    def test_init(self):
        """正常に初期化できること"""
        param = self.get_sample_param()
        service = baas.Service(param)
        self.assertEquals(service.param, param)
        self.assertEquals(service.param["baseUrl"], "http://localhost/api")
        self.assertEquals(service.session_token, None)

    def test_init_normalize_base_url(self):
        """baseUrl が正常に正規化されること"""
        param = self.get_sample_param()
        param["baseUrl"] = "http://localhost/api/"  # trailing slash
        service = baas.Service(param)
        self.assertEquals(service.param["baseUrl"], "http://localhost/api")

    def _test_init_bad_sub(self, key):
        param = self.get_sample_param()
        del param[key]
        with self.assertRaises(ValueError):
            baas.Service(param)

    def test_no_base_url(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("baseUrl")

    def test_no_tenant_id(self):
        """tenantId 指定がないときにエラーになること"""
        self._test_init_bad_sub("tenantId")

    def test_no_app_id(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("appId")

    def test_no_app_key(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("appKey")

    @patch("necbaas.Service._do_request")
    def test_execute_rest(self, mock):
        """正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        service.session_token = "token1"

        query = {"a": 1}

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c", query=query)
        self.assertEqual(ret, {})

        method = mock.call_args[0][0]
        kwargs = mock.call_args[1]
        self.assertEqual(method, "GET")
        self.assertEqual(kwargs["url"], "http://localhost/api/1/tenant1/a/b/c")
        self.assertEqual(kwargs["params"], query)

        headers = kwargs["headers"]
        self.assertEqual(headers["X-Application-Id"], "app1")
        self.assertEqual(headers["X-Application-Key"], "key1")
        self.assertEqual(headers["X-Session-Token"], "token1")

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_headers(self, mock):
        """ヘッダ付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c", headers={"X-header1": "xxx"})
        self.assertEqual(ret, {})

        headers = mock.call_args[1]["headers"]
        self.assertEqual(headers["X-header1"], "xxx")

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_json(self, mock):
        """JSONボディ付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        service.execute_rest("POST", "a/b/c", json={"a": 1})

        kwargs = mock.call_args[1]
        self.assertEqual(kwargs["json"], {"a": 1})

        # json 指定時は Content-Type ヘッダなし (requests 側で自動設定)
        headers = kwargs["headers"]
        self.assertNotIn("Content-Type", headers)

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_data(self, mock):
        """data付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        service.execute_rest("POST", "a/b/c", data="xxxxx")

        kwargs = mock.call_args[1]
        self.assertEqual(kwargs["data"], "xxxxx")

        # data 指定時は Content-Type デフォルトは application/octet-stream
        headers = kwargs["headers"]
        self.assertEqual(headers["Content-Type"], "application/octet-stream")







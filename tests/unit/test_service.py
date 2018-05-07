from unittest import TestCase
from mock import patch

import necbaas as baas


class ServiceTestCase(TestCase):
    def test_init(self):
        service = baas.Service({})
        self.assertEquals(service.param, {})
        self.assertEquals(service.session_token, None)

    @patch("necbaas.Service._do_request")
    def test_execute_rest(self, mock):
        service = baas.Service({
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        })

        service.session_token = "token1"

        mock.return_value = {}
        ret = service.execute_rest("GET", "/a/b/c")
        self.assertEqual(ret, {})

        method = mock.call_args[0][0]
        kwargs = mock.call_args[1]
        self.assertEqual(method, "GET")
        self.assertEqual(kwargs["url"], "http://localhost/api/1/tenant1/a/b/c")
        headers = kwargs["headers"]
        self.assertEqual(headers["X-Application-Id"], "app1")
        self.assertEqual(headers["X-Application-Key"], "key1")
        self.assertEqual(headers["X-Session-Token"], "token1")

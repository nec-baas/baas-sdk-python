from unittest import TestCase
from unittest.mock import patch

import necbaas as baas


class ServiceTestCase(TestCase):
    def test_init(self):
        service = baas.Service({})
        self.assertEquals(service.param, {})
        self.assertEquals(service.sessionToken, None)

    @patch("necbaas.Service._urlopen")
    def test_execute_rest(self, mock):
        service = baas.Service({
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        })

        mock.return_value = {}
        ret = service.execute_rest("GET", "/a/b/c")
        self.assertEqual(ret, {})

        req = mock.call_args[0][0]
        self.assertEqual(req.full_url, "http://localhost/api/1/tenant1/a/b/c")

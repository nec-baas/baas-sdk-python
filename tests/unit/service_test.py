from unittest import TestCase

import necbaas as baas

class ServiceTestCase(TestCase):
    def test_init(self):
        service = baas.Service({})
        self.assertEquals(service.param, {})
        self.assertEquals(service.sessionToken, None)

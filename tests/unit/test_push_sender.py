# -*- coding: utf-8 -*-
import necbaas as baas

from .util import *


class TestPushSender(object):
    def get_service(self):
        param = {
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        }
        return baas.Service(param)

    def test_send(self):
        """正常に send できること"""
        expected = 100
        service = mock_service_json_resp({"installations": expected})

        request = {"query": {"_id": "instaId"}, "message": "message"}

        results = baas.PushSender.send(service, request)
        assert results == expected

        assert get_rest_args(service) == ("POST", "/push/notifications")
        json = get_rest_kwargs(service)["json"]
        assert json == request

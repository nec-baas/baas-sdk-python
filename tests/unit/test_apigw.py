# -*- coding: utf-8 -*-
import necbaas as baas

from .util import *


class TestApigw(object):
    def test_execute(self):
        """正常に APIGW コールできること"""
        expected_result ={"result": 1}
        service = mock_service_json_resp(expected_result)

        apigw = baas.Apigw(service, "api1", "POST", "/a/b/c")

        json = {"key1": 12345}
        query ={"query": "xxx"}
        headers = {"X-Some-Header": "xxxxx"}
        result = apigw.execute(json=json, query=query, headers=headers).json()
        assert result == expected_result

        assert get_rest_args(service) == ("POST", "api/api1/a/b/c")
        kwargs = get_rest_kwargs(service)
        assert kwargs["json"] == json
        assert kwargs["query"] == query
        assert kwargs["headers"] == headers

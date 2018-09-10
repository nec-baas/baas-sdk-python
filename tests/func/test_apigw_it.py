# -*- coding: utf-8 -*-
import json
import pytest
import logging
from requests import HTTPError

import necbaas as baas
from . import util

# ロガー初期化
logging.basicConfig(level=logging.WARNING)


class TestApigw(object):
    def setup(self):
        self.service = util.create_service()

    @pytest.mark.skip(reason='need to register cloud function')
    def test_execute(self):
        """
        API GW呼び出し正常

        Note:
            以下のCloudFunctionを事前に登録する
            API Name: api1
            subpath: subpath1/subpath2
            response json: {"message": "Hello World!"}
        """
        self.service.logger.setLevel(logging.DEBUG)  # REST API log

        apigw = baas.Apigw(self.service, "api1", "GET", "subpath1/subpath2")

        r = apigw.execute()
        res = r.json()
        assert res["message"] == "Hello World!"

    def test_execute_nonexist(self):
        """存在しない APIGW 呼び出し。404 Not Found となること"""
        self.service.logger.setLevel(logging.DEBUG)  # REST API log

        apigw = baas.Apigw(self.service, "api1", "GET", "a/b/c/d/e/f/g")

        with pytest.raises(HTTPError) as ei:
            apigw.execute()
        resp = ei.value.response
        assert resp.status_code == 404
        j = json.loads(resp.text)
        assert j["error"] == "No such API"

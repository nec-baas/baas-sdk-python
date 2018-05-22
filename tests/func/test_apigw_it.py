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
    service = None
    # type: baas.Service

    def setup(self):
        self.service = util.create_service()

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

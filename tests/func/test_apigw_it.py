# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError

import necbaas as baas
from . import util


class TestApigw(object):
    service = None
    # type: baas.Service

    def setup(self):
        self.service = util.create_service()

    def test_execute_nonexist(self):
        """存在しない APIGW 呼び出し。404 Not Found となること"""
        apigw = baas.Apigw(self.service, "api1", "GET", "a/b/c/d/e/f/g")

        with pytest.raises(HTTPError) as ei:
            apigw.execute()
        status_code = ei.value.response.status_code
        assert status_code == 404

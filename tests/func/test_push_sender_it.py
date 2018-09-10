# -*- coding: utf-8 -*-
import pytest
import logging
import necbaas as baas
from . import util

# ロガー初期化
logging.basicConfig(level=logging.WARNING)


class TestPushSender(object):
    def setup(self):
        self.service = util.create_service()

    @pytest.mark.skip(reason='need to register installations')
    def test_push_send(self):
        """Push送信正常"""
        self.service.logger.setLevel(logging.DEBUG)  # REST API log

        request = {
            "query": {},
            "message": "test message"}
        send_num = baas.PushSender.send(self.service, request)

        assert send_num == 3

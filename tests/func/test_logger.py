# -*- coding: utf-8 -*-
import logging
import necbaas as baas
from . import util

# ロガー初期化
logging.basicConfig(level=logging.WARNING)


class TestLogger(object):
    master_service = None
    # type: baas.Service

    def setup(self):
        self.master_service = util.create_service(master=True)

    def test_debug_log(self):
        """デバッグログが出力されること(手動テスト、目視確認すること)"""
        self.master_service.logger.setLevel(logging.DEBUG)
        baas.User.query(self.master_service)

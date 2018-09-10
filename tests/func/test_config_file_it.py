# -*- coding: utf-8 -*-
import os
import logging
import pytest
import necbaas as baas
from . import util

# 初期設定ファイルテスト
logging.basicConfig(level=logging.WARNING)


class TestConfigFile(object):
    master_service = None
    # type: baas.Service

    def setup(self):
        if not os.path.exists(os.path.expanduser("~/.baas/python")):
            os.makedirs(os.path.expanduser("~/.baas/python"))

        if os.path.exists(os.path.expanduser("~/.baas/python/python_config.yaml")):
            os.remove(os.path.expanduser("~/.baas/python/python_config.yaml"))

    def test_init_home_file(self):
        """ホームディレクトリの設定ファイルでサービス初期化すること"""
        # ファイルが存在しない場合はエラー
        with pytest.raises(Exception):
            baas.Service()

        # パラメータ指定で初期化
        c = util.load_config()
        param = c["service"]
        service = baas.Service(param)

        # ファイル保存
        service.save_config(os.path.expanduser("~/.baas/python/python_config.yaml"))

        # 設定ファイルで初期化
        service2 = baas.Service(param)
        assert service2.param == param

        param2 = {
            "baseUrl": "http://テストホスト/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1",
            "proxy": {
                "http": "proxy.example.com:8080",
                "https": "proxy.example2.com:8080"
            }
        }

        service3 = baas.Service(param2)

        # ファイル上書き保存
        service3.save_config(os.path.expanduser("~/.baas/python/python_config.yaml"))

        # 設定ファイルで初期化
        service4 = baas.Service()
        assert service4.param == param2

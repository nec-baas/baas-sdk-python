# -*- coding: utf-8 -*-
import os
import time
import shutil
import pytest
from requests.exceptions import HTTPError
import necbaas as baas
from . import util


# セッショントークンテスト
class TestSessionTokenFile(object):
    master_service = None
    # type: baas.Service

    def setup(self):
        if os.path.exists(os.path.expanduser("~/.baas/python")):
            shutil.rmtree(os.path.expanduser("~/.baas/python"))

    def test_save_session_token(self):
        """セッショントークンのセーブ・ロードが正常に実行できること"""
        service1 = util.create_service()
        util.setup_user(service1)

        # セッショントークン検証正常
        service1.verify_session_token()

        # セッショントークン保存（ディレクトリなし、新規ファイル生成）
        service1.save_session_token()

        # セッショントークン設定（新規設定）
        service2 = util.create_service()
        service2.load_session_token()

        assert service2.session_token == service1.session_token
        assert service2.session_token_expire == service1.session_token_expire

        baas.User.logout(service2)

        # セッショントークン保存（セッショントークン上書き）
        service3 = util.create_service()
        time.sleep(1)  # Wait to change the token
        baas.User.login(service3, username="user1", password="Passw0rD")
        service3.save_session_token()

        # セッショントークン設定（上書き設定）
        service4 = util.create_service()
        time.sleep(1)  # Wait to change the token
        baas.User.login(service4, username="user1", password="Passw0rD")
        assert service4.session_token != service3.session_token
        assert service4.session_token_expire != service3.session_token_expire

        service4.load_session_token()

        assert service4.session_token == service3.session_token
        assert service4.session_token_expire == service3.session_token_expire

        baas.User.logout(service4)

        # セッショントークンファイル削除
        baas.Service.delete_session_token_file()

        # セッショントークン設定（セッションクリア）
        service5 = util.create_service()
        time.sleep(1)  # Wait to change the token
        baas.User.login(service5, username="user1", password="Passw0rD")
        assert service5.session_token is not None
        assert service5.session_token_expire is not None

        service5.load_session_token()

        assert service5.session_token is None
        assert service5.session_token_expire is None

        with pytest.raises(HTTPError) as ei:
            baas.User.logout(service5)
        e = ei.value
        assert e.response.status_code == 401

        # セッショントークンファイル削除（二重削除）
        baas.Service.delete_session_token_file()

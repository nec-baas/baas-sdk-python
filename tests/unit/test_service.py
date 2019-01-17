# -*- coding: utf-8 -*-
from mock import patch, mock_open
import pytest
import json
import yaml
import time
import sys
import os
import io

import necbaas as baas

# for mock of open()
builtin = 'builtins'
if sys.version_info[0] == 2:
    builtin = '__builtin__'


class TestService(object):
    def get_sample_param(self):
        """テスト用のサンプルパラメータを返す"""
        return {
            "baseUrl": "http://localhost/api",
            "tenantId": "tenant1",
            "appId": "app1",
            "appKey": "key1"
        }

    def test_init(self):
        """正常に初期化できること"""
        param = self.get_sample_param()
        service = baas.Service(param)
        assert service.param == param
        assert service.param["baseUrl"] == "http://localhost/api"
        assert service.session_token is None

    def test_init_normalize_base_url(self):
        """baseUrl が正常に正規化されること"""
        param = self.get_sample_param()
        param["baseUrl"] = "http://localhost/api/"  # trailing slash
        service = baas.Service(param)
        assert service.param["baseUrl"] == "http://localhost/api"

    @pytest.mark.parametrize("base_url", [u"http://ホスト名/api/", "http://ホスト名/api"])
    def test_init_base_url_jp(self, base_url):
        """日本語 baseUrl が正常に初期化されること"""
        param = self.get_sample_param()
        param["baseUrl"] = base_url
        service = baas.Service(param)
        assert service.param["baseUrl"] == u"http://ホスト名/api"

    def _test_init_bad_sub(self, key):
        param = self.get_sample_param()
        del param[key]
        with pytest.raises(ValueError):
            baas.Service(param)

    def test_no_base_url(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("baseUrl")

    def test_no_tenant_id(self):
        """tenantId 指定がないときにエラーになること"""
        self._test_init_bad_sub("tenantId")

    def test_no_app_id(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("appId")

    def test_no_app_key(self):
        """baseUrl 指定がないときにエラーになること"""
        self._test_init_bad_sub("appKey")

    def test_init_with_file(self):
        """ファイルを使用して正常に初期化できること"""
        config_file = "baseUrl: http://localhost/api\n" \
            "tenantId: tenant1\n" \
            "appId: app1\n" \
            "appKey: key1\n" \
            "proxy:\n" \
            "  http: proxy.example.com:8080\n" \
            "  https: proxy.example2.com:8080\n"
 
        with patch("io.open", mock_open(read_data=config_file)):
            service = baas.Service()

        assert service.param["baseUrl"] == "http://localhost/api"
        assert service.param["tenantId"] == "tenant1"
        assert service.param["appId"] == "app1"
        assert service.param["appKey"] == "key1"
        proxy = service.param["proxy"]
        assert proxy["http"] == "proxy.example.com:8080"
        assert proxy["https"] == "proxy.example2.com:8080"

    def test_init_file_not_found(self):
        """設定ファイルが存在しない場合はエラーとなること"""
        m = mock_open()
        with patch("io.open", m) as mocked_open:
            mocked_open.side_effect = IOError()
            with pytest.raises(Exception):
                baas.Service()

        args_list = m.call_args_list
        assert args_list[0][0][0] == os.path.expanduser("~/.baas/python/python_config.yaml")
        assert args_list[1][0][0] == "/etc/baas/python/python_config.yaml"

    def test_save_config(self):
        """正常に設定情報を保存できること"""
        param = self.get_sample_param()
        service = baas.Service(param)

        path = "/tmp/config.yaml"
        m = mock_open()
        with patch("io.open", m, create=True):
            service.save_config(path)

        m.assert_called_with(path, 'w', encoding='utf-8')
        write_data = self._get_write_data(m)
        assert param == yaml.load(write_data)

    def _get_write_data(self, mock):
        handle = mock()
        write_string = ''
        for args in handle.write.call_args_list:
            write_string += args[0][0]
        return write_string

    def test_default_timeout(self):
        """正常にデフォルトタイムアウト値の操作ができること"""
        # 初期値
        assert  baas.Service.get_default_timeout() is None

        # 数値
        self._test_default_timeout(5)
        # Tuple
        self._test_default_timeout((3.05, 27))
        # 未設定
        self._test_default_timeout(None)

    def _test_default_timeout(self, value):
        baas.Service.set_default_timeout(value)
        assert baas.Service.get_default_timeout() is value

    @patch("necbaas.Service._do_request")
    def test_execute_rest(self, mock):
        """正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        service.session_token = "token1"

        query = {"a": 1}

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c", query=query)
        assert ret == {}

        method = mock.call_args[0][0]
        kwargs = mock.call_args[1]
        assert method == "GET"
        assert kwargs["url"] == "http://localhost/api/1/tenant1/a/b/c"
        assert kwargs["params"] == query

        headers = kwargs["headers"]
        assert headers["X-Application-Id"] == "app1"
        assert headers["X-Application-Key"] == "key1"
        assert headers["X-Session-Token"] == "token1"

        # timeout は含まれない
        assert "timeout" not in kwargs

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_timeout(self, mock):
        """正常にタイムアウト付きで REST API を呼び出せること"""
        baas.Service.set_default_timeout(10)

        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c")
        assert ret == {}

        timeout = mock.call_args[1]["timeout"]
        assert timeout is 10

    @patch("necbaas.Service._do_request")
    def test_execute_rest_jp(self, mock):
        """正常に日本語ありの URL で REST API を呼び出せること"""
        param = self.get_sample_param()
        param["baseUrl"] = u"http://ホスト名/api"
        service = baas.Service(param)

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c")
        assert ret == {}

        kwargs = mock.call_args[1]
        assert kwargs["url"] == "http://ホスト名/api/1/tenant1/a/b/c"

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_headers(self, mock):
        """ヘッダ付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        ret = service.execute_rest("GET", "a/b/c", headers={"X-header1": "xxx"})
        assert ret == {}

        headers = mock.call_args[1]["headers"]
        assert headers["X-header1"] == "xxx"

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_json(self, mock):
        """JSONボディ付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        service.execute_rest("POST", "a/b/c", json={"a": 1})

        kwargs = mock.call_args[1]
        assert kwargs["json"] == {"a": 1}

        # json 指定時は Content-Type ヘッダなし (requests 側で自動設定)
        headers = kwargs["headers"]
        assert "Content-Type" not in headers

    @patch("necbaas.Service._do_request")
    def test_execute_rest_with_data(self, mock):
        """data付きで正常に REST API を呼び出せること"""
        service = baas.Service(self.get_sample_param())

        mock.return_value = {}
        service.execute_rest("POST", "a/b/c", data="xxxxx")

        kwargs = mock.call_args[1]
        assert kwargs["data"] == "xxxxx"

        # data 指定時は Content-Type デフォルトは application/octet-stream
        headers = kwargs["headers"]
        assert headers["Content-Type"] == "application/octet-stream"

    def test_execute_rest_invalid_method(self):
        """不正なメソッドはエラーとなること"""
        service = baas.Service(self.get_sample_param())

        with pytest.raises(Exception):
            service.execute_rest("PATCH", "/a/b/c")

    @patch("os.path")
    def test_load_session_token(self, mock_path):
        """正常にセッショントークンが load できること"""
        mock_path.exists.return_value = True
        session_token = '{"sessionTokenExpire": 1534847297, "sessionToken": "testToken"}'

        service = baas.Service(self.get_sample_param())

        with patch(builtin + ".open", mock_open(read_data=session_token)):
            service.load_session_token()

        assert service.session_token == "testToken"
        assert service.session_token_expire == 1534847297

    @patch("os.path")
    def test_load_session_token_file_not_exists(self, mock_path):
        """セッショントークンファイルがない場合はセッショントークンをクリアすること"""
        mock_path.exists.return_value = False

        service = baas.Service(self.get_sample_param())
        service.session_token = "testToken"
        service.session_token_expire = 1534847297

        service.load_session_token()

        assert service.session_token is None
        assert service.session_token_expire is None

    def _test_load_session_token_file_invalid(self, mock_path, session_token):
        mock_path.exists.return_value = True

        service = baas.Service(self.get_sample_param())

        with patch(builtin + ".open", mock_open(read_data=session_token)):
            with pytest.raises(Exception):
                service.load_session_token()

    @patch("os.path")
    def test_load_session_token_file_session_token_none(self, mock_path):
        """セッショントークンがない場合はエラーとなること"""
        session_token = '{"sessionTokenExpire": 1534847297}'
        self._test_load_session_token_file_invalid(mock_path, session_token)

    @patch("os.path")
    def test_load_session_token_file_session_token_expire_none(self, mock_path):
        """セッショントークン期限がない場合はエラーとなること"""
        session_token = '{"sessionToken": "testToken"}'
        self._test_load_session_token_file_invalid(mock_path, session_token)

    @patch("os.path")
    @patch("os.makedirs")
    def test_save_session_token(self, mock_mkdirs, mock_path):
        """正常にセッショントークンが save できること"""
        mock_path.exists.return_value = False
        session_token = {
            "sessionToken": "testToken",
            "sessionTokenExpire": 1534847297}
        expected_token = json.dumps(session_token)

        service = baas.Service(self.get_sample_param())

        service.session_token = "testToken"
        service.session_token_expire = 1534847297

        m = mock_open()
        with patch(builtin + ".open", m, create=True):
            service.save_session_token()

        m.assert_called_with(baas.Service._SESSION_TOKEN_FILE_PATH, 'w')
        assert self._get_write_data(m) == expected_token

        mock_mkdirs.assert_called_once()

    @patch("os.path")
    def test_save_session_token_without_token(self, mock_path):
        """セッショントークンがない場合はエラーとなること"""
        mock_path.exists.return_value = True

        service = baas.Service(self.get_sample_param())

        service.session_token = None
        service.session_token_expire = None

        with pytest.raises(Exception):
            service.save_session_token()

    @patch("os.path")
    @patch("os.remove")
    def test_delete_session_token_file(self, mock_remove, mock_path):
        """正常にセッショントークンが delete できること"""
        mock_path.exists.return_value = True

        baas.Service.delete_session_token_file()

        mock_remove.assert_called_once()

    def test_verify_session_token(self):
        """正常にセッショントークンが検証できること"""
        service = baas.Service(self.get_sample_param())

        service.session_token = "testToken"
        service.session_token_expire = time.time() + 1

        service.verify_session_token()

    def test_verify_session_token_no_token(self):
        """正常にセッショントークンがない場合は例外が raise されること"""
        service = baas.Service(self.get_sample_param())

        with pytest.raises(Exception):
            service.verify_session_token()

    def test_verify_session_token_expired(self):
        """正常にセッショントークンが期限切れの場合は例外が raise されること"""
        service = baas.Service(self.get_sample_param())

        service.session_token = "testToken"
        service.session_token_expire = time.time()

        with pytest.raises(Exception):
            service.verify_session_token()

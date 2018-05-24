# -*- coding: utf-8 -*-
import re
import pytest
from requests import HTTPError

import necbaas as baas

from .test_storage_base import TestStorageBase


class TestFileStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("file")

    def teardown(self):
        self.cleanup()

    def create_test_data(self, length):
        """テストデータ生成"""
        ary = []
        for i in range(length):
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            idx = i % len(alphabet)
            ary.append(alphabet[idx:idx+1])
        return ''.join(ary)

    def upload_file_one(self):
        # type: () -> (baas.FileBucket, str, dict)
        b = baas.FileBucket(self.service, "bucket1")
        test_data = self.create_test_data(64)
        meta = b.create("file1.txt", data=test_data.encode(), content_type="plain/text")
        return b, test_data, meta

    def test_upload(self):
        """正常にuploadできること。日本語ファイル名も使用できること。"""
        b = baas.FileBucket(self.service, "bucket1")

        filename = "日本語.txt"

        # upload
        test_data = self.create_test_data(1024)
        meta = b.create(filename, data=test_data.encode(), content_type="plain/text")
        assert meta["filename"] == filename
        assert meta["length"] == len(test_data)
        assert meta["contentType"] == "plain/text"

        # download
        res = b.download(filename)
        assert res.status_code == 200
        assert res.text == test_data

        # stream download
        with b.download(filename, stream=True) as res:
            assert res.status_code == 200
            data = res.raw.read()
            assert data.decode() == test_data

    def test_get_metadata(self):
        """正常にメタデータ取得できること"""
        (b, data, meta) = self.upload_file_one()
        filename = meta["filename"]

        result = b.get_metadata(filename)
        assert result == meta

    @pytest.mark.parametrize("good_etag", [None, True, False])
    def test_update(self, good_etag):
        """
        正常に更新アップロードできること
        Args:
            good_etag: None - ETag なし、True - 正常 ETag、False - 異常 ETag

        Returns:

        """
        (b, data, meta) = self.upload_file_one()
        filename = meta["filename"]
        if good_etag is None:
            meta_etag = None
            file_etag = None
        elif good_etag:
            meta_etag = meta["metaETag"]
            file_etag = meta["fileETag"]
        else:
            meta_etag = "BAD_ETAG"
            file_etag = "BAD_ETAG"

        data = "12345".encode()

        if good_etag is None or good_etag:
            meta = b.update(filename, data, content_type="application/octet-stream", meta_etag=meta_etag,
                            file_etag=file_etag)
            assert meta["length"] == len(data)
            assert meta["contentType"] == "application/octet-stream"
        else:
            with pytest.raises(HTTPError) as ei:
                b.update(filename, data, content_type="application/octet-stream", meta_etag=meta_etag, file_etag=file_etag)
            status_code = ei.value.response.status_code
            assert status_code == 409

    @pytest.mark.parametrize("good_etag", [None, True, False])
    def test_update_metadata(self, good_etag):
        """
        正常にメタデータ更新できること
        Args:
            good_etag: None - ETag なし、True - 正常 ETag、False - 異常 ETag

        Returns:
        """
        (b, data, meta) = self.upload_file_one()
        filename = meta["filename"]
        if good_etag is None:
            etag = None
        elif good_etag:
            etag = meta["metaETag"]
        else:
            etag = "BAD_ETAG"

        # options 変更
        options = {"tag": "test data"}
        meta["options"] = options

        if good_etag is None or good_etag:
            new_meta = b.update_metadata(filename, meta, etag=etag)
            assert new_meta["options"] == options
            assert new_meta["metaETag"] != etag
        else:
            with pytest.raises(HTTPError) as ei:
                b.update_metadata(filename, meta, etag=etag)
            status_code = ei.value.response.status_code
            assert status_code == 409

    def test_query(self):
        """正常にクエリできること"""
        b = baas.FileBucket(self.service, "bucket1")

        # 初期状態では 0 件
        files = b.query()
        assert len(files) == 0

        # ファイル登録
        test_data = self.create_test_data(128)
        for i in range(5):
            b.create("file{}.txt".format(i), data=test_data.encode(), content_type="plain/text")
        files = b.query()
        assert len(files) == 5
        for file in files:
            assert re.match(r"^file\d.txt$", file["filename"])
            assert file["length"] == len(test_data)
            assert file["contentType"] == "plain/text"

    def test_remove(self):
        """正常に削除できること"""
        (b, data, meta) = self.upload_file_one()
        filename = meta["filename"]

        res = b.remove(filename)
        assert len(res) == 0  # empty json

        # ファイル削除確認
        assert len(b.query()) == 0


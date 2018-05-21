import json
import necbaas as baas

from .util import *


class TestFileBucket(object):
    def get_bucket(self, expected_result):
        service = mock_service_json_resp(expected_result)
        bucket = baas.FileBucket(service, "bucket1")
        return service, bucket

    def test_query(self):
        """正常にクエリできること"""
        expected_results = [{"name": "file1"}]
        service, bucket = self.get_bucket({"results": expected_results})

        results = bucket.query()
        assert results == expected_results

        assert get_rest_args(service) == ("GET", "/files/bucket1")

    def test_get_metadata(self):
        """正常にメタデータ取得できること"""
        expected_result = {"name": "file1"}
        service, bucket = self.get_bucket(expected_result)

        result = bucket.get_metadata("file1")
        assert result == expected_result

        assert get_rest_args(service) == ("GET", "/files/bucket1/file1")

    def test_update_metadata(self):
        """正常にメタデータ更新できること"""
        expected_result = {"name": "file1"}
        service, bucket = self.get_bucket(expected_result)

        meta = {}
        result = bucket.update_metadata("file1", meta, etag="etag1")
        assert result == expected_result

        assert get_rest_args(service) == ("PUT", "/files/bucket1/file1")
        kwargs = get_rest_kwargs(service)
        assert kwargs["json"] == meta
        assert kwargs["query"] == {"metaETag": "etag1"}

    def test_upload(self):
        """正常に新規アップロードできること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        data = "TEST DATA".encode()
        acl = {"r": "g:anonymous"}
        result = bucket.upload("file1", data, acl=acl)
        assert result == expected_result

        assert get_rest_args(service) == ("POST", "/files/bucket1/file1")
        kwargs = get_rest_kwargs(service)

        assert kwargs["data"] == data
        assert kwargs["headers"]["Content-Type"] == "application/octet-stream"
        assert kwargs["headers"]["X-ACL"] == json.dumps(acl)

    def test_update(self):
        """正常に更新アップロードできること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        data = "TEST DATA".encode()
        result = bucket.update("file1", data, content_type="text/plain", meta_etag="me1", file_etag="fe1")
        assert result == expected_result

        assert get_rest_args(service) == ("PUT", "/files/bucket1/file1")
        kwargs = get_rest_kwargs(service)

        assert kwargs["data"] == data
        assert kwargs["query"] == {"metaETag": "me1", "fileETag": "fe1"}
        assert kwargs["headers"]["Content-Type"] == "text/plain"
        assert "X-ACL" not in kwargs["headers"]

    def test_download(self):
        """正常にダウンロードできること"""
        resp = MagicMock()
        service = mock_service_resp(resp)
        bucket = baas.FileBucket(service, "bucket1")

        result = bucket.download("file1")
        assert result == resp

        assert get_rest_args(service) == ("GET", "/files/bucket1/file1")
        assert get_rest_kwargs(service)["stream"] == False

    def test_remove(self):
        """正常に削除できること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        result = bucket.remove("file1")
        assert result == expected_result

        assert get_rest_args(service) == ("DELETE", "/files/bucket1/file1")

# -*- coding: utf-8 -*-
import pytest

import necbaas as baas

from .util import *


class TestBuckets(object):
    def get_bucket(self, expected_result):
        service = mock_service_json_resp(expected_result)
        bucket = baas.Buckets(service, "object")
        return service, bucket

    def test_init(self):
        """正常に初期化できること"""
        service = mock_service_json_resp("")
        bucket = baas.Buckets(service, "file")

        assert bucket.service == service
        assert bucket.bucket_type == "file"

    def test_init_bad_bucket_type(self):
        """バケットタイプが不正の場合はエラーになること"""
        service = mock_service_json_resp("")
        with pytest.raises(ValueError):
            baas.Buckets(service, "type")

    def test_upsert(self):
        """正常に upsert できること"""
        expected = {"name": "bucket1", "description": "test bucket"}
        service, bucket = self.get_bucket(expected)

        acl = {"r": ["g:anonymous"], "w": ["user1"]}
        content_acl = {"r": ["g:authenticated"]}

        result = bucket.upsert(name="bucket1", acl=acl, content_acl=content_acl)
        assert result == expected

        assert get_rest_args(service) == ("PUT", "buckets/object/bucket1")
        json = get_rest_kwargs(service)["json"]
        assert json["description"] == ""
        assert json["ACL"] == acl
        assert json["contentACL"] == content_acl

    def test_query(self):
        """正常に検索できること"""
        expected = [{"name": "bucket01", "description": "test bucket01"}, {"name": "bucket02", "description": "test bucket02"}]
        service, bucket = self.get_bucket({"results": expected})

        results = bucket.query()
        assert results == expected

        assert get_rest_args(service) == ("GET", "buckets/object")

    def test_get(self):
        """正常に取得できること"""
        expected = {"name": "bucket1", "description": "test bucket"}
        service, bucket = self.get_bucket(expected)

        result = bucket.get("bucket1")
        assert result == expected

        assert get_rest_args(service) == ("GET", "buckets/object/bucket1")

    def test_remove(self):
        """正常に削除できること"""
        expected = {}
        service, bucket = self.get_bucket(expected)

        result = bucket.remove("bucket1")
        assert result == expected

        assert get_rest_args(service) == ("DELETE", "buckets/object/bucket1")

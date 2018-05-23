# -*- coding: utf-8 -*-
import json
from mock import MagicMock
import pytest

import necbaas as baas

from .util import *


class TestObjectBucket(object):
    def get_bucket(self, expected_result):
        service = mock_service_json_resp(expected_result)
        bucket = baas.ObjectBucket(service, "bucket1")
        return service, bucket

    def test_query(self):
        """正常にクエリできること"""
        expected_results = [{"key1": 1}, {"key1": 2}]
        service, bucket = self.get_bucket({"results": expected_results})

        where = {"key1": 12345}
        order = "key1,-key2"
        skip = 500
        limit = 100
        projection = {"key1": 1, "key2": 1, "key3": 1}

        results = bucket.query(where=where, order=order, skip=skip, limit=limit, projection=projection)
        assert results == expected_results

        assert get_rest_args(service) == ("GET", "/objects/bucket1")
        query = get_rest_kwargs(service)["query"]
        assert query["where"] == json.dumps(where)
        assert query["order"] == order
        assert query["skip"] == skip
        assert query["limit"] == limit
        assert query["projection"] == json.dumps(projection)

    def test_insert(self):
        """正常に INSERT できること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        data = {"key1": 1}
        result = bucket.insert(data)
        assert result == expected_result

        assert get_rest_args(service) == ("POST", "/objects/bucket1")
        req_json = get_rest_kwargs(service)["json"]
        assert req_json == data

    def test_update(self):
        """正常に update できること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        data = {"key1": 2}
        result = bucket.update("oid1", data, "etag1")
        assert result == expected_result

        assert get_rest_args(service) == ("PUT", "/objects/bucket1/oid1")
        kwargs = get_rest_kwargs(service)
        assert kwargs["json"] == data
        assert kwargs["query"]["etag"] == "etag1"

    def test_remove(self):
        """正常に削除できること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        result = bucket.remove("oid1")
        assert result == expected_result

        assert get_rest_args(service) == ("DELETE", "/objects/bucket1/oid1")
        assert get_rest_kwargs(service)["query"] == {"deleteMark": 0}

    def test_remove_with_query(self):
        """正常に削除できること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        where = {"key1": 1}
        result = bucket.remove_with_query(where=where)
        assert result == expected_result

        assert get_rest_args(service) == ("DELETE", "/objects/bucket1")
        query = get_rest_kwargs(service)["query"]
        assert query["where"] == json.dumps(where)
        assert query["deleteMark"] == 0

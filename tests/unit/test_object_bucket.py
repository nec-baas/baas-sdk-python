# -*- coding: utf-8 -*-
import json
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

        results = bucket.query(where=where, order=order, skip=skip, limit=limit, projection=projection, delete_mark=True)
        assert results == expected_results

        assert get_rest_args(service) == ("GET", "/objects/bucket1")
        query = get_rest_kwargs(service)["query"]
        assert query["where"] == json.dumps(where)
        assert query["order"] == order
        assert query["skip"] == skip
        assert query["limit"] == limit
        assert query["projection"] == json.dumps(projection)
        assert query["deleteMark"]

    def test_query_max(self):
        """正常にクエリできること(クエリサイズMAX)"""
        expected_results = [{"key1": 1}, {"key1": 2}]
        service, bucket = self.get_bucket({"results": expected_results})

        # where%3d%7b%22key1%22%3a+%22[data]%22%7d -> 33byte + data
        data = "a" * (1499 - 32)
        where = {"key1": data}

        results = bucket.query(where=where)
        assert results == expected_results

        assert get_rest_args(service) == ("GET", "/objects/bucket1")
        query = get_rest_kwargs(service)["query"]
        assert query["where"] == json.dumps(where)

    def test_long_query(self):
        """正常にロングクエリできること"""
        expected_results = [{"key1": 1}, {"key1": 2}]
        service, bucket = self.get_bucket({"results": expected_results})

        # where%3d%7b%22key1%22%3a+%22[data]%22%7d -> 33byte + data
        data = "a" * (1500 - 32)
        where = {"key1": data}

        results = bucket.query(where=where)
        assert results == expected_results

        assert get_rest_args(service) == ("POST", "/objects/bucket1/_query")
        query = get_rest_kwargs(service)["json"]
        assert query["where"] == json.dumps(where)

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

    def test_remove_empty_oid(self):
        """oid が空の場合はエラーとなること"""
        expected_result = {}
        service, bucket = self.get_bucket(expected_result)

        with pytest.raises(ValueError):
            bucket.remove("")

    def test_batch(self):
        """正常に batch できること"""
        expected_result = [{"result": "ok", "_id": "id1"}, {"result": "conflict", "reasonCode": "etag_mismatch"}]
        service, bucket = self.get_bucket({"results": expected_result})

        requests = [{"op": "insert", "data": {"key": "val"}}]
        result = bucket.batch(requests)
        assert result == expected_result

        assert get_rest_args(service) == ("POST", "/objects/bucket1/_batch")
        kwargs = get_rest_kwargs(service)
        assert kwargs["json"] == {"requests": requests}

    def test_aggregate(self):
        """正常に aggregate できること"""
        expected_result = [{"data": 123}, {"key": "val", "key2": 1000}]
        service, bucket = self.get_bucket({"results": expected_result})

        pipeline = [{"$lookup": {"from": "inventoryTestBucket", "localField": "item", "foreignField": "sku", "as": "inventory_docs"}}]
        options = {"allowDiskUse": True}
        result = bucket.aggregate(pipeline, options)
        assert result == expected_result

        assert get_rest_args(service) == ("POST", "/objects/bucket1/_aggregate")
        kwargs = get_rest_kwargs(service)
        assert kwargs["json"] == {"pipeline": pipeline, "options": options}

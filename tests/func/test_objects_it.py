# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError

import necbaas as baas
from .test_storage_base import TestStorageBase


class TestObjectStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("object")

    def teardown(self):
        self.cleanup()

    def insert_sample_data(self, count):
        # type: () -> baas.ObjectBucket
        b = baas.ObjectBucket(self.service, "bucket1")

        for i in range(count):
            #print(i)
            b.insert({"key": i})

        return b

    def test_crud(self):
        """追加・更新・クエリ・削除が実行できること"""
        b = baas.ObjectBucket(self.service, "bucket1")

        # insert
        res = b.insert({"key1": 12345})
        assert res["key1"] == 12345

        # update
        res = b.update(res["_id"], {"key1": 23456}, etag=res["etag"])
        assert res["key1"] == 23456

        # query
        results = b.query(where={"key1": 23456})
        assert len(results) == 1
        assert results[0]["key1"] == 23456

        # remove
        _id = results[0]["_id"]
        res = b.remove(_id)
        assert len(res) == 0

        # remove with query
        res = b.remove_with_query({})
        assert res["result"] == "ok"
        assert res["deletedObjects"] == 0

    def test_query_all(self):
        """全件検索できること"""
        b = self.insert_sample_data(10)

        results = b.query()
        assert len(results) == 10

    def test_query_with_condition(self):
        """条件付きクエリできること"""
        b = self.insert_sample_data(10)
        where = {"key": {"$lt": 9}}
        projection = {"createdAt": 0}
        results = b.query(where=where, order="-key", skip=2, limit=5, projection=projection)
        assert len(results) == 5  # limit
        assert results[0]["key"] == 6  # where, order, skip
        assert results[4]["key"] == 2
        assert "createdAt" not in results[0]  # projection
        assert "updatedAt" in results[0]

    def test_query_with_count(self):
        """件数付きクエリできること"""
        b = self.insert_sample_data(10)

        (results, count) = b.query_with_count(limit=5)
        assert len(results) == 5
        assert count == 10

    @pytest.mark.parametrize("good_etag", [None, True, False])
    def test_update(self, good_etag):
        """正常に update できること"""
        b = baas.ObjectBucket(self.service, "bucket1")
        data = {"key": 1}
        data = b.insert(data)

        data["key"] = 100
        oid = data["_id"]
        if good_etag is None:
            etag = None
        elif good_etag:
            etag = data["etag"]
        else:
            etag = "BAD_ETAG"

        if good_etag is None or good_etag:
            new_data = b.update(oid, data, etag=etag)
            assert new_data["key"] == 100
        else:
            with pytest.raises(HTTPError) as ei:
                b.update(oid, data, etag=etag)
            status_code = ei.value.response.status_code
            assert status_code == 409

    @pytest.mark.parametrize("soft_delete", [None, True, False])
    def test_remove(self, soft_delete):
        """正常に削除できること"""
        b = self.insert_sample_data(1)
        objs = b.query()

        oid = objs[0]["_id"]
        if soft_delete is None:
            res = b.remove(oid)
        else:
            res = b.remove(oid, soft_delete=soft_delete)

        if soft_delete:
            assert res["_deleted"] == soft_delete
        else:
            assert len(res) == 0

    def test_remove_with_query(self):
        """正常に一括削除できること"""
        b = self.insert_sample_data(10)
        assert len(b.query()) == 10

        where = {"key": {"$gt": 3}}  # 0, 1, 2, 3 だけ残る
        res = b.remove_with_query(where=where)
        assert res["result"] == "ok"
        assert res["deletedObjects"] == 6

        assert len(b.query()) == 4

        # 全件削除
        res = b.remove_with_query()
        assert res["result"] == "ok"
        assert res["deletedObjects"] == 4

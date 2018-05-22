import necbaas as baas
from .test_storage_base import TestStorageBase


class TestObjectStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("object")

    def teardown(self):
        self.cleanup()

    def insert_sample_data(self):
        # type: () -> baas.ObjectBucket
        b = baas.ObjectBucket(self.service, "bucket1")

        for i in range(10):
            #print(i)
            b.insert({"key": i})

        return b

    def test_crud(self):
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
        assert res["_id"] == _id

        # remove with query
        res = b.remove_with_query({})
        assert res["result"] == "ok"
        assert res["deletedObjects"] == 0

    def test_query_all(self):
        """全件検索できること"""
        b = self.insert_sample_data()

        results = b.query()
        assert len(results) == 10

    def test_query_with_condition(self):
        """条件付きクエリできること"""
        b = self.insert_sample_data()
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
        b = self.insert_sample_data()

        (results, count) = b.query_with_count(limit=5)
        assert len(results) == 5
        assert count == 10


import necbaas as baas
from .test_storage_base import TestStorageBase


class TestObjectStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("object")

    def teardown(self):
        self.cleanup()

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

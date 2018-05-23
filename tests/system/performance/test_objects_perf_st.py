# -*- coding: utf-8 -*-
import time
from requests import HTTPError
import necbaas as baas
from tests.func import util


#@pytest.mark.skip(reason="manual test")
class TestObjectsPerformance(object):
    """オブジェクトストレージ性能テスト"""

    service = None
    # type: baas.Service
    master_service = None
    # type: baas.Service
    bucket = None
    # type: baas.ObjectBucket

    TEST_BUCKET = "performance1"

    def setup(self):
        self.service = util.create_service()
        self.master_service = util.create_service(master=True)

        # ensure bucket
        buckets = baas.Buckets(self.master_service, "object")
        buckets.upsert(self.TEST_BUCKET, desc="performance test",
                       acl={}, content_acl={"r": ["g:anonymous"], "w": ["g:anonymous"]})

        self.bucket = baas.ObjectBucket(self.service, self.TEST_BUCKET)

        (res, total) = self.bucket.query_with_count(limit=1)
        if total == 10000:
            # ok, test data exists
            return
        elif total > 0:
            # re-create buckets
            buckets.remove(self.TEST_BUCKET)
            buckets.upsert(self.TEST_BUCKET, content_acl={"r": ["g:anonymous"], "w": ["g:anonymous"]})

        self.create_test_data_10000()

    def create_test_data_10000(self):
        """10,000件のテストデータを生成する"""
        # do batch operation: 500 * 20 = 10,000 objects
        requests = []
        for i in range(500):
            requests.append({
                "op": "insert",
                "data": {
                    "key": i
                }
            })
        # execute batch
        for i in range(20):
            # print("batch = {}".format(500 * (i+1)), flush=True)
            results = self.bucket.batch(requests)
            assert len(results) == 500

    def drop_test_object_bucket(self):
        buckets = baas.Buckets(self.master_service, "object")
        try:
            buckets.remove(self.TEST_BUCKET)
        except HTTPError:
            pass  # just ignore

    def test_obj_write(self):
        """オブジェクトストレージ書き込み性能"""
        # start test
        count = 100
        start = time.time()
        for i in range(count):
            # print(i)
            # stdout.flush()
            self.bucket.insert({"write_test": 10000 + i})
        elapsed = time.time() - start
        print("Object write: elapsed time: total = {} sec, each write(average) = {} sec".format(elapsed, elapsed / count))

        # clear data
        self.bucket.remove_with_query({"write_test": {"$exists": True}})

    def test_obj_query(self):
        """オブジェクトストレージ検索性能"""
        # execute query
        start = time.time()
        count = 100
        for i in range(count):
            objs = self.bucket.query(skip=i*100, limit=100)
            assert len(objs) == 100
        elapsed = time.time() - start
        print("Object query(100 of 10000): elapsed time: total = {} sec, average = {}".format(elapsed, elapsed / count))

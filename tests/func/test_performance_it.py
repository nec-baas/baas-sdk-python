# -*- coding: utf-8 -*-
import pytest
import time
import necbaas as baas
from . import util


@pytest.mark.skip(reason="manual test")  # テスト実行時にこの行を手動でコメントアウトすること
class TestPerformance(object):
    """性能テスト"""

    service = None
    # type: baas.Service
    master_service = None
    # type: baas.Service

    def setup(self):
        self.service = util.create_service()
        self.master_service = util.create_service(master=True)

    def create_test_object_bucket(self):
        # create bucket
        buckets = baas.Buckets(self.master_service, "object")
        buckets.upsert("performance", content_acl={"r": ["g:anonymous"], "w": ["g:anonymous"]})
        return baas.ObjectBucket(self.service, "performance")

    def drop_test_object_bucket(self):
        buckets = baas.Buckets(self.master_service, "object")
        buckets.remove("performance")

    def test_obj_write(self):
        """オブジェクトストレージ書き込み性能"""
        # create bucket
        bucket = self.create_test_object_bucket()

        # start test
        count = 100
        start = time.time()
        for i in range(count):
            print(i)
            bucket.insert({"key": i})
        elapsed = time.time() - start
        print("Object write: elapsed time: total = {} sec, each write(average) = {} sec".format(elapsed, elapsed / count))

        self.drop_test_object_bucket()

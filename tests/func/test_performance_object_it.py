# -*- coding: utf-8 -*-
import os
import csv
import time
import pytest

import necbaas as baas
from .test_storage_base import TestStorageBase


class TestPerformanceObject(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("object")

    def teardown(self):
        self.cleanup()
        self.remove_all_buckets()

    def _register_object(self, bucket_name, size, count):
        b = baas.ObjectBucket(self.service, bucket_name)

        test_data = self.create_test_data(size)

        requests = []
        for i in range(count):
            request = {
                "op": "insert",
                "data": {
                    "DATA_ID": i,
                    "DATA": test_data
                }
            }
            requests.append(request)

        b.batch(requests)

    def _query_object(self, bucket_name, size, count):
        b = baas.ObjectBucket(self.service, bucket_name)

        objects, c = b.query_with_count(limit=-1, order="DATA_ID")

        assert c == count
        assert len(objects) == count

        for i in range(count):
            assert objects[i]["DATA_ID"] == i
            assert len(objects[i]["DATA"]) == size

        return objects

    @pytest.mark.skip(reason='performance test')
    def test_object_count(self):
        """最大オブジェクト数"""
        object_num = 10000
        object_size = 1024

        self._register_object("bucket1", object_size, object_num)
        self._query_object("bucket1", object_size, object_num)

    @pytest.mark.skip(reason='performance test')
    def test_object_size(self):
        """最大オブジェクトサイズ"""
        object_num = 8
        object_size = 256 * 1024

        self._register_object("bucket1", object_size, object_num)
        self._query_object("bucket1", object_size, object_num)

    @pytest.mark.skip(reason='performance test')
    def test_bucket_count(self):
        """最大バケットサイズ"""
        bucket_num = 1000
        object_num = 2000
        object_size = 1024

        self.remove_all_buckets()

        for i in range(bucket_num):
            self.buckets.upsert("bucket" + str(i), content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

        for i in range(bucket_num):
            self._register_object("bucket" + str(i), object_size, object_num)

        for i in range(bucket_num):
            self._query_object("bucket" + str(i), object_size, object_num)

    def _import_csv(self):
        with open(os.path.expanduser("~/.baas/TestData_1KB_10000Item.csv"), "r") as f:
            reader = csv.DictReader(f)

            requests = []
            for row in reader:
                request = {"op": "insert", "data": row}
                requests.append(request)

            self.bucket.batch(requests)

    @pytest.mark.skip(reason='performance test')
    def test_crud_time(self):
        """CRUD実行時間 (1件)"""
        self.bucket = baas.ObjectBucket(self.service, "bucket1")
        self._import_csv()

        # query
        numbers = []
        for i in range(10000):
            numbers.append(str((i + 1) * 100))
        where = {"NO": {"$in": numbers}}

        start_time = time.time()
        objects = self.bucket.query(where=where, limit=-1)
        elapsed_time = time.time() - start_time

        assert len(objects) == 100
        assert elapsed_time < 0.3
        print("query time: " + str(elapsed_time))

        # create
        start_time = time.time()
        obj = self.bucket.insert({"key": "value"})
        elapsed_time = time.time() - start_time

        assert obj["key"] == "value"
        assert elapsed_time < 0.1
        print("create time: " + str(elapsed_time))

        # update
        start_time = time.time()
        obj = self.bucket.update(obj["_id"], {"key2": "value2"})
        elapsed_time = time.time() - start_time

        assert obj["key2"] == "value2"
        assert elapsed_time < 0.1
        print("update time: " + str(elapsed_time))

        # delete
        start_time = time.time()
        self.bucket.remove(obj["_id"])
        elapsed_time = time.time() - start_time

        assert elapsed_time < 0.1
        print("delete time: " + str(elapsed_time))

    @pytest.mark.skip(reason='durability test')
    def test_durability_object(self):
        """耐久試験：オブジェクトストレージ 検索／更新"""
        self.bucket = baas.ObjectBucket(self.service, "bucket1")
        self._import_csv()

        objects, count = self.bucket.query_with_count()
        assert count == 10000

        update_id = objects[0]["_id"]

        end_time = time.time() + (48 * 60 * 60)

        counter = 0

        while end_time >= time.time():
            # update
            obj = self.bucket.update(update_id, {"updateKey": counter})
            assert obj["updateKey"] == counter

            # query
            target = "ANTC-CD{:05}".format((counter % 100) * 100)
            where = {"CD": {"$gte": target}}

            objects = self.bucket.query(where=where, limit=100)
            assert len(objects) == 100

            counter += 1

            # sleep 1sec
            time.sleep(1)

            # update session token
            if self.service.session_token_expire - (60 * 60) < time.time():
                baas.User.login(self.service, username="user1", password="Passw0rD")

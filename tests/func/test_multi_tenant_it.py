# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class TestMultiTenant(object):
    def setup(self):
        self._setup(key="service", num=1)
        self._setup(key="service2", num=2)

    def _setup(self, key, num):
        master_service = util.create_service(master=True, key=key)

        util.remove_all_users(key)
        user = baas.User(master_service)
        user.username = "user" + str(num)
        user.email = "user" + str(num) + "@example.com"
        user.password = "Passw0rD" + str(num)
        user.register()

        buckets = baas.Buckets(master_service, "object")

        bucket_name = "bucket" + str(num)
        try:
            buckets.remove(bucket_name)
        except HTTPError:
            pass

        buckets.upsert(bucket_name, content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

    def teardown(self):
        self._cleanup(key="service", num=1)
        self._cleanup(key="service2", num=2)

    def _cleanup(self, key, num):
        master_service = util.create_service(master=True, key=key)

        try:
            buckets = baas.Buckets(master_service, "object")
            buckets.remove("bucket" + str(num))
        except HTTPError:
            pass

        util.remove_all_users(key)

    def test_multi_tenant(self):
        """マルチテナント：テナント毎にREST APIが実行できること"""
        service1 = util.create_service(key="service")
        service2 = util.create_service(key="service2")

        baas.User.login(service1, username="user1", password="Passw0rD1")
        baas.User.login(service2, username="user2", password="Passw0rD2")

        b1 = baas.ObjectBucket(service1, "bucket1")
        b2 = baas.ObjectBucket(service2, "bucket2")

        res1 = b1.insert({"key1": 12345})
        assert res1["key1"] == 12345

        res2 = b2.insert({"key2": 23456})
        assert res2["key2"] == 23456

        results1 = b1.query()
        assert len(results1) == 1
        assert results1[0]["key1"] == 12345

        results2 = b2.query()
        assert len(results2) == 1
        assert results2[0]["key2"] == 23456

        baas.User.logout(service1)
        baas.User.logout(service2)

# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError

import necbaas as baas
from . import util


class TestBucket(object):
    service = None
    # type: baas.Service

    def setup(self):
        self.masterService = util.create_service(master=True)

    def teardown(self):
        for b in self.bucket.query():
            self.bucket.remove(b["name"])

    def test_upsert(self):
        """正常にバケット作成・更新できること"""
        self.bucket = baas.Buckets(self.masterService, "object")

        # create
        create_res = self.bucket.upsert("bucket1")

        assert create_res["name"] == "bucket1"
        assert create_res["description"] == ""
        assert "ACL" in create_res
        assert "contentACL" in create_res

        # update
        with pytest.raises(HTTPError) as ei:
            self.bucket.upsert("bucket1")
        status_code = ei.value.response.status_code
        assert status_code == 400

    def test_upsert_with_options(self):
        """正常にバケット作成・更新できること"""
        self.bucket = baas.Buckets(self.masterService, "file")

        # create
        desc = "test bucket description"
        acl = {"u": ["g:authenticated"]}
        content_acl = {"d": ["g:anonymous"]}
        res = self.bucket.upsert("bucket1", desc=desc, acl=acl, content_acl=content_acl)

        assert res["name"] == "bucket1"
        assert res["description"] == desc
        assert res["ACL"]["u"] == ["g:authenticated"]
        assert res["contentACL"]["d"] == ["g:anonymous"]

        # update
        desc = "upsert description"
        acl = {"u": ["g:anonymous"]}
        content_acl = {"d": ["g:authenticated"]}
        res = self.bucket.upsert("bucket1", desc=desc, acl=acl, content_acl=content_acl)

        assert res["name"] == "bucket1"
        assert res["description"] == desc
        assert res["ACL"]["u"] == ["g:anonymous"]
        assert res["contentACL"]["d"] == ["g:authenticated"]

    def test_query(self):
        """正常にバケット全件検索できること"""
        self.bucket = baas.Buckets(self.masterService, "object")
        num = 10
        for i in range(num):
            self.bucket.upsert("bucket" + str(i))

        # query
        results = self.bucket.query()

        assert len(results) == num
        for i in range(num):
            assert results[i]["name"] == "bucket" + str(i)

    def test_get(self):
        """正常にバケット取得できること"""
        self.bucket = baas.Buckets(self.masterService, "object")
        create_res = self.bucket.upsert("bucket1")

        # get
        get_res = self.bucket.get("bucket1")
        assert create_res == get_res

    def test_remove(self):
        """正常にバケット削除できること"""
        self.bucket = baas.Buckets(self.masterService, "object")
        self.bucket.upsert("bucket1")

        # remove
        self.bucket.remove("bucket1")

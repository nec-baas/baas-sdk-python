# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class TestStorageBase(object):
    service = None
    # type: baas.Service
    masterService = None
    # type: baas.Service
    user = None
    # type: baas.User
    buckets = None
    # type: baas.Buckets

    def setup_bucket_and_user(self, bucket_type):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)

        self.buckets = baas.Buckets(self.masterService, bucket_type)

        self.user = util.setup_user(self.service)

        try:
            self.buckets.remove("bucket1")
        except HTTPError:
            pass

        # Create test bucket
        self.buckets.upsert("bucket1", content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

    def cleanup(self):
        try:
            self.buckets.remove("bucket1")
        except HTTPError:
            pass  # ignore...

        try:
            baas.User.logout(self.service)
        except HTTPError:
            pass  # ignore...

        try:
            users = baas.User.query(self.masterService, username="user1")
            baas.User.remove(self.masterService, users[0]["_id"])
        except HTTPError:
            pass  # ignore...

    def remove_all_buckets(self):
        for bucket in self.buckets.query():
            self.buckets.remove(bucket["name"])

    def create_test_data(self, length):
        """テストデータ生成"""
        ary = []
        for i in range(length):
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            idx = i % len(alphabet)
            ary.append(alphabet[idx:idx+1])
        return ''.join(ary)

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

        util.remove_all_users()

        # Register user
        user = baas.User(self.service)
        user.username = "user1"
        user.email = "user1@example.com"
        user.password = "Passw0rD"
        user.register()
        self.user = user

        # Login
        baas.User.login(self.service, username=user.username, password=user.password)

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

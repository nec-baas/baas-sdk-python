from unittest import TestCase
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class ObjectStorageIT(TestCase):
    service = None
    # type: baas.Service
    masterService = None
    # type: baas.Service
    user = None
    # type: baas.User

    def setUp(self):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)

        util.remove_all_users()

        # Register user
        user = baas.User(self.service)
        user.username = "user1"
        user.email = "user1@example.com"
        user.password = "Passw0rD"
        user.register()
        self.user = user

        # Login
        baas.User.login_with_username(self.service, user.username, user.password)

        # Create test bucket
        baas.Buckets.upsert(self.masterService, "object", "bucket1",
                            content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

    def tearDown(self):
        try:
            baas.Buckets.remove(self.masterService, "object", "bucket1")
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

    def test_crud(self):
        b = baas.ObjectBucket(self.service, "bucket1")

        # insert
        res = b.insert({"key1": 12345})
        self.assertEqual(res["key1"], 12345)

        # update
        res = b.update(res["_id"], {"key1": 23456}, etag=res["etag"])
        self.assertEqual(res["key1"], 23456)

        # query
        res = b.query(where={"key1": 23456})
        results = res["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["key1"], 23456)

        # remove
        _id = results[0]["_id"]
        res = b.remove(_id)
        self.assertEqual(res["_id"], _id)

        # remove with query
        res = b.remove_with_query({})
        self.assertEqual(res["result"], "ok")
        self.assertEqual(res["deletedObjects"], 0)

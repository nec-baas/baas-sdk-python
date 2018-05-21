from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class TestObjectStorage(object):
    service = None
    # type: baas.Service
    masterService = None
    # type: baas.Service
    user = None
    # type: baas.User
    buckets = None
    # type: baas.Buckets

    def setup(self):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)

        self.buckets = baas.Buckets(self.masterService, "object")

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

        # Create test bucket
        self.buckets.upsert("bucket1", content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

    def teardown(self):
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

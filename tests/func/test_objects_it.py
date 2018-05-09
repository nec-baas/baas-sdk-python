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

    def tearDown(self):
        try:
            baas.User.logout(self.service)
        except HTTPError:
            pass  # ignore...

        try:
            users = baas.User.query(self.masterService, username="user1")
            baas.User.remove(self.masterService, users[0]["_id"])
        except HTTPError:
            pass  # ignore...

    def test1(self):
        pass

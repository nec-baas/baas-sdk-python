from unittest import TestCase
import requests
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class UserIT(TestCase):
    service = None
    # type: baas.Service
    masterService = None
    # type: baas.Service

    def setUp(self):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)
        util.remove_all_users()

    def register_user(self):
        u = baas.User(self.service)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "Passw0rD"
        u.options = {"realname": "Foo Bar"}
        u.register()
        return u

    def test_register(self):
        u = baas.User(self.service)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "Passw0rD"
        u.options = {"realname": "Foo Bar"}

        res = u.register()
        print(res)

        try:
            u.register()
        except HTTPError as e:
            s = e.response.status_code
            self.assertEqual(s, 409)

    def test_query(self):
        self.register_user()

        # query all
        users = baas.User.query(self.masterService)
        self.assertEqual(len(users), 1)

        # query by user id
        users = baas.User.query(self.masterService, username="user1")
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "user1")

        # query by email
        users = baas.User.query(self.masterService, email="user1@example.com")
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "user1")

        # no result
        try:
            baas.User.query(self.masterService, username="no_such_user")
        except HTTPError as e:
            self.assertEqual(e.response.status_code, 404)

    def test_login_logout(self):
        u = self.register_user()
        self.assertEqual(self.service.session_token, None)

        res = baas.User.login(self.service, {"username": u.username, "password": u.password})
        #print(res)

        self.assertNotEqual(self.service.session_token, None)

        res = baas.User.logout(self.service)
        self.assertEqual(self.service.session_token, None)



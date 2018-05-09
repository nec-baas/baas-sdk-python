from unittest import TestCase
import requests

import necbaas as baas
from . import util


class UserIT(TestCase):
    def test_register(self):
        s = util.create_service()

        u = baas.User(s)
        u.username = "user1"
        u.email = "user1@example.com"
        u.password = "Passw0rD"
        u.options = {"realname": "Foo Bar"}

        res = u.register()
        print(res)

        try:
            u.register()
        except requests.exceptions.HTTPError as e:
            s = e.response.status_code
            self.assertEqual(s, 409)

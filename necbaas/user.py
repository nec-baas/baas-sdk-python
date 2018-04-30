# -*- coding: utf-8 -*-
import json


class User(object):
    """
    User

    :param Service service: Service

    Attributes
    ----------
    username : str
        Username
    email : str
        E-mail address
    password : str
        Password
    options : dict
        Options
    """

    def __init__(self, service):
        self.service = service
        self.username = None
        self.email = None
        self.password = None
        self.options = None

    @staticmethod
    def login_with_username(service, username, password):
        """
        Login with user name

        Example::

            result = necbaas.User.login_with_username(service, "foo", "Passw0rD")

        :param service: Service
        :param str username: User name
        :param str password: Password
        :return: Response JSON in dictionary
        """
        return User.login(service, {
            "username": username,
            "password": password
        })

    @staticmethod
    def login_with_email(service, email, password):
        """
        Login with E-mail

        Example::

            result = necbaas.User.login_with_email(service, "foo@example.com", "Passw0rD")

        :param service: Service
        :param str email: User name
        :param str password: Password
        :return: Response JSON in dictionary
        """
        return User.login(service, {
            "email": email,
            "password": password
        })

    @staticmethod
    def login(service, param):
        """
        Login

        Example::

            result = necbaas.User.login(service, {
                "username": "foo",
                "password": "Passw0rD"
            })

        :param service: Service
        :param dict param: dictionary. The parameter is encoded in JSON and sent to server.
            Usually contains username or email, and password.
        :return: Response JSON in dictionary
        """
        f = service.execute_rest("POST", "/login", None, json.dumps(param).encode("utf-8"))
        res = json.loads(f.read())

        session_token = res["sessionToken"]
        service.set_session_token(session_token)
        return res

    @staticmethod
    def logout(service):
        """
        Logout

        :param service: Service
        :return: Response JSON in dictionary
        """
        f = service.execute_rest("DELETE", "/login")
        res = json.loads(f.read())
        service.set_session_token(None)
        return res

    def register(self):
        """
        Register user.
        Specify username, email, password and options properties.

        Example::

            user = necbaas.User(service)
            user.username = "foo"
            user.email = "foo@example.com"
            user.password = "Passw0rD"
            response = user.register()

        :return: Registration info (JSON)
        """
        body = {}
        if self.username is not None:
            body["username"] = self.username
        if self.email is not None:
            body["email"] = self.email
        if self.password is not None:
            body["password"] = self.password
        if self.options is not None:
            body["options"] = self.options

        f = self.service.execute_rest("POST", "/users", None, body)
        res = json.loads(f.read())
        return res

    @staticmethod
    def query(service, username=None, email=None):
        """
        Query user.

        :param Service service: Service
        :param username: Username
        :param email: E-mail
        :return: Response JSON in dictionary
        """
        query = {}
        if username is not None:
            query["username"] = username
        if email is not None:
            query["email"] = email

        f = service.execute_rest("GET", "/users", query)
        res = json.loads(f.read())
        return res

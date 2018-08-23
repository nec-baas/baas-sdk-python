# -*- coding: utf-8 -*-
"""
User module
"""
from .service import Service


class User(object):
    """
    User

    Args:
        service (Service): Service

    Attributes:
        username (str): Username
        email (str): E-mail address
        password (str): Password
        options (dict): Options
    """

    def __init__(self, service):
        # type: (Service) -> None
        self.service = service
        self.username = None
        self.email = None
        self.password = None
        self.options = None

    @staticmethod
    def login(service, username=None, email=None, password=None, params=None):
        # type: (Service, str, str, str, dict) -> dict
        """
        Login

        Example:
            ::

                # login with username
                result = necbaas.User.login(service, username="user1", password="Passw0rD")

                # login with email
                result = necbaas.User.login(service, email="user1@example.com", password="Passw0rD")

                # login with dict
                result = necbaas.User.login(service, params={
                    "username": "foo",
                    "password": "Passw0rD"
                })

        Args:
            service (Service): Service
            username (str): User name (mandatory, if both email/params is not specified)
            email (str): E-mail (mandatory, if both username/params is not specified)
            password (str): Password (mandatory, if params is not specified)
            params (dict): dictionary. The parameter is encoded in JSON and sent to server.
                Usually contains username or email, and password. (optional)

        Returns:
            dict: Response JSON
        """
        if params is None:
            if password is None:
                raise ValueError("No password nor params")
            params = {"password": password}
            if username is not None:
                params["username"] = username
            elif email is not None:
                params["email"] = email
            else:
                raise ValueError("No username nor email")

        r = service.execute_rest("POST", "/login", json=params)
        res = r.json()

        service.session_token = res["sessionToken"]
        service.session_token_expire = res["expire"]
        return res

    @staticmethod
    def logout(service):
        # type: (Service) -> dict
        """
        Logout

        Args:
            service (Service): Service
        Returns:
            dict: Response JSON in dictionary
        """
        r = service.execute_rest("DELETE", "/login")
        res = r.json()
        service.session_token = None
        service.session_token_expire = None
        return res

    def register(self):
        # type: () -> dict
        """
        Register user.
        Specify username, email, password and options properties.

        Example:
            ::

                user = necbaas.User(service)
                user.username = "foo"
                user.email = "foo@example.com"
                user.password = "Passw0rD"
                response = user.register()

        Returns:
            dist: Registration info (JSON)
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

        r = self.service.execute_rest("POST", "/users", json=body)
        res = r.json()
        return res

    def update(self, user_id, etag=None):
        # type: (str, str) -> dict
        """
        Update user.

        Args:
            user_id (str): User ID
            etag (str): ETag (optional)

        Returns:
            dist: User info (JSON)
        """
        query = {}
        if etag is not None:
            query["etag"] = etag

        body = {}
        if self.username is not None:
            body["username"] = self.username
        if self.email is not None:
            body["email"] = self.email
        if self.password is not None:
            body["password"] = self.password
        if self.options is not None:
            body["options"] = self.options

        r = self.service.execute_rest("PUT", "/users/{}".format(user_id), query=query, json=body)
        res = r.json()
        return res

    @staticmethod
    def query(service, username=None, email=None):
        # type: (Service, str, str) -> list
        """
        Query user.

        Args:
            service (Service): Service
            username (str): Username (optional)
            email (str): E-mail (optional)
        Returns:
            list: List of user info
        """
        query = {}
        if username is not None:
            query["username"] = username
        if email is not None:
            query["email"] = email

        r = service.execute_rest("GET", "/users", query=query)
        res = r.json()
        return res["results"]

    @staticmethod
    def get(service, user_id):
        # type: (Service, str) -> dict
        """
        Get user info.

        Args:
            service (Service): Service
            user_id (str): User ID
        Returns:
            dict: User info
        """
        r = service.execute_rest("GET", "/users/{}".format(user_id))
        res = r.json()
        return res

    @staticmethod
    def remove(service, user_id):
        # type: (Service, str) -> dict
        """
        Remove user.

        Args:
            service (Service): Service
            user_id (str): User ID
        Returns:
            dict: Response JSON
        """
        r = service.execute_rest("DELETE", "/users/{}".format(user_id))
        res = r.json()
        return res

    @staticmethod
    def reset_password(service, username=None, email=None):
        # type: (Service, str, str) -> dict
        """
        Reset password.

        Args:
            service (Service): Service
            username (str): Username (optional)
            email (str): E-mail (optional)
        Returns:
            dict: Response JSON
        """
        body = {}
        if username is not None:
            body["username"] = username
        if email is not None:
            body["email"] = email

        r = service.execute_rest("POST", "/request_password_reset", json=body)
        res = r.json()
        return res

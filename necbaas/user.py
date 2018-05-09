# -*- coding: utf-8 -*-

from .service import Service


class User(object):
    """
    User

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
    def login_with_username(service, username, password):
        # type: (Service, str, str) -> dict
        """
        Login with user name

        Example:
            ::

                result = necbaas.User.login_with_username(service, "foo", "Passw0rD")

        Args:
            service (Service): Service
            username (str): User name
            password (str): Password
        Returns:
            dict: Response JSON in dictionary
        """
        return User.login(service, {
            "username": username,
            "password": password
        })

    @staticmethod
    def login_with_email(service, email, password):
        # type: (Service, str, str) -> dict
        """
        Login with E-mail

        Example:
            ::

                result = necbaas.User.login_with_email(service, "foo@example.com", "Passw0rD")

        Args:
            service (Service): Service
            email (str): User name
            password (str): Password
        Returns:
            dict: Response JSON
        """
        return User.login(service, {
            "email": email,
            "password": password
        })

    @staticmethod
    def login(service, param):
        # type: (Service, dict) -> dict
        """
        Login

        Example:
            ::

                result = necbaas.User.login(service, {
                    "username": "foo",
                    "password": "Passw0rD"
                })

        Args:
            service (Service): Service
            param (dict): dictionary. The parameter is encoded in JSON and sent to server.
                Usually contains username or email, and password.

        Returns:
            dict: Response JSON
        """
        r = service.execute_rest("POST", "/login", json=param)
        res = r.json()

        service.session_token = res["sessionToken"]
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

# -*- coding: utf-8 -*-
"""
Group module
"""
from .service import Service


class Group(object):
    """
    Group

    Args:
        service (Service): Service
        group_name (str): Group name

    Attributes:
        service (Service): Service
        group_name (str): Group name
    """

    def __init__(self, service, group_name):
        # type: (Service, str) -> None
        self.service = service
        self.group_name = group_name

    def upsert(self, users=None, groups=None, acl=None, etag=None):
        # type: (list, list, dict, str) -> dict
        """
        Create/Update group.

        Args:
            users (list): List of user ID belonging to group (optional)
            groups (list): List of group name belonging to group (optional)
            acl (dict): ACL (optional)
            etag (str): ETag (optional)

        Returns:
            dict: Response JSON
        """
        query = {}
        if etag is not None:
            query["etag"] = etag

        body = {}
        if users is not None:
            body["users"] = users
        if groups is not None:
            body["groups"] = groups
        if acl is not None:
            body["ACL"] = acl

        r = self.service.execute_rest("PUT", "/groups/{}".format(self.group_name), query=query, json=body)
        return r.json()

    @staticmethod
    def query(service):
        # type: (Service) -> list
        """
        Query groups.

        Returns:
            list: List of group info
        """
        r = service.execute_rest("GET", "/groups")
        res = r.json()
        return res["results"]

    def get(self):
        # type: () -> dict
        """
        Query group.

        Returns:
            dict: Group info
        """
        r = self.service.execute_rest("GET", "/groups/{}".format(self.group_name))
        return r.json()

    def remove(self):
        # type: () -> dict
        """
        Remove group.

        Returns:
            dict: Response json
        """
        r = self.service.execute_rest("DELETE", "/groups/{}".format(self.group_name))
        return r.json()

    def add_members(self, users=None, groups=None):
        # type: (list, list) -> dict
        """
        Add members in group.

        Args:
            users (list): List of user ID to add (optional)
            groups (list): List of group name to add (optional)

        Returns:
            dict: Group info
        """
        body = {}
        if users is not None:
            body["users"] = users
        if groups is not None:
            body["groups"] = groups

        r = self.service.execute_rest("PUT", "/groups/{}/addMembers".format(self.group_name), json=body)
        return r.json()

    def remove_members(self, users=None, groups=None):
        # type: (list, list) -> dict
        """
        Remove members in group.

        Args:
            users (list): List of user ID to remove (optional)
            groups (list): List of group name to remove (optional)

        Returns:
            dict: Group info
        """
        body = {}
        if users is not None:
            body["users"] = users
        if groups is not None:
            body["groups"] = groups

        r = self.service.execute_rest("PUT", "/groups/{}/removeMembers".format(self.group_name), json=body)
        return r.json()

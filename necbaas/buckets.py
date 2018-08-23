# -*- coding: utf-8 -*-
"""
Bucket manager module
"""
from .service import Service


class Buckets(object):
    """
    Bucket Manager

    Args:
        service (Service): Service
        bucket_type (str): Bucket type, "object" or "file".

    Attributes:
        service (Service): Service
        bucket_type (str): Bucket type, "object" or "file".
    """

    def __init__(self, service, bucket_type):
        # type: (Service, str) -> None
        self.service = service
        self.bucket_type = bucket_type

        if bucket_type is not "object" and bucket_type is not "file":
            raise ValueError("bad bucket_type")

    def upsert(self, name, desc="", acl=None, content_acl=None):
        # type: (str, str, dict, dict) -> dict
        """
        Create/Update bucket.
        
        Args:
            name (str): Bucket name
            desc (str): Description (mandatory for update)
            acl (dict): Bucket ACL (mandatory for update)
            content_acl (dict): Content ACL (mandatory for update)

        Returns:
            dict: Response JSON
        """
        body = {
            "description": desc
        }
        if acl is not None:
            body["ACL"] = acl
        if content_acl is not None:
            body["contentACL"] = content_acl
        r = self.service.execute_rest("PUT", "buckets/{}/{}".format(self.bucket_type, name), json=body)
        return r.json()

    def query(self):
        # type: () -> list
        """
        Query buckets.

        Returns:
            list: List of bucket info

        """
        r = self.service.execute_rest("GET", "buckets/{}".format(self.bucket_type))
        res = r.json()
        return res["results"]

    def get(self, name):
        # type: (str) -> dict
        """
        Query bucket.

        Args:
            name (str): Bucket name.

        Returns:
            dict: Bucket info
        """
        r = self.service.execute_rest("GET", "buckets/{}/{}".format(self.bucket_type, name))
        return r.json()

    def remove(self, name):
        # type: (str) -> dict
        """
        Remove bucket.

        Args:
            name (str): Bucket name.

        Returns:
            dict: Bucket info
        """
        r = self.service.execute_rest("DELETE", "buckets/{}/{}".format(self.bucket_type, name))
        return r.json()

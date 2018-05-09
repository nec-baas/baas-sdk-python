# -*- coding: utf-8 -*-
from .service import Service


class Buckets(object):
    """
    Bucket Manager
    """

    @staticmethod
    def upsert(service, bucket_type, name, desc="", acl=None, content_acl=None):
        # type: (Service, str, str) -> dict
        """
        Create/Update bucket.
        
        Args:
            service (Service): Service 
            bucket_type (str): Bucket type, "object" or "file". 
            name (str): Bucket name 
            desc (str): Description
            acl (dict): Bucket ACL
            content_acl (dict): Content ACL

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
        r = service.execute_rest("PUT", "buckets/{}/{}".format(bucket_type, name), json=body)
        return r.json()

    @staticmethod
    def query(service, bucket_type):
        # type: (Service, str) -> list
        """
        Query buckets.

        Args:
            service (Service): Service
            bucket_type (str): Bucket type, "object" or "file".

        Returns:
            list: List of bucket info

        """
        r = service.execute_rest("GET", "buckets/{}".format(bucket_type))
        res = r.json()
        return res["results"]

    @staticmethod
    def get(service, bucket_type, name):
        # type: (Service, str) -> dict
        """
        Query bucket.

        Args:
            service (Service): Service
            bucket_type (str): Bucket type, "object" or "file".
            name (str): Bucket name.

        Returns:
            dict: Bucket info
        """
        r = service.execute_rest("GET", "buckets/{}/{}".format(bucket_type, name))
        return r.json()

    @staticmethod
    def remove(service, bucket_type, name):
        # type: (Service, str) -> dict
        """
        Remove bucket.

        Args:
            service (Service): Service
            bucket_type (str): Bucket type, "object" or "file".
            name (str): Bucket name.

        Returns:
            dict: Bucket info
        """
        r = service.execute_rest("DELETE", "buckets/{}/{}".format(bucket_type, name))
        return r.json()

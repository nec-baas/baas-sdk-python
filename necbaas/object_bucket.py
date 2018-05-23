# -*- coding: utf-8 -*-
"""
JSON Object bucket module
"""
import json
from .service import Service


class ObjectBucket(object):
    """
    JSON Object Storage Bucket.

    Args:
        service (Service): Service
        bucket_name (str): Bucket name
    """

    service = None
    # type: Service
    """Service instance"""

    bucket_name = None
    # type: str
    """Bucket name"""

    def __init__(self, service, bucket_name):
        # type: (Service, str) -> None
        self.service = service
        self.bucket_name = bucket_name

    def query(self, where=None, order=None, skip=0, limit=None, projection=None):
        # type: (dict, str, int, int, dict) -> list
        """
        Query objects in this bucket.

        Examples:
            ::

                results = bucket.query(where={"product_name": "orange"}, order="-updatedAt", limit=100)

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)

        Returns:
            list: List of JSON objects
        """
        res = self._query(where=where, order=order, skip=skip, limit=limit, projection=projection)
        return res["results"]

    def query_with_count(self, where=None, order=None, skip=0, limit=None, projection=None):
        # type: (dict, str, int, int, dict) -> (list, int)
        """
        Query objects in this bucket (with count query).

        Examples:
            ::

                (results, count) = bucket.query(where={"product_name": "orange"}, order="-updatedAt", limit=100)

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)

        Returns:
            (list, count): Tuple of list of JSON objects and total count of query.
        """
        res = self._query(where=where, order=order, skip=skip, limit=limit, projection=projection, count=True)
        return res["results"], res["count"]

    def _query(self, where=None, order=None, skip=0, limit=None, projection=None, count=False):
        """
        Query objects (internal).

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)
            count (bool): Get total count (optional)

        Returns:
            dict: Response in JSON
        """
        query_params = {}

        if where is not None:
            query_params["where"] = json.dumps(where)
        if order is not None:
            query_params["order"] = order
        if skip > 0:
            query_params["skip"] = skip
        if limit is not None:
            query_params["limit"] = limit
        if projection is not None:
            query_params["projection"] = json.dumps(projection)
        if count:
            query_params["count"] = 1

        r = self.service.execute_rest("GET", "/objects/{}".format(self.bucket_name), query=query_params)
        return r.json()

    def insert(self, data):
        # type: (dict) -> dict
        """
        Insert JSON Object

        Examples:
            ::

                acl = {"r": ["g:authenticated"], "w": ["g:authenticated"]}
                result = bucket.insert({"name": "foo", "score": 70, "ACL": acl})

        Args:
            data (dict): Data (JSON)

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("POST", "/objects/{}".format(self.bucket_name), json=data)
        res = r.json()
        return res

    def update(self, oid, data, etag=None):
        # type: (str, dict, str) -> dict
        """
        Update JSON Object

        Args:
            oid (str): ID of Object
            data (dict): Data (JSON)
            etag (str): ETag (optional)

        Returns:
            dict: Response JSON
        """
        query_params = {}
        if etag is not None:
            query_params["etag"] = etag

        r = self.service.execute_rest("PUT", "/objects/{}/{}".format(self.bucket_name, oid),
                                      query=query_params, json=data)
        res = r.json()
        return res

    def remove(self, oid, soft_delete=False):
        # type: (str) -> dict
        """
        Remove one JSON Object

        Args:
            oid (str): Object ID
            soft_delete (bool): Soft delete (optional, default=False)

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("DELETE", "/objects/{}/{}".format(self.bucket_name, oid),
                                      query={"deleteMark": 1 if soft_delete else 0})
        res = r.json()
        return res

    def remove_with_query(self, where=None, soft_delete=False):
        # type: (dict) -> dict
        """
        Remove multiple JSON Objects

        Args:
            where (dict): Query condition (optional)
            soft_delete (bool): Soft delete (optional, default=False)

        Returns:
            dict: Response JSON
        """
        if where is None:
            where = {}

        query_params = {
            "where": json.dumps(where),
            "deleteMark": 1 if soft_delete else 0
        }
        
        r = self.service.execute_rest("DELETE", "/objects/{}".format(self.bucket_name), query=query_params)
        res = r.json()
        return res

    def batch(self, requests, soft_delete=False):
        # type: (list) -> list
        """
        Batch operation

        Examples:
            ::
                requests = [
                    {"op": "insert", "data": {"name": "foo", "score": 70}},
                    {"op": "insert", "data": {"name": "bar", "score": 80}}
                ]
                results = bucket.batch(requests)

        Args:
            requests (list): List of batch requests
            soft_delete (bool): Soft delete (optional, default=False)

        Returns:
            list: List of batch results
        """
        query = {"deleteMark": 1 if soft_delete else 0}
        body_json = {
            "requests": requests
        }
        r = self.service.execute_rest("POST", "/objects/{}/_batch".format(self.bucket_name),
                                      json=body_json, query=query)
        res = r.json()
        return res["results"]

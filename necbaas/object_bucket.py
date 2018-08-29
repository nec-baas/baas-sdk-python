# -*- coding: utf-8 -*-
"""
JSON Object bucket module
"""
import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from .service import Service


class ObjectBucket(object):
    """
    JSON Object Storage Bucket.

    Args:
        service (Service): Service
        bucket_name (str): Bucket name

    Attributes:
        service (Service): Service
        bucket_name (str): Bucket name
    """

    _MAX_QUERY_SIZE = 1500
    # type: int

    def __init__(self, service, bucket_name):
        # type: (Service, str) -> None
        self.service = service
        self.bucket_name = bucket_name

    def query(self, where=None, order=None, skip=0, limit=None, projection=None, delete_mark=False):
        # type: (dict, str, int, int, dict, bool) -> list
        """
        Query objects in this bucket.

        Examples:
            ::

                results = bucket.query(where={"product_name": "orange"}, order="-updatedAt", limit=100)

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional, default=0)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)
            delete_mark (bool): Include soft deleted data (optional, default=False)

        Returns:
            list: List of JSON objects
        """
        res = self._query(where=where, order=order, skip=skip, limit=limit, projection=projection,
                          delete_mark=delete_mark)
        return res["results"]

    def query_with_count(self, where=None, order=None, skip=0, limit=None, projection=None, delete_mark=False):
        # type: (dict, str, int, int, dict, bool) -> (list, int)
        """
        Query objects in this bucket (with count query).

        Examples:
            ::

                (results, count) = bucket.query_with_count(where={"product_name": "orange"}, order="-updatedAt", limit=100)

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional, default=0)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)
            delete_mark (bool): Include soft deleted data (optional, default=False)

        Returns:
            (list, count): Tuple of list of JSON objects and total count of query.
        """
        res = self._query(where=where, order=order, skip=skip, limit=limit, projection=projection,
                          delete_mark=delete_mark, count=True)
        return res["results"], res["count"]

    def _query(self, where=None, order=None, skip=0, limit=None, projection=None, delete_mark=False, count=False):
        """
        Query objects (internal).

        Args:
            where (dict): Query conditions (JSON) (optional)
            order (str): Sort conditions (optional)
            skip (int): Skip count (optional, default=0)
            limit (int): Limit count (optional)
            projection (dict): Projection (JSON) (optional)
            delete_mark (bool): Include delete marked data (optional, default=False)
            count (bool): Get total count (optional, default=False)

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
        if delete_mark:
            query_params["deleteMark"] = 1
        if count:
            query_params["count"] = 1

        query_string = urlencode(query_params)
        if len(query_string) < ObjectBucket._MAX_QUERY_SIZE:
            r = self.service.execute_rest("GET", "/objects/{}".format(self.bucket_name), query=query_params)
        else:
            r = self.service.execute_rest("POST", "/objects/{}/_query".format(self.bucket_name), json=query_params)

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
        # type: (str, bool) -> dict
        """
        Remove one JSON Object

        Args:
            oid (str): Object ID
            soft_delete (bool): Soft delete (optional, default=False)

        Returns:
            dict: Response JSON
        """
        if not oid:  # fail-safe: check not None nor empty to avoid remove all objects.
            raise ValueError("No oid")
        r = self.service.execute_rest("DELETE", "/objects/{}/{}".format(self.bucket_name, oid),
                                      query={"deleteMark": 1 if soft_delete else 0})
        res = r.json()
        return res

    def remove_with_query(self, where=None, soft_delete=False):
        # type: (dict, bool) -> dict
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
        # type: (list, bool) -> list
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

    def aggregate(self, pipeline, options=None):
        # type: (list, dict) -> list
        """
        Aggregation operation

        Examples:
            ::

                pipeline = [
                    {"$lookup": { ... }},
                    ...
                ]
                options = {"allowDiskUse": True}
                results = bucket.aggregate(pipeline, options)

        Args:
            pipeline (list): List of aggregation pipeline stage
            options (dist): Aggregation option parameter (optional)

        Returns:
            list: List of aggregation results
        """
        body = {"pipeline": pipeline}
        if options is not None:
            body["options"] = options

        r = self.service.execute_rest("POST", "/objects/{}/_aggregate".format(self.bucket_name), json=body)
        res = r.json()
        return res["results"]

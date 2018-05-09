# -*- coding: utf-8 -*-
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
            where (dict): Query conditions (JSON)
            order (str): Sort conditions
            skip (int): Skip count
            limit (int): Limit count
            projection (dict): Projection (JSON)

        Returns:
            list: List of JSON objects
        """
        res = self._query(where=where, order=order, skip=skip, limit=limit, projection=projection)
        return res["results"]

    def _query(self, where=None, order=None, skip=0, limit=None, projection=None, count=False):
        """
        Query objects (internal).

        Args:
            where (dict): Query conditions (JSON)
            order (str): Sort conditions
            skip (int): Skip count
            limit (int): Limit count
            projection (dict): Projection (JSON)
            count (bool): Get total count

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

        r = self.service.execute_rest("GET", "/objects/" + self.bucket_name, query=query_params)
        return r.json()

    def insert(self, data):
        # type: (dict) -> dict
        """
        Insert JSON Object

        Args:
            data (dict): Data (JSON)

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("POST", "/objects/" + self.bucket_name, json=data)
        res = r.json()
        return res

    def update(self, oid, data, etag=None):
        # type: (str, dict, str) -> dict
        """
        Update JSON Object

        Args:
            oid (str): ID of Object
            data (dict): Data (JSON)
            etag (str): ETag

        Returns:
            dict: Response JSON
        """
        query_params = {}
        if etag is not None:
            query_params["etag"] = etag

        r = self.service.execute_rest("PUT", "/objects/" + self.bucket_name + "/" + oid, query=query_params, json=data)
        res = r.json()
        return res

    def remove(self, oid):
        # type: (str) -> dict
        """
        Remove one JSON Object

        Args:
            oid (str): Object ID

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("DELETE", "/objects/" + self.bucket_name + "/" + oid, query={"deleteMark": 1})
        res = r.json()
        return res

    def remove_with_query(self, where=None):
        # type: (dict) -> dict
        """
        Remove multiple JSON Objects

        Args:
            where (dict): Query condition

        Returns:
            dict: Response JSON
        """
        if where is None:
            where = {}

        query_params = {
            "where": json.dumps(where),
            "deleteMark": 1
        }
        
        r = self.service.execute_rest("DELETE", "/objects/" + self.bucket_name, query=query_params)
        res = r.json()
        return res

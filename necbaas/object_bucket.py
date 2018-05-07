# -*- coding: utf-8 -*-
import json
from .service import Service


class ObjectBucket(object):
    """
    JSON Object Storage Bucket.

    :param Service service: Service
    :param str bucket_name: Bucket name
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
        # type: (dict, str, int, int, dict) -> dict
        """
        Query objects in this bucket

        :param dict where: Query conditions (JSON)
        :param str order: Sort conditions
        :param int skip: Skip count
        :param int limit: Limit count
        :param dict projection: Projection (JSON)
        :return:
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

        r = self.service.execute_rest("GET", "/objects/" + self.bucket_name, query=query_params)
        res = r.json()

        return res  # TODO:

    def insert(self, data):
        # type: (dict) -> dict
        """
        Insert JSON Object

        :param dict data: Data (JSON)
        :return: Inserted data
        """
        r = self.service.execute_rest("POST", "/objects/" + self.bucket_name, json=data)
        res = r.json()
        return res

    def update(self, id, data, etag=None):
        # type: (str, dict, str) -> dict
        """
        Update JSON Object

        :param str id: ID of Object
        :param dict data: Data (JSON)
        :param str etag: ETag
        :return: Updated data
        """
        query_params = {}
        if etag is not None:
            query_params["etag"] = etag

        r = self.service.execute_rest("PUT", "/objects/" + self.bucket_name + "/" + id, query=query_params, json=data)
        res = r.json()
        return res

    def remove(self, id):
        # type: (str) -> dict
        """
        Remove one JSON Object

        :param str id: ID
        :return:
        """
        r = self.service.execute_rest("DELETE", "/objects/" + self.bucket_name + "/" + id, query={"deleteMark": 1})
        res = r.json()
        return res

    def remove_with_query(self, where=None):
        # type: (dict) -> dict
        """
        Remove multiple JSON Objects

        :param dict where: Query condition
        :return:
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

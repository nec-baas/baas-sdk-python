# -*- coding: utf-8 -*-
import json
from .service import Service


class ObjectBucket(object):
    """
    JSON Object Storage Bucket.

    :param Service service: Service
    :param str bucket_name: Bucket name
    """
    def __init__(self, service, bucket_name):
        # type: (Service, str) -> None
        self.service = service
        self.bucketName = bucket_name

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

        r = self.service.execute_rest("GET", "/objects/" + self.bucketName, query=query_params)
        res = r.json()

        return res  # TODO:

    def insert(self, data):
        # type: (dict) -> dict
        """
        オブジェクトのINSERT

        :param dict data: データ
        :return: 挿入後のデータ
        """
        r = self.service.execute_rest("POST", "/objects/" + self.bucketName, json=data)
        res = r.json()
        return res

    def update(self, id, data, etag=None):
        # type: (str, dict, str) -> dict
        """
        オブジェクト更新

        :param str id: ID
        :param dict data: データ
        :param str etag: ETag
        :return: 更新後のデータ
        """
        query_params = {}
        if etag is not None:
            query_params["etag"] = etag

        r = self.service.execute_rest("PUT", "/objects/" + self.bucketName + "/" + id, query=query_params, json=data)
        res = r.json()
        return res

    def remove(self, id):
        # type: (str) -> dict
        """
        オブジェクト削除

        :param str id: ID
        :return:
        """
        r = self.service.execute_rest("DELETE", "/objects/" + self.bucketName + "/" + id, query={"deleteMark": 1})
        res = r.json()
        return res

    def remove_with_query(self, where=None):
        # type: (dict) -> dict
        """
        オブジェクト一括削除

        :param dict where: 検索条件
        :return:
        """
        if where is None:
            where = {}

        query_params = {
            "where": json.dumps(where),
            "deleteMark": 1
        }
        
        r = self.service.execute_rest("DELETE", "/objects/" + self.bucketName, query=query_params)
        res = r.json()
        return res

# -*- coding: utf-8 -*-
import json


class ObjectBucket(object):
    """
    JSON Object Storage Bucket.

    :param Service service: Service
    :param str bucket_name: Bucket name
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

    def query(self, where=None, order=None, skip=0, limit=None, projection=None):
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

        f = self.service.execute_rest("GET", "/objects/" + self.bucketName, query_params)
        res = json.loads(f.read())

        return res  # TODO:

    def insert(self, data):
        """
        オブジェクトのINSERT

        :param dict data: データ
        :return: 挿入後のデータ
        """
        f = self.service.execute_rest("POST", "/objects/" + self.bucketName, None, json.dumps(data).encode("utf-8"))
        res = json.loads(f.read())
        return res

    def update(self, id, data, etag=None):
        """
        オブジェクト更新

        :param id: ID
        :param data: データ
        :param etag: ETag
        :return: 更新後のデータ
        """
        query_params = {}
        if etag is not None:
            query_params["etag"] = etag

        f = self.service.execute_rest("PUT", "/objects/" + self.bucketName + "/" + id,
                                      query_params, json.dumps(data).encode("utf-8"))
        res = json.loads(f.read())
        return res

    def remove(self, id):
        """
        オブジェクト削除

        :param str id: ID
        :return:
        """
        f = self.service.execute_rest("DELETE", "/objects/" + self.bucketName + "/" + id, {"deleteMark": 1})
        res = json.loads(f.read())
        return res

    def remove_with_query(self, where=None):
        """
        オブジェクト一括削除

        :param where: 検索条件
        :return:
        """
        if where is None:
            where = {}

        query_params = {
            "where": json.dumps(where),
            "deleteMark": 1
        }
        
        f = self.service.execute_rest("DELETE", "/objects/" + self.bucketName, query_params)
        res = json.loads(f.read())
        return res

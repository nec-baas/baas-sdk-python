# -*- coding: UTF-8 -*-
import json


class ObjectBucket:
    """
    オブジェクトバケット
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

    def query(self, where=None, sort=None, skip=0, limit=None):
        """
        クエリ
        :param dict where: クエリ条件
        :param str sort: ソート条件
        :param int skip: スキップカウント
        :param int limit: 上限数
        :return:
        """
        query_params = {}

        if where is not None:
            query_params["where"] = json.dumps(where)
        if sort is not None:
            query_params["sort"] = sort
        if skip > 0:
            query_params["skip"] = skip
        if limit is not None:
            query_params["limit"] = limit

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

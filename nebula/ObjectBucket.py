# -*- coding: UTF-8 -*-
import json


class ObjectBucket:
    """
    オブジェクトバケット
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

    def query(self, query=None, skip=0, limit=None):
        """
        クエリ
        :param dict query: クエリ条件
        :param int skip: スキップカウント
        :param int limit: 上限数
        :return:
        """
        query_params = {}

        if query is not None:
            query_params["query"] = json.dumps(query)

        if skip > 0:
            query_params["skip"] = skip
        if limit is not None:
            query_params["limit"] = limit

        f = self.service.execute_rest("GET", "/objects/" + self.bucketName, query_params)
        res = json.loads(f.read())

        return res  # TODO:

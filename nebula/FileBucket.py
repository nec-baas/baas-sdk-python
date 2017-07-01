# -*- coding: UTF-8 -*-
import json


class FileBucket:
    """
    ファイルバケット
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

    def query(self):
        """
        ファイル一覧を取得する
        :return:
        """
        f = self.service.execute_rest("GET", "/files/" + self.bucketName)
        res = json.loads(f.read())
        return res

    def upload(self, filename, data, content_type="application/octet-stream", acl=None):
        """
        ファイルをアップロードする
        :praram str filename: ファイル名
        :param data:
        :return:
        """
        return self._upload(filename, data, content_type, "POST", acl)

    def update(self, filename, data, content_type="application/octet-stream"):
        """
        ファイルを更新する
        :praram str filename: ファイル名
        :param data:
        :return:
        """
        return self._upload(filename, data, content_type, "PUT", None)

    def _upload(self, filename, data, content_type, method, acl):
        headers = {
            "Content-Type": content_type
        }
        if acl is not None:
            headers["X-ACL"] = json.dumps(acl)

        f = self.service.execute_rest(method, self._get_file_path(filename), None, data, headers)
        res = json.loads(f.read())
        return res

    def _get_file_path(self, filename):
        return "/files/" + self.bucketName + "/" + filename

    def download(self, filename):
        """
        ファイルをダウンロードする
        :param filename: ファイル名 
        :return: file like object
        """
        f = self.service.execute_rest("GET", self._get_file_path(filename))
        return f

    def remove(self, filename):
        """
        ファイルを削除する
        :param str filename: ファイル名
        :return:
        """
        f = self.service.execute_rest("DELETE", self._get_file_path(filename))
        res = json.loads(f.read())
        return res;

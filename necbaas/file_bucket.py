# -*- coding: utf-8 -*-
import json


class FileBucket(object):
    """
    File Bucket

    :param Service service: Service
    :param str bucket_name: Bucket name
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

    def query(self):
        """
        Query file list.

        :return: Response JSON
        """
        r = self.service.execute_rest("GET", "/files/" + self.bucketName)
        res = r.json()
        return res

    def upload(self, filename, data, content_type="application/octet-stream", acl=None):
        """
        Upload file

        :praram str filename: Filename
        :param data: Data
        :return: Response JSON
        """
        return self._upload(filename, data, content_type, "POST", acl)

    def update(self, filename, data, content_type="application/octet-stream"):
        """
        Update file

        :param str filename: ファイル名
        :param data: Data
        :param str content_type: Content-Type
        :return:
        """
        return self._upload(filename, data, content_type, "PUT", None)

    def _upload(self, filename, data, content_type, method, acl):
        headers = {
            "Content-Type": content_type
        }
        if acl is not None:
            headers["X-ACL"] = json.dumps(acl)

        r = self.service.execute_rest(method, self._get_file_path(filename), data=data, headers=headers)
        res = r.json()
        return res

    def _get_file_path(self, filename):
        return "/files/" + self.bucketName + "/" + filename

    def download(self, filename):
        """
        Download file.

        Examples::

            r = bucket.download("file1")
            binary = r.content # binary content
            text = r.text      # text content
            json = r.json()    # json content

        :param filename: Filename
        :return: response (requests library)
        """
        r = self.service.execute_rest("GET", self._get_file_path(filename))
        return r

    def remove(self, filename):
        """
        Delete file

        :param str filename: Filename
        :return:
        """
        r = self.service.execute_rest("DELETE", self._get_file_path(filename))
        res = r.json()
        return res

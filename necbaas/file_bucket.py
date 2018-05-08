# -*- coding: utf-8 -*-
import json
from .service import Service
from requests import Response


class FileBucket(object):
    """
    File Bucket

    :param Service service: Service
    :param str bucket_name: Bucket name
    """

    def __init__(self, service, bucket_name):
        # type: (Service, str) -> None
        self.service = service
        self.bucketName = bucket_name

    def query(self):
        # type: () -> dict
        """
        Query file list.

        :return: Response JSON
        """
        r = self.service.execute_rest("GET", "/files/" + self.bucketName)
        res = r.json()
        return res

    def upload(self, filename, data, content_type="application/octet-stream", acl=None):
        # type: (str, any, str, dict, bool) -> dict
        """
        Upload file

        Example:
            ::

                with open("/data/data1.dat", "rb") as f:
                    bucket.upload("data1.dat", f, acl={"r": "g:anonymous"})

        :param str filename: Filename
        :param data: Data
        :param str content_type: Content-Type (default=application/octet-stream)
        :param dict acl: ACL (default=None)
        :return: Response JSON
        """
        r = self._upload(filename, data, content_type, "POST", acl=acl)
        res = r.json()
        return res

    def update(self, filename, data, content_type="application/octet-stream"):
        # type: (str, any, str, bool) -> dict
        """
        Update file

        :param str filename: File name
        :param data: Data
        :param str content_type: Content-Type
        :return: Response JSON
        """
        r = self._upload(filename, data, content_type, "PUT")
        res = r.json()
        return res

    def _upload(self, filename, data, content_type, method, acl=None):
        # type: (str, any, str, str, dict) -> Response
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

    def download(self, filename, stream=False):
        # type: (str) -> Response
        """
        Download file.

        Example:

            Example 1 without streaming::

                r = bucket.download("file1.json")
                binary = r.content   # get binary content
                #text = r.text       # get text content
                #json = r.json()     # get json content

            Example2 with streaming::

                with bucket.download("file2.zip", stream=True) as r:
                    # Do things with the response here

            For details of streaming support, see http://docs.python-requests.org/en/master/user/advanced/#streaming-requests.

        :param str filename: Filename
        :param bool stream: Stream flag
        :return: Response (requests library)
        """
        r = self.service.execute_rest("GET", self._get_file_path(filename), stream=stream)
        return r

    def remove(self, filename):
        # type: (str) -> dict
        """
        Delete file

        :param str filename: Filename
        :return: Response JSON
        """
        r = self.service.execute_rest("DELETE", self._get_file_path(filename))
        res = r.json()
        return res

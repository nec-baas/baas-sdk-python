# -*- coding: utf-8 -*-
import json
from .service import Service
from requests import Response


class FileBucket(object):
    """
    File Bucket

    Args:
        service (Service): Service
        bucket_name (str): Bucket name
    """

    def __init__(self, service, bucket_name):
        # type: (Service, str) -> None
        self.service = service
        self.bucket_name = bucket_name

    def query(self):
        # type: () -> dict
        """
        Query file list.

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("GET", "/files/{}".format(self.bucket_name))
        res = r.json()
        return res

    def get_metadata(self, filename):
        # type: (str) -> dict
        """
        Get file metadata.

        Args:
            filename (str): File name

        Returns:
            dict: File Metadata
        """
        r = self.service.execute_rest("GET", "/files/{}/{}".format(self.bucket_name, filename))
        res = r.json()
        return res

    def update_metadata(self, filename, meta, etag=None):
        # type: (str, dict) -> dict
        """
        Update file metadata

        Args:
            filename (str): File name
            meta (dict): File metadata (JSON)
            etag (str): ETag of file metadata (optional)

        Returns:
            dict: Updated file metadata
        """
        param = None
        if etag is None:
            param = {"metaETag": etag}

        r = self.service.execute_rest("PUT", "/files/{}/{}".format(self.bucket_name, filename), json=meta, param=param)
        res = r.json()
        return res

    def upload(self, filename, data, content_type="application/octet-stream", acl=None):
        # type: (str, any, str, dict) -> dict
        """
        Upload file.

        Example:
            ::

                with open("/data/data1.dat", "rb") as f:
                    bucket.upload("data1.dat", f, acl={"r": "g:anonymous"})

        Args:
            filename (str): Filename
            data (any): File data in bytes or file-like object.
            content_type (str): Content-Type (default=application/octet-stream)
            acl (dict): ACL (default=None)

        Returns:
            dict: Response JSON
        """
        r = self._upload(filename, data, content_type, "POST", acl=acl)
        res = r.json()
        return res

    def update(self, filename, data, content_type="application/octet-stream", meta_etag=None, file_etag=None):
        # type: (str, any, str) -> dict
        """
        Update file body.

        Args:
            filename (str): File name
            data (any): File data in bytes or file-like object.
            content_type (str): Content-Type
            meta_etag (str): File metadata ETag
            file_etag (str): File body ETag

        Returns:
            dict: Response JSON
        """
        params = {}
        if meta_etag is not None:
            params["metaETag"] = meta_etag
        if file_etag is not None:
            params["fileETag"] = file_etag

        r = self._upload(filename, data, content_type, "PUT", params=params)
        res = r.json()
        return res

    def _upload(self, filename, data, content_type, method, acl=None, params=None):
        # type: (str, any, str, str, dict, dict) -> Response
        headers = {
            "Content-Type": content_type
        }
        if acl is not None:
            headers["X-ACL"] = json.dumps(acl)

        r = self.service.execute_rest(method, self._get_file_path(filename), data=data, params=params, headers=headers)
        res = r.json()
        return res

    def _get_file_path(self, filename):
        return "/files/{}/{}".format(self.bucket_name, filename)

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

            For details of streaming support,
            see http://docs.python-requests.org/en/master/user/advanced/#streaming-requests.

        Args:
            filename (str): Filename
            stream (bool): Stream flag

        Returns:
            Response: Response (requests library)
        """
        r = self.service.execute_rest("GET", self._get_file_path(filename), stream=stream)
        return r

    def remove(self, filename):
        # type: (str) -> dict
        """
        Delete file

        Args:
            filename (str): Filename

        Returns:
            dict: Response JSON
        """
        r = self.service.execute_rest("DELETE", self._get_file_path(filename))
        res = r.json()
        return res

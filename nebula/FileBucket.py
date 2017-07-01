# -*- coding: UTF-8 -*-


class FileBucket:
    """
    ファイルバケット
    """
    def __init__(self, service, bucket_name):
        self.service = service
        self.bucketName = bucket_name

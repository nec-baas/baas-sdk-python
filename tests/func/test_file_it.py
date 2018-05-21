import necbaas as baas

from .test_storage_base import TestStorageBase


class TestFileStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("file")

    def teardown(self):
        self.cleanup()

    def test_upload_download(self):
        b = baas.FileBucket(self.service, "bucket1")

        # upload
        data = "abcde".encode()
        meta = b.upload("file1.txt", data=data, content_type="plain/text")
        assert meta["filename"] == "file1.txt"
        assert meta["length"] == 5
        assert meta["contentType"] == "plain/text"

        # download
        res = b.download("file1.txt")
        assert res.status_code == 200
        assert res.text == "abcde"

        # stream download
        with b.download("file1.txt", stream=True) as res:
            assert res.status_code == 200
            data = res.raw.read()
            assert data.decode() == "abcde"

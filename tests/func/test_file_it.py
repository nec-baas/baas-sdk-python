import necbaas as baas

from .test_storage_base import TestStorageBase


class TestFileStorage(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("file")

    def teardown(self):
        self.cleanup()

    def create_test_data(self, length):
        ary = []
        for i in range(length):
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            idx = i % len(alphabet)
            ary.append(alphabet[idx:idx+1])
        return ''.join(ary)

    def test_upload_download(self):
        b = baas.FileBucket(self.service, "bucket1")

        # upload
        test_data = self.create_test_data(1024)
        meta = b.upload("file1.txt", data=test_data.encode(), content_type="plain/text")
        assert meta["filename"] == "file1.txt"
        assert meta["length"] == len(test_data)
        assert meta["contentType"] == "plain/text"

        # download
        res = b.download("file1.txt")
        assert res.status_code == 200
        assert res.text == test_data

        # stream download
        with b.download("file1.txt", stream=True) as res:
            assert res.status_code == 200
            data = res.raw.read()
            assert data.decode() == test_data

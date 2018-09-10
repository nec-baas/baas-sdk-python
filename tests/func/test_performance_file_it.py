# -*- coding: utf-8 -*-
import os
import time
import pytest

import necbaas as baas
from .test_storage_base import TestStorageBase


class TestPerformanceFile(TestStorageBase):
    def setup(self):
        self.setup_bucket_and_user("file")

    def teardown(self):
        self.cleanup()
        self.remove_all_buckets()

    @pytest.mark.skip(reason='performance test')
    def test_file_count(self):
        """ファイル数/メタファイル数"""
        b = baas.FileBucket(self.service, "bucket1")

        text_data = self.create_test_data(1024 * 1024)

        with open(os.path.expanduser("~/.baas/spec_test_1mb.jpg"), "rb") as f:
            img_data = f.read()

        for i in range(500):
            filename = "TextFile_{}.txt".format(i)
            b.create(filename, data=text_data.encode(), content_type="plain/text")

            filename = "ImageFile_{}.jpg".format(i)
            b.create(filename, data=img_data, content_type="image/jpeg")

        file_list = b.query()
        assert len(file_list) == 1000

    @pytest.mark.skip(reason='performance test')
    def test_file_size(self):
        """ファイルサイズ"""
        b = baas.FileBucket(self.service, "bucket1")

        with open(os.path.expanduser("~/.baas/spec_test_100mb.mp4"), "rb") as f:
            mp4_data = f.read()

        for i in range(8):
            filename = "MovieFile_{}.mp4".format(i)
            b.create(filename, data=mp4_data, content_type="video/mp4")

        file_list = b.query()
        assert len(file_list) == 8

    @pytest.mark.skip(reason='performance test')
    def test_bucket_count(self):
        """バケット数"""
        self.remove_all_buckets()

        for i in range(1000):
            self.buckets.upsert("bucket" + str(i), content_acl={"r": ["g:authenticated"], "w": ["g:authenticated"]})

        text_data = self.create_test_data(1024 * 1024)

        for i in range(1000):
            b = baas.FileBucket(self.service, "bucket" + str(i))
            b.create("TextFile.txt", data=text_data.encode(), content_type="plain/text")

        results = self.buckets.query()
        assert len(results) == 1000

    @pytest.mark.skip(reason='performance test')
    def test_upload_time(self):
        """新規ファイルアップロード時間 (1Mbyte)"""
        b = baas.FileBucket(self.service, "bucket1")
        text_data = self.create_test_data(1024 * 1024)

        start_time = time.time()
        meta = b.create("test_file.txt", data=text_data.encode(), content_type="plain/text")
        elapsed_time = time.time() - start_time

        assert meta["length"] == len(text_data)
        assert elapsed_time < 0.9
        print("query time: " + str(elapsed_time))

    @pytest.mark.skip(reason='performance test')
    def test_download_time(self):
        """新規ファイルダウンロード時間 (1Mbyte)"""
        b = baas.FileBucket(self.service, "bucket1")
        text_data = self.create_test_data(1024 * 1024)
        b.create("test_file.txt", data=text_data.encode(), content_type="plain/text")

        start_time = time.time()
        res = b.download("test_file.txt")
        elapsed_time = time.time() - start_time

        assert res.status_code == 200
        assert res.text == text_data
        assert elapsed_time < 1.1
        print("query time: " + str(elapsed_time))

    @pytest.mark.skip(reason='durability test')
    def test_durability_file(self):
        """耐久試験：ファイルストレージ アップロード／ダウンロード"""
        b = baas.FileBucket(self.service, "bucket1")

        filename = "test_file.txt"
        text_data = self.create_test_data(1024 * 1024)

        end_time = time.time() + (48 * 60 * 60)

        while end_time >= time.time():
            # upload
            meta = b.create(filename, data=text_data.encode(), content_type="plain/text")
            assert meta["filename"] == filename
            assert meta["length"] == len(text_data)
            assert meta["contentType"] == "plain/text"

            # download
            res = b.download(filename)
            assert res.status_code == 200
            assert res.text == text_data

            # remove
            b.remove(filename)

            # sleep 1sec
            time.sleep(1)

            # update session token
            if self.service.session_token_expire - (60 * 60) < time.time():
                baas.User.login(self.service, username="user1", password="Passw0rD")

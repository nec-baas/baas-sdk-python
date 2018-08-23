# -*- coding: utf-8 -*-
import necbaas as baas

from .util import *


class TestGroup(object):
    def get_group(self, expected_result):
        service = mock_service_json_resp(expected_result)
        group = baas.Group(service, "group1")
        return service, group

    def test_upsert(self):
        """正常に upsert できること"""
        expected = {"name": "group1", "users": ["user1", "user2"]}
        service, group = self.get_group(expected)

        users = ["user3", "user4"]
        groups = ["group2", "group2"]
        acl = {"r": ["g:anonymous"], "w": ["user1"]}
        etag = "testEtag"

        result = group.upsert(users=users, groups=groups, acl=acl, etag=etag)
        assert result == expected

        assert get_rest_args(service) == ("PUT", "/groups/group1")
        query = get_rest_kwargs(service)["query"]
        assert query["etag"] == etag
        json = get_rest_kwargs(service)["json"]
        assert json["users"] == users
        assert json["groups"] == groups
        assert json["ACL"] == acl

    def test_query(self):
        """正常に検索できること"""
        expected = [{"_id": "group01", "name": "group1"}, {"_id": "group02", "name": "group2"}]
        service = mock_service_json_resp({"results": expected})

        results = baas.Group.query(service)
        assert results == expected

        assert get_rest_args(service) == ("GET", "/groups")

    def test_get(self):
        """正常に取得できること"""
        expected = {"name": "group1", "users": ["user1", "user2"]}
        service, group = self.get_group(expected)

        result = group.get()
        assert result == expected

        assert get_rest_args(service) == ("GET", "/groups/group1")

    def test_remove(self):
        """正常に削除できること"""
        expected = {}
        service, group = self.get_group(expected)

        result = group.remove()
        assert result == expected

        assert get_rest_args(service) == ("DELETE", "/groups/group1")

    def test_add_menbers(self):
        """正常にメンバ追加できること"""
        expected = {"name": "group1", "users": ["user1", "user2"]}
        service, group = self.get_group(expected)

        users = ["user3", "user4"]
        groups = ["group2", "group2"]

        result = group.add_members(users=users, groups=groups)
        assert result == expected

        assert get_rest_args(service) == ("PUT", "/groups/group1/addMembers")
        json = get_rest_kwargs(service)["json"]
        assert json["users"] == users
        assert json["groups"] == groups

    def test_remove_menbers(self):
        """正常にメンバ削除できること"""
        expected = {"name": "group1", "users": ["user1", "user2"]}
        service, group = self.get_group(expected)

        users = ["user3", "user4"]
        groups = ["group2", "group2"]

        result = group.remove_members(users=users, groups=groups)
        assert result == expected

        assert get_rest_args(service) == ("PUT", "/groups/group1/removeMembers")
        json = get_rest_kwargs(service)["json"]
        assert json["users"] == users
        assert json["groups"] == groups

# -*- coding: utf-8 -*-
import pytest
from requests.exceptions import HTTPError

import necbaas as baas
from . import util


class TestGroup(object):
    def setup(self):
        self.service = util.create_service()
        self.masterService = util.create_service(master=True)
        util.remove_all_groups()
        util.remove_all_users()

    def register_users(self, count):
        user_ids = []
        for i in range(count):
            u = baas.User(self.masterService)
            u.username = "user" + str(i)
            u.email = u.username + "@example.com"
            u.password = "Passw0rD"
            res = u.register()
            user_ids.append(res["_id"])
        return user_ids

    def register_groups(self, count):
        groups = []
        for i in range(count):
            g = baas.Group(self.masterService, "group" + str(i))
            res = g.upsert()
            groups.append(res["name"])
        return groups

    def test_upsert(self):
        """
        グループ登録・更新テスト(upsert)
        - 正常登録・更新できること
        """
        g = baas.Group(self.masterService, "group1")

        # create
        create_res = g.upsert()
        assert create_res["users"] == []
        assert create_res["groups"] == []
        assert "ACL" in create_res

        # update
        update_res = g.upsert()
        assert create_res["users"] == []
        assert create_res["groups"] == []
        assert create_res["etag"] != update_res["etag"]

    def test_upsert_with_option(self):
        """
        グループ登録・更新テスト(upsert)
        - 正常登録・更新できること
        - Etagが不一致の場合はエラーになること
        """
        user_ids = self.register_users(3)
        self.register_groups(3)
        g = baas.Group(self.masterService, "group3")

        # create
        users = [user_ids[0], user_ids[2]]
        groups = ["group1"]
        acl = {"u": ["g:authenticated"]}

        create_res = g.upsert(users=users, groups=groups, acl=acl)
        assert set(create_res["users"]) == set(users)
        assert set(create_res["groups"]) == set(groups)
        assert create_res["ACL"]["u"] == ["g:authenticated"]

        # update
        users = [user_ids[1]]
        groups = ["group0", "group2"]
        acl = {"u": ["g:anonymous"]}
        etag = create_res["etag"]

        update_res = g.upsert(users=users, groups=groups, acl=acl, etag=etag)
        assert set(update_res["users"]) == set(users)
        assert set(update_res["groups"]) == set(groups)
        assert update_res["ACL"]["u"] == ["g:anonymous"]
        assert etag != update_res["etag"]

        # update(etag mismatch)
        with pytest.raises(HTTPError) as ei:
            g.upsert(etag=etag)
        status_code = ei.value.response.status_code
        assert status_code == 409

    def test_query(self):
        """
        グループ全件検索
        """
        self.register_groups(3)

        # query
        groups = baas.Group.query(self.masterService)

        assert len(groups) == 3
        assert groups[0]["name"] == "group0"
        assert groups[1]["name"] == "group1"
        assert groups[2]["name"] == "group2"

    def test_get(self):
        """
        グループ取得
        """
        g = baas.Group(self.masterService, "group1")
        g.upsert()

        # get
        res = g.get()

        assert res["users"] == []
        assert res["groups"] == []
        assert "ACL" in res

    def test_remove(self):
        """
        グループ削除
        """
        g = baas.Group(self.masterService, "group1")
        g.upsert()

        # get
        g.remove()

    @pytest.mark.parametrize("member_num", [0, 1, 3])
    def test_add_remove_member(self, member_num):
        """
        メンバ追加・削除
        """
        user_ids = self.register_users(member_num)
        groups = self.register_groups(member_num + 1)

        g = baas.Group(self.masterService, groups[0])

        # add members
        users = user_ids
        del groups[0]
        res = g.add_members(users=users, groups=groups)

        assert set(res["users"]) == set(users)
        assert set(res["groups"]) == set(groups)

        # remove members
        res = g.remove_members(users=users, groups=groups)

        assert res["users"] == []
        assert res["groups"] == []

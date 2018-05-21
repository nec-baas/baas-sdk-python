#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../"))
import necbaas as baas

from config import CONFIG

service = baas.Service(CONFIG);

# login test
res = baas.User.login(service, username="user1", password="Passw0rD")
print("login result:", res)

print()

# object bucket
objectBucket = baas.ObjectBucket(service, "test2")

obj = objectBucket.insert({"score": 90})
print("insert:", obj)

obj["score"] = 95
res = objectBucket.update(obj["_id"], obj, obj["etag"])
print("update:", res)

res = objectBucket.query(where={})
print("query:", res)

res = objectBucket.remove_with_query({})
print("delete:", res)

print()

# file upload/download test
fileBucket = baas.FileBucket(service, "test1")

acl = {
    "r": ["g:anonymous"],
    "w": ["g:anonymous"]
}

res = fileBucket.upload("test.txt", "TESTDATA".encode("utf-8"), "plain/text", acl=acl)
#res = bucket2.update("test.txt", "TESTDATA".encode("utf-8"), "plain/text")
print(res)

res = fileBucket.query()
print(res)

res = fileBucket.download("test.txt")
print(res.text)

res = fileBucket.remove("test.txt")
print(res)

# logout
res = baas.User.logout(service)
print("logout:", res)

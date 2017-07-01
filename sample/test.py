#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../"))
import nebula

from config import CONFIG

service = nebula.Service(CONFIG);

# login test
res = nebula.User.login_with_username(service, "user1", "Passw0rD")
print("login result:", res)

print()

# object bucket
objectBucket = nebula.ObjectBucket(service, "test2")

obj = objectBucket.insert({"score": 90})
print("insert:", obj)

obj["score"] = 95
res = objectBucket.update(obj["_id"], obj, obj["etag"])
print("update:", res)

res = objectBucket.query({}, 0, -1)
print("query:", res)

res = objectBucket.remove_with_query({})
print("delete:", res)

print()

# file upload/download test
fileBucket = nebula.FileBucket(service, "test1")

acl = {
    "r": ["g:anonymous"],
    "w": ["g:anonymous"]
}

res = fileBucket.upload("test.txt", "TESTDATA".encode("utf-8"), "plain/text", acl)
#res = bucket2.update("test.txt", "TESTDATA".encode("utf-8"), "plain/text")
print(res)

res = fileBucket.query()
print(res)

res = fileBucket.download("test.txt")
print(res.read())

res = fileBucket.remove("test.txt")
print(res)

# logout
res = nebula.User.logout(service)
print("logout:", res)

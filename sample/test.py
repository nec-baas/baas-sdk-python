#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__) + "../"))
import nebula

from config import CONFIG

service = nebula.Service(CONFIG);

# login test
nebula.User.login(service, {
    "username": "user1",
    "password": "Passw0rD"
})

# object bucket query test
bucket1 = nebula.ObjectBucket(service, "test2")
res = bucket1.query({}, 0, -1)
print(res)

# file download test
bucket2 = nebula.FileBucket(service, "test1")

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


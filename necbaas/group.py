# -*- coding: utf-8 -*-
import json

class Group(object):
    """
    グループ
    """
    def __init__(self, service, name):
        self.service = service
        self.name = name


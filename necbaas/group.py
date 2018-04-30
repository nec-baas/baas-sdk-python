# -*- coding: utf-8 -*-
import json

class Group(object):
    """
    Group

    :param Service service: Service
    :param str name: Group name
    """
    def __init__(self, service, name):
        self.service = service
        self.name = name


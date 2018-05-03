# -*- coding: utf-8 -*-
from .service import Service


class Group(object):
    """
    Group

    :param Service service: Service
    :param str name: Group name
    """
    def __init__(self, service, name):
        # type: (Service, str) -> None
        self.service = service
        self.name = name


# -*- coding: utf-8 -*-
"""
Group module
"""
from .service import Service


class Group(object):
    """
    Group

    Args:
        service (Service): Service
        name (str): Group name
    """
    def __init__(self, service, name):
        # type: (Service, str) -> None
        self.service = service
        self.name = name


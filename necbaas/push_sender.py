# -*- coding: utf-8 -*-
"""
Push sender module
"""
from .service import Service


class PushSender(object):
    """
    Push sender class

    """

    @staticmethod
    def send(service, request):
        # type: (Service, dict) -> int
        """
        Send push.

        Args:
            service (Service): Service
            request (dict): Conditions to send

        Returns:
            int: Count of matched installations
        """
        r = service.execute_rest("POST", "/push/notifications", json=request)
        res = r.json()
        return res["installations"]

# -*- coding: utf-8 -*-
"""
wanipconnection.py
~~~~~~~~~~~~~~~~~~

Implements the WAN IP Connection V1 service.
"""
from .service import Service


class WANIPConnectionV1(Service):
    """
    This service type enables a UPnP control point to configure and control IP
    connections on the WAN interface of a UPnP compliant InternetGatewayDevice.
    """
